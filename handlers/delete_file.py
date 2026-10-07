# -*- coding: utf-8 -*-
"""Handlers for selective file deletion and clearing session data."""
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core import t
from .common import init_session, get_status_text, get_main_keyboard, safe_edit_or_reply


async def manage_files_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the selective file deletion / clear menu."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')

    files = session.get('files', {})
    filenames = session.get('filenames', {})

    buttons = []
    file_labels = {
        'uz': ("🇺🇿 Oʻzbekcha hisobot", "uz"),
        'ru': ("🇷🇺 Ruscha hisobot", "ru"),
        'eng': ("🇬🇧 Inglizcha hisobot", "eng"),
        'ai': ("🤖 SI (AI) hisoboti", "ai"),
        'namuna': ("📄 Namuna (.docx)", "namuna"),
    }

    has_any = False
    for key, (label, _) in file_labels.items():
        if key in files:
            has_any = True
            fn = html.escape(str(filenames.get(key, f"{key}.pdf")))
            buttons.append([
                InlineKeyboardButton(f"❌ {label} ({fn})ni oʻchirish", callback_data=f"del_file_{key}")
            ])

    # Option to clear everything
    buttons.append([
        InlineKeyboardButton("🗑 BARCHASINI TOZALASH", callback_data="confirm_clear_all")
    ])
    buttons.append([
        InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")
    ])

    kb = InlineKeyboardMarkup(buttons)
    if has_any:
        text = (
            "📁 <b>FAYLLARNI BOSHQARISH VA OʻCHIRISH:</b>\n\n"
            "Notoʻgʻri yuklangan faylni alohida oʻchirish uchun quyidagi tugmalardan birini bosing, "
            "yoki barcha fayllarni butunlay tozalang:\n"
        )
    else:
        text = (
            "📁 <b>FAYLLARNI BOSHQARISH:</b>\n\n"
            "<i>Hozircha hech qanday fayl yuklanmagan.</i>\n\n"
            "Barcha kiritilgan rekvizitlarni dastlabki holatga qaytarish uchun "
            "«Barchasini tozalash» tugmasini bosing:"
        )

    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def delete_single_file_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deletes a single uploaded file (uz, ru, eng, ai, or namuna) from user session."""
    query = update.callback_query
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')

    file_key = query.data.replace("del_file_", "")
    files = session.get('files', {})
    filenames = session.get('filenames', {})
    counts = session.get('sources_count', {})

    removed_name = filenames.get(file_key, file_key)

    # Remove from session
    files.pop(file_key, None)
    filenames.pop(file_key, None)
    counts.pop(file_key, None)

    if file_key == 'ai':
        session['ai_pcts'] = None
    elif file_key == 'namuna':
        session['phrases'] = {}

    await query.answer(f"«{removed_name}» oʻchirildi!")

    # Check if there are remaining files
    if any(k in files for k in ('uz', 'ru', 'eng', 'ai', 'namuna')):
        # Refresh the delete menu
        await manage_files_menu_callback(update, context)
    else:
        # If no files left, return to dashboard
        text = (
            f"✅ <b>«{html.escape(removed_name)}» oʻchirildi.</b>\n\n" +
            get_status_text(session)
        )
        await safe_edit_or_reply(query, text, reply_markup=get_main_keyboard(session), session=session)


async def confirm_clear_all_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clears all session data and files."""
    query = update.callback_query
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    await query.answer(t("cleared", bot_l))

    # Preserve language preference and dashboard_msg_id
    saved_bot_l = session.get('bot_lang', 'uz-latn')
    saved_doc_l = session.get('lang', 'uz-cyrl')
    saved_msg_id = session.get('dashboard_msg_id')

    context.user_data.clear()
    session = init_session(context.user_data)
    session['bot_lang'] = saved_bot_l
    session['lang'] = saved_doc_l
    session['dashboard_msg_id'] = saved_msg_id

    text = f"{t('cleared', saved_bot_l)}\n\n" + get_status_text(session)
    kb = get_main_keyboard(session)
    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)
