# -*- coding: utf-8 -*-
"""Channel subscription verification logic and prompt rendering."""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from core import t, db
from .common import init_session, get_status_text, get_main_keyboard, update_dashboard, safe_edit_or_reply


async def is_user_subscribed(bot, user) -> tuple[bool, str]:
    """
    Checks if a user is subscribed to the mandatory channel.
    Returns (is_subscribed: bool, channel_url: str).
    Admin is always exempt. If force subscription is disabled, returns (True, '').
    """
    if not user:
        return True, ""
    if config.is_admin(user):
        return True, ""

    enabled = db.get_setting('force_sub_enabled', '0') == '1'
    if not enabled:
        return True, ""

    channel = db.get_setting('force_sub_channel', '').strip()
    if not channel:
        return True, ""

    channel_url = db.get_setting('force_sub_channel_url', '').strip()
    if not channel_url:
        clean_ch = channel.lstrip('@')
        channel_url = f"https://t.me/{clean_ch}"

    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user.id)
        if member.status in ('creator', 'administrator', 'member', 'restricted'):
            return True, channel_url
        return False, channel_url
    except Exception:
        # Fail-open if bot lacks rights or channel not configured properly
        return True, channel_url


def get_sub_prompt_content(session: dict, channel_url: str) -> tuple[str, InlineKeyboardMarkup]:
    """Returns the alert text and keyboard asking the user to subscribe."""
    bot_l = session.get('bot_lang', 'uz-latn')
    text = t('force_sub_prompt', bot_l)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t('btn_sub_channel', bot_l), url=channel_url)],
        [InlineKeyboardButton(t('btn_check_sub', bot_l), callback_data="check_force_sub")]
    ])
    return text, kb


async def check_force_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback when user clicks '✅ Aʼzolikni tekshirish'."""
    query = update.callback_query
    session = init_session(context.user_data)
    user = update.effective_user

    subbed, ch_url = await is_user_subscribed(context.bot, user)
    if subbed:
        await query.answer("✅ Rahmat! Aʼzoligingiz tasdiqlandi.", show_alert=True)
        await safe_edit_or_reply(query, get_status_text(session), reply_markup=get_main_keyboard(session), session=session)
    else:
        await query.answer("⚠️ Siz hali kanalga aʼzo boʻlmadingiz! Iltimos, avval aʼzo boʻling.", show_alert=True)
