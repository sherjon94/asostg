# -*- coding: utf-8 -*-
"""Feedback and support handler allowing direct communication between users and admin."""
import html
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from core import t, db
from .common import init_session, get_status_text, get_main_keyboard, safe_edit_or_reply, update_dashboard


async def feedback_prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entrypoint for /feedback command or feedback_prompt button."""
    session = init_session(context.user_data)
    session['waiting_feedback'] = True
    bot_l = session.get('bot_lang', 'uz-latn')

    text = t('feedback_prompt', bot_l)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t('btn_cancel', bot_l), callback_data="feedback_cancel")]
    ])

    if update.callback_query:
        await update.callback_query.answer()
        await safe_edit_or_reply(update.callback_query, text, reply_markup=kb, session=session)
    elif update.message:
        msg = await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
        session['dashboard_msg_id'] = msg.message_id


async def feedback_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels feedback input and returns to main menu."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    session['waiting_feedback'] = False
    await safe_edit_or_reply(query, get_status_text(session), reply_markup=get_main_keyboard(session), session=session)


async def process_user_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Processes message from user if session has waiting_feedback=True."""
    session = init_session(context.user_data)
    if not session.get('waiting_feedback'):
        return False

    user = update.effective_user
    msg = update.message
    bot_l = session.get('bot_lang', 'uz-latn')

    user_text = msg.text or msg.caption or "<i>[Fayl yoki media biriktirilgan]</i>"
    user_name = html.escape(user.full_name or "Nomaʼlum")
    username_str = f"@{user.username}" if user.username else "<i>Mavjud emas</i>"

    # Save to SQLite DB
    try:
        db.save_feedback(user.id, user.username or "", user.full_name or "", user_text)
    except Exception:
        pass

    session['waiting_feedback'] = False

    # Send to Admin
    admin_id = db.get_admin_id()
    if admin_id:
        admin_notice = (
            "📬 <b>YANGI MUROJAAT (FEEDBACK):</b>\n\n"
            f"👤 <b>Kimdan:</b> {user_name}\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"🌐 <b>Username:</b> {username_str}\n"
            f"📅 <b>Vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"💬 <b>Xabar matni:</b>\n{html.escape(user_text)}\n\n"
            "<i>💡 Ushbu xabarga bevosita 'Reply' (Javob berish) qilib, foydalanuvchiga javob yoʻllashingiz mumkin!</i>"
        )
        try:
            if msg.photo:
                await context.bot.send_photo(
                    chat_id=admin_id,
                    photo=msg.photo[-1].file_id,
                    caption=admin_notice,
                    parse_mode="HTML"
                )
            elif msg.document:
                await context.bot.send_document(
                    chat_id=admin_id,
                    document=msg.document.file_id,
                    caption=admin_notice,
                    parse_mode="HTML"
                )
            else:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=admin_notice,
                    parse_mode="HTML"
                )
        except Exception as e:
            print(f"Failed to deliver feedback to admin {admin_id}: {e}")

    # Confirm to user
    sent_text = t('feedback_sent', bot_l) + "\n\n" + get_status_text(session)
    msg_res = await update.message.reply_text(
        sent_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard(session)
    )
    session['dashboard_msg_id'] = msg_res.message_id
    return True


async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Checks if admin is replying to a forwarded feedback message.
    If so, forwards the response back to the original user.
    """
    user = update.effective_user
    msg = update.message
    if not msg or not msg.reply_to_message or not config.is_admin(user):
        return False

    replied_text = msg.reply_to_message.text or msg.reply_to_message.caption or ""
    # Look for user ID in <code>{user.id}</code>
    m_id = re.search(r'ID:.*?(\d{5,15})', replied_text)
    if not m_id:
        return False

    target_user_id = int(m_id.group(1))
    admin_text = msg.text or msg.caption or ""

    user_msg_text = (
        "👨‍💻 <b>ADMIN JAVOBI:</b>\n\n"
        f"{html.escape(admin_text)}"
    )

    try:
        if msg.photo:
            await context.bot.send_photo(
                chat_id=target_user_id,
                photo=msg.photo[-1].file_id,
                caption=user_msg_text,
                parse_mode="HTML"
            )
        elif msg.document:
            await context.bot.send_document(
                chat_id=target_user_id,
                document=msg.document.file_id,
                caption=user_msg_text,
                parse_mode="HTML"
            )
        else:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=user_msg_text,
                parse_mode="HTML"
            )
        await msg.reply_text(f"✅ Javob <code>{target_user_id}</code> ID li foydalanuvchiga muvaffaqiyatli yetkazildi!", parse_mode="HTML")
        return True
    except Exception as e:
        await msg.reply_text(f"❌ Xatolik: Foydalanuvchiga yetkazib boʻlmadi ({html.escape(str(e))})")
        return True


async def admin_reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allows admin to reply manually via /reply <user_id> <message>."""
    user = update.effective_user
    if not config.is_admin(user):
        return

    args = context.args
    if not args or len(args) < 2 or not args[0].isdigit():
        await update.message.reply_text(
            "ℹ️ <b>Foydalanish:</b> <code>/reply &lt;user_id&gt; &lt;xabar matni&gt;</code>\n\n"
            "Misol: <code>/reply 123456789 Assalomu alaykum, savolingiz boʻyicha...</code>",
            parse_mode="HTML"
        )
        return

    target_id = int(args[0])
    reply_body = " ".join(args[1:])

    try:
        await context.bot.send_message(
            chat_id=target_id,
            text=f"👨‍💻 <b>ADMIN JAVOBI:</b>\n\n{html.escape(reply_body)}",
            parse_mode="HTML"
        )
        await update.message.reply_text(f"✅ Javob <code>{target_id}</code> ID li foydalanuvchiga yetkazildi!", parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik yuz berdi: {html.escape(str(e))}")
