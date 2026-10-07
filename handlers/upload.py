import html
import io
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core import (
    detect_file_type, is_scanned_pdf, parse_report, parse_ai, extract_meta_from_pdf,
    extract_phrases_from_sample, format_short_name, t,
    is_archive, extract_files_from_archive,
    db, check_rate_limit, GLOBAL_PROCESSING_SEMAPHORE
)
from .common import (
    init_session, get_status_text, get_main_keyboard,
    safe_edit_or_reply, update_dashboard, get_user_lock
)
from .sub_check import is_user_subscribed, get_sub_prompt_content


def _apply_extracted_meta(session: dict, new_meta: dict):
    if not new_meta:
        return
    meta = session.get('meta', {})
    for k in ('fio', 'university', 'topic', 'spec'):
        if new_meta.get(k):
            meta[k] = new_meta[k]
    if new_meta.get('degree'):
        meta['degree'] = new_meta['degree']
    if new_meta.get('status'):
        meta['status'] = new_meta['status']
    
    # Auto fill author short name into commission row 6
    if meta.get('fio'):
        comm = meta.get('commission', [])
        if comm and len(comm) >= 6:
            comm[-1][1] = format_short_name(meta['fio'])
    session['meta'] = meta


def _process_single_file(session: dict, data: bytes, filename: str) -> str:
    """Processes a single PDF or DOCX file into session. Returns detected type."""
    detected = detect_file_type(data, filename)

    if detected == "docx":
        session['files']['namuna'] = data
        session['filenames']['namuna'] = filename
        phrases = extract_phrases_from_sample(data)
        if phrases:
            session['phrases'] = phrases
        return "docx"

    if detected == "ai":
        session['files']['ai'] = data
        session['filenames']['ai'] = filename
        pcts = parse_ai(data)
        session['ai_pcts'] = pcts
        extracted = extract_meta_from_pdf(data)
        _apply_extracted_meta(session, extracted)
        return "ai"

    if detected in ("uz", "ru", "eng"):
        session['files'][detected] = data
        session['filenames'][detected] = filename
        sources = parse_report(data)
        session['sources_count'][detected] = len(sources)
        extracted = extract_meta_from_pdf(data)
        _apply_extracted_meta(session, extracted)
        return detected

    return detected


