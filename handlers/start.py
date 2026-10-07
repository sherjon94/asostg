# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from core import t, db
from .common import init_session, get_status_text, get_main_keyboard, safe_edit_or_reply


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        db.upsert_user(user.id, user.username, user.first_name, user.last_name)

    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')

    # Force subscription check
    from .sub_check import is_user_subscribed, get_sub_prompt_content
    subbed, ch_url = await is_user_subscribed(context.bot, user)
    if not subbed:
        p_text, p_kb = get_sub_prompt_content(session, ch_url)
        if update.message:
            msg = await update.message.reply_text(p_text, parse_mode="HTML", reply_markup=p_kb)
            session['dashboard_msg_id'] = msg.message_id
        elif update.callback_query:
            await safe_edit_or_reply(update.callback_query, p_text, reply_markup=p_kb, session=session)
        return

    text = t("welcome", bot_l, admin=config.ADMIN_USERNAME)
    status_text = get_status_text(session)
    keyboard = get_main_keyboard(session)
    
    if update.message:
        msg = await update.message.reply_text(
            text + status_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
        session['dashboard_msg_id'] = msg.message_id
    elif update.callback_query:
        await safe_edit_or_reply(update.callback_query, text + status_text, reply_markup=keyboard, session=session)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        db.upsert_user(user.id, user.username, user.first_name, user.last_name)

    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    help_text = t("help", bot_l, admin=config.ADMIN_USERNAME)
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("btn_donate", bot_l), callback_data="donate_menu"),
            InlineKeyboardButton(t("btn_admin_chat", bot_l, admin=config.ADMIN_USERNAME), url=config.ADMIN_URL),
        ],
        [InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")]
    ])
    
    if update.callback_query:
        await safe_edit_or_reply(update.callback_query, help_text, reply_markup=kb, session=session)
    elif update.message:
        msg = await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=kb)
        session['dashboard_msg_id'] = msg.message_id


async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        db.upsert_user(user.id, user.username, user.first_name, user.last_name)

    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    text = t("donate_text", bot_l, url=config.DONATE_URL)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_taps_link", bot_l), url=config.DONATE_URL)],
        [InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")]
    ])

    if update.callback_query:
        await update.callback_query.answer()
        await safe_edit_or_reply(update.callback_query, text, reply_markup=kb, session=session)
    elif update.message:
        msg = await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
        session['dashboard_msg_id'] = msg.message_id


donate_menu_callback = donate_command


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .admin import admin_panel_handler
    await admin_panel_handler(update, context)


async def clear_session_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    session['editing_field'] = None
    session['pending_file'] = None
    
    text = get_status_text(session)
    kb = get_main_keyboard(session)
    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)
