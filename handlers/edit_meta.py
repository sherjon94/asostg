import html
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from core import format_short_name, t, BOT_LANGUAGES, DOC_LANGUAGES, cyr2lat
from .common import init_session, get_status_text, get_main_keyboard, safe_edit_or_reply


async def edit_meta_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    meta = session.get('meta', {})

    status_cur = "Tayanch" if meta.get('status') == 'tayanch' else "Mustaqil"
    if bot_l in ('uz-latn', 'en'):
        status_cur = cyr2lat(status_cur)
    degree_cur = "PhD" if "phd" in (meta.get('degree') or "").lower() else "DSc"

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("btn_edit_fio", bot_l), callback_data="edit_field_fio"),
            InlineKeyboardButton(t("btn_edit_uni", bot_l), callback_data="edit_field_uni"),
        ],
        [
            InlineKeyboardButton(f"🎓 {status_cur} 🔁", callback_data="toggle_status"),
            InlineKeyboardButton(f"📜 {degree_cur} 🔁", callback_data="toggle_degree"),
        ],
        [
            InlineKeyboardButton(t("btn_edit_topic", bot_l), callback_data="edit_field_topic"),
        ],
        [
            InlineKeyboardButton(t("btn_edit_spec", bot_l), callback_data="edit_field_spec"),
        ],
        [
            InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu"),
        ]
    ])

    raw_fio = meta.get('fio') or ""
    raw_uni = meta.get('university') or ""
    raw_topic = meta.get('topic') or ""
    raw_spec = meta.get('spec') or ""
    degree = meta.get('degree') or 'PhD'
    if bot_l in ('uz-latn', 'en'):
        degree = cyr2lat(degree)

    def _format_field(val: str, is_topic: bool = False) -> str:
        if val and str(val).strip():
            v = cyr2lat(str(val).strip()) if bot_l in ('uz-latn', 'en') else str(val).strip()
            ev = html.escape(v)
            return f"«{ev}»" if is_topic else ev
        return f"<i>{t('empty', bot_l)}</i>"

    e_fio = _format_field(raw_fio)
    e_uni = _format_field(raw_uni)
    e_status = html.escape(str(status_cur))
    e_topic = _format_field(raw_topic, is_topic=True)
    e_spec = _format_field(raw_spec)
    e_degree = html.escape(str(degree))

    text = (
        f"{t('edit_menu_title', bot_l)}\n\n"
        f"{t('fio_label', bot_l)} {e_fio}\n"
        f"{t('uni_label', bot_l)} {e_uni}\n"
        f"{t('status_label', bot_l)} {e_status}\n"
        f"{t('topic_label', bot_l)} {e_topic}\n"
        f"{t('spec_label', bot_l)} {e_spec}\n"
        f"{t('degree_label', bot_l)} {e_degree}\n"
    )
    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def toggle_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    meta = session.get('meta', {})
    cur = meta.get('status', 'tayanch')
    meta['status'] = 'mustaqil' if cur == 'tayanch' else 'tayanch'
    session['meta'] = meta
    await edit_meta_menu_callback(update, context)


async def toggle_degree_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    meta = session.get('meta', {})
    cur = meta.get('degree', '')
    if "dsc" in cur.lower() or "фан доктори" in cur.lower():
        meta['degree'] = "фалсафа доктори (PhD) диссертацияси"
    else:
        meta['degree'] = "фан доктори (DSc) диссертацияси"
    session['meta'] = meta
    await edit_meta_menu_callback(update, context)


async def edit_field_prompt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    field = query.data.replace("edit_field_", "")
    session['editing_field'] = field

    prompts = {
        'fio': t('prompt_fio', bot_l),
        'uni': t('prompt_uni', bot_l),
        'topic': t('prompt_topic', bot_l),
        'spec': t('prompt_spec', bot_l),
    }

    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_cancel", bot_l), callback_data="menu_edit_meta")]])
    await safe_edit_or_reply(query, prompts.get(field, "Yangi qiymatni yuboring:"), reply_markup=kb, session=session)