async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = init_session(context.user_data)
    user = update.effective_user
    user_id = user.id
    chat_id = update.effective_chat.id
    doc = update.message.document
    filename = doc.file_name or "fayl.pdf"
    fn_esc = html.escape(filename)

    # 1. Track user in SQLite database
    db.upsert_user(user.id, user.username, user.first_name, user.last_name)

    # If user is writing feedback and sent a file
    if session.get('waiting_feedback'):
        from .feedback import process_user_feedback
        await process_user_feedback(update, context)
        return

    # 2. Force subscription check
    subbed, ch_url = await is_user_subscribed(context.bot, user)
    if not subbed:
        p_text, p_kb = get_sub_prompt_content(session, ch_url)
        await update_dashboard(context.bot, chat_id, session, custom_text=p_text, custom_keyboard=p_kb)
        return

    # 3. Rate limiting check (anti-flood)
    allowed, wait_sec = check_rate_limit(user_id)
    if not allowed:
        await update_dashboard(
            context.bot, chat_id, session,
            custom_text=(
                f"⏳ <b>Juda tez fayl yuborildi (Anti-flood / Navbat himoyasi).</b>\n\n"
                f"Server barqaror ishlashi uchun iltimos, <b>{wait_sec} soniya</b> kuting va qayta yuboring.\n\n" +
                get_status_text(session)
            )
        )
        return

    lock = get_user_lock(user_id)
    async with lock:
        # Check Telegram Bot API 20 MB download limit
        if doc.file_size and doc.file_size > 20 * 1024 * 1024:
            await update_dashboard(
                context.bot, chat_id, session,
                custom_text=(
                    f"⚠️ <b>«{fn_esc}» hajmi 20 MB dan katta.</b>\n\n"
                    f"Telegram botlari orqali 20 MB dan katta fayllarni qabul qilib boʻlmaydi. "
                    f"Iltimos, faylni siqib yoki kichikroq hajmda yuboring.\n\n" +
                    get_status_text(session)
                )
            )
            return

        async with GLOBAL_PROCESSING_SEMAPHORE:
            try:
                tg_file = await doc.get_file()
                file_bytes = await tg_file.download_as_bytearray()
                data = bytes(file_bytes)
            except Exception as e:
                err_esc = html.escape(str(e))
                await update_dashboard(
                    context.bot, chat_id, session,
                    custom_text=f"❌ <b>«{fn_esc}» yuklab olishda xatolik:</b> {err_esc}\n\n" + get_status_text(session)
                )
                return

        bot_l = session.get('bot_lang', 'uz-latn')

        # 1. Check if uploaded file is an archive (ZIP, RAR, 7Z)
        if is_archive(filename, data):
            extracted_files = extract_files_from_archive(data, filename)
            if not extracted_files:
                await update_dashboard(
                    context.bot, chat_id, session,
                    custom_text=f"⚠️ <b>«{fn_esc}» arxivida PDF yoki DOCX fayllari topilmadi.</b>\n\n" + get_status_text(session)
                )
                return

            # Process all extracted files, skipping scanned image PDFs
            scanned_in_arch = []
            for sub_name, sub_data in extracted_files:
                if (sub_name.lower().endswith(".pdf") or sub_data.startswith(b"%PDF")) and is_scanned_pdf(sub_data):
                    scanned_in_arch.append(sub_name)
                    continue
                _process_single_file(session, sub_data, sub_name)

            custom_notice = None
            if scanned_in_arch:
                arch_scanned_names = ", ".join(f"«{html.escape(s)}»" for s in scanned_in_arch)
                custom_notice = (
                    f"⚠️ <b>Arxiv ichidagi {arch_scanned_names} fayllari skanerlangan (rasm) koʻrinishida!</b>\n\n"
                    f"{t('err_scanned_pdf', bot_l)}\n\n" + get_status_text(session)
                )

            await update_dashboard(context.bot, chat_id, session, custom_text=custom_notice)
            return

        # 2. Check if single PDF is a scanned image
        if (filename.lower().endswith(".pdf") or data.startswith(b"%PDF")):
            if is_scanned_pdf(data):
                await update_dashboard(
                    context.bot, chat_id, session,
                    custom_text=f"⚠️ <b>«{fn_esc}» skaner qilingan (rasm) formatida!</b>\n\n"
                                f"{t('err_scanned_pdf', bot_l)}\n\n" + get_status_text(session)
                )
                return

        # 3. Single file processing
        detected = _process_single_file(session, data, filename)
        if detected in ("docx", "ai", "uz", "ru", "eng"):
            await update_dashboard(context.bot, chat_id, session)
            return

        # If unknown PDF type, prompt user inline on the dashboard
        session['pending_file'] = {'bytes': data, 'filename': filename}
        bot_l = session.get('bot_lang', 'uz-latn')
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇺🇿 Oʻzbekcha", callback_data="assign_uz"),
                InlineKeyboardButton("🇷🇺 Ruscha", callback_data="assign_ru"),
            ],
            [
                InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="assign_eng"),
                InlineKeyboardButton("🤖 SI (AI)", callback_data="assign_ai"),
            ],
            [
                InlineKeyboardButton(t("btn_cancel", bot_l), callback_data="assign_cancel")
            ]
        ])
        assign_text = (
            f"❓ <b>«{fn_esc}»</b> fayli qaysi hisobot turiga tegishli?\n"
            f"Iltimos, pastdagi tugmalardan birini tanlang:\n\n" +
            get_status_text(session)
        )
        await update_dashboard(context.bot, chat_id, session, custom_text=assign_text, custom_keyboard=kb)


async def assign_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    pending = session.get('pending_file')

    if not pending or not pending.get('bytes'):
        await safe_edit_or_reply(query, get_status_text(session), reply_markup=get_main_keyboard(session), session=session)
        return

    action = query.data
    data = pending['bytes']
    filename = pending['filename']

    if action == "assign_cancel":
        session['pending_file'] = None
        await safe_edit_or_reply(query, get_status_text(session), reply_markup=get_main_keyboard(session), session=session)
        return

    target = action.replace("assign_", "")
    if target == "ai":
        session['files']['ai'] = data
        session['filenames']['ai'] = filename
        pcts = parse_ai(data)
        session['ai_pcts'] = pcts
        extracted = extract_meta_from_pdf(data)
        _apply_extracted_meta(session, extracted)
    elif target in ("uz", "ru", "eng"):
        session['files'][target] = data
        session['filenames'][target] = filename
        sources = parse_report(data)
        session['sources_count'][target] = len(sources)
        extracted = extract_meta_from_pdf(data)
        _apply_extracted_meta(session, extracted)

    session['pending_file'] = None
    text = get_status_text(session)
    await safe_edit_or_reply(query, text, reply_markup=get_main_keyboard(session), session=session)