async def text_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = init_session(context.user_data)
    user = update.effective_user
    if user:
        from core import db
        db.upsert_user(user.id, user.username, user.first_name, user.last_name)

    # 1. Direct admin reply to forwarded feedback
    from .feedback import handle_admin_reply, process_user_feedback
    if update.message and update.message.reply_to_message and config.is_admin(user):
        replied = await handle_admin_reply(update, context)
        if replied:
            return

    # 2. Admin setting mandatory channel
    if session.get('admin_action') == 'awaiting_channel':
        from .admin import admin_set_channel_input
        handled = await admin_set_channel_input(update, context)
        if handled:
            return

    # 3. User submitting feedback / message
    if session.get('waiting_feedback'):
        handled = await process_user_feedback(update, context)
        if handled:
            return

    # 4. Check if admin is entering broadcast message
    if session.get('admin_action') == 'awaiting_broadcast':
        from .admin import admin_broadcast_confirm
        handled = await admin_broadcast_confirm(update, context)
        if handled:
            return

    bot_l = session.get('bot_lang', 'uz-latn')
    field = session.get('editing_field')

    if not field:
        msg = await update.message.reply_text(
            t("tip_files", bot_l),
            parse_mode="HTML",
            reply_markup=get_main_keyboard(session)
        )
        session['dashboard_msg_id'] = msg.message_id
        return

    text = update.message.text.strip()
    meta = session.get('meta', {})

    if field == 'fio':
        text = re.sub(r'(?i)\b(угли|ўғли|ўгли)\b', 'ўғли', text)
        text = re.sub(r'(?i)\b(кизи|қизи)\b', 'қизи', text)
        text = re.sub(r'(?i)\b(o[\'ʻ’`]?g[\'ʻ’`]?li)\b', "oʻgʻli", text)
        text = re.sub(r'(?i)\b(qizi)\b', "qizi", text)
        meta['fio'] = text
        comm = meta.get('commission', [])
        if comm and not comm[-1][1]:
            comm[-1][1] = format_short_name(text)
    elif field == 'uni':
        meta['university'] = text
    elif field == 'topic':
        meta['topic'] = text
    elif field == 'spec':
        meta['spec'] = text
    elif field.startswith('comm_'):
        idx = int(field.split('_')[1])
        sub = field.split('_')[2]
        comm = meta.get('commission', [])
        if 0 <= idx < len(comm):
            if sub == 'name':
                if text.strip() in ('-', '--', "bo'sh", "boʻsh", 'bosh', 'empty', 'clear', 'пусто'):
                    comm[idx][1] = ""
                else:
                    comm[idx][1] = text
            elif sub == 'title':
                comm[idx][0] = text

    session['editing_field'] = None
    session['meta'] = meta

    msg = await update.message.reply_text(
        f"{t('meta_saved', bot_l)}\n\n" + get_status_text(session),
        parse_mode="HTML",
        reply_markup=get_main_keyboard(session)
    )
    session['dashboard_msg_id'] = msg.message_id


# --- Bot Interface Language Menu ---
async def bot_lang_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    session = init_session(context.user_data)
    cur_lang = session.get('bot_lang', 'uz-latn')

    buttons = []
    for code, label in BOT_LANGUAGES.items():
        mark = " ✅" if code == cur_lang else ""
        buttons.append([InlineKeyboardButton(f"{label}{mark}", callback_data=f"set_bot_lang_{code}")])
    buttons.append([InlineKeyboardButton(t("btn_back", cur_lang), callback_data="main_menu")])

    kb = InlineKeyboardMarkup(buttons)
    text = t("choose_bot_lang", cur_lang)
    if query:
        await safe_edit_or_reply(query, text, reply_markup=kb, session=session)
    elif update.message:
        msg = await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
        session['dashboard_msg_id'] = msg.message_id


async def set_bot_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    new_lang = query.data.replace("set_bot_lang_", "")
    await query.answer("Bot tili oʻzgartirildi!")
    session = init_session(context.user_data)
    session['bot_lang'] = new_lang

    text = f"{t('bot_lang_changed', new_lang, lang=BOT_LANGUAGES.get(new_lang, new_lang))}\n\n"
    text += get_status_text(session)
    await safe_edit_or_reply(query, text, reply_markup=get_main_keyboard(session), session=session)


# --- Document Output Language Menu ---
async def doc_lang_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    cur_doc_lang = session.get('lang', 'uz-cyrl')

    buttons = []
    for code, label in DOC_LANGUAGES.items():
        mark = " ✅" if code == cur_doc_lang else ""
        buttons.append([InlineKeyboardButton(f"{label}{mark}", callback_data=f"set_doc_lang_{code}")])
    buttons.append([InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")])

    kb = InlineKeyboardMarkup(buttons)
    text = t("choose_doc_lang", bot_l)
    if query:
        await safe_edit_or_reply(query, text, reply_markup=kb, session=session)
    elif update.message:
        msg = await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
        session['dashboard_msg_id'] = msg.message_id


async def set_doc_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Hujjat tili tanlandi!")
    session = init_session(context.user_data)
    new_lang = query.data.replace("set_doc_lang_", "").replace("set_lang_", "")
    session['lang'] = new_lang
    bot_l = session.get('bot_lang', 'uz-latn')

    files = session.get('files', {})
    has_reports = any(k in files for k in ('uz', 'ru', 'eng'))
    buttons = []
    if has_reports:
        buttons.append([InlineKeyboardButton(f"🚀 {DOC_LANGUAGES.get(new_lang, '')}da Asosnoma yaratish", callback_data="gen_docx")])
    buttons.append([
        InlineKeyboardButton(t("btn_doc_lang", bot_l), callback_data="menu_doc_lang"),
        InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")
    ])
    buttons.append([
        InlineKeyboardButton(t("btn_admin_chat", bot_l, admin=config.ADMIN_USERNAME), url=config.ADMIN_URL),
    ])

    text = f"{t('doc_lang_changed', bot_l, lang=DOC_LANGUAGES.get(new_lang, new_lang))}\n\n"
    text += get_status_text(session)
    await safe_edit_or_reply(query, text, reply_markup=InlineKeyboardMarkup(buttons), session=session)


# Backwards compatibility aliases
lang_menu_callback = doc_lang_menu_callback
set_lang_callback = set_doc_lang_callback
