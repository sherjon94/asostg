# -*- coding: utf-8 -*-
"""Admin control panel: statistics, broadcast messaging, and user management."""
import asyncio
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest, TelegramError
from telegram.ext import ContextTypes
import config
from core import t, db
from .common import init_session, get_status_text, get_main_keyboard, safe_edit_or_reply


async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for /admin command or admin_info callback."""
    user = update.effective_user
    if not user:
        return

    # Track user in database
    db.upsert_user(user.id, user.username, user.first_name, user.last_name)

    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')

    # If NOT admin, show regular admin contact info
    if not config.is_admin(user):
        contact_text = t("admin", bot_l, admin=config.ADMIN_USERNAME, url=config.ADMIN_URL)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t("btn_admin_chat", bot_l, admin=config.ADMIN_USERNAME), url=config.ADMIN_URL)],
            [InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")]
        ])
        if update.callback_query:
            await update.callback_query.answer()
            await safe_edit_or_reply(update.callback_query, contact_text, reply_markup=kb, session=session)
        elif update.message:
            msg = await update.message.reply_text(contact_text, parse_mode="HTML", reply_markup=kb)
            session['dashboard_msg_id'] = msg.message_id
        return

    # Admin Control Panel
    if update.callback_query:
        await update.callback_query.answer()

    text = (
        "👑 <b>ADMIN BOSHQARUV PANELI</b>\n\n"
        f"Assalomu alaykum, <b>@{config.ADMIN_USERNAME}</b>!\n"
        "Bot statistikasi va boshqaruv vositalaridan birini tanlang:\n"
    )

    force_sub_mark = "✅" if db.get_setting('force_sub_enabled', '0') == '1' else "❌"
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Bot Statistikasi", callback_data="admin_stats"),
            InlineKeyboardButton("👥 Foydalanuvchilar (@)", callback_data="admin_users_list_0"),
        ],
        [
            InlineKeyboardButton("📢 Xabar tarqatish", callback_data="admin_broadcast_prompt"),
            InlineKeyboardButton(f"📢 Majburiy kanal ({force_sub_mark})", callback_data="admin_force_sub_menu"),
        ],
        [
            InlineKeyboardButton("⬅️ Bosh menyuga qaytish", callback_data="main_menu")
        ]
    ])

    if update.callback_query:
        await safe_edit_or_reply(update.callback_query, text, reply_markup=kb, session=session)
    elif update.message:
        msg = await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
        session['dashboard_msg_id'] = msg.message_id


async def admin_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows comprehensive system stats."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)

    stats = db.get_stats()

    recent_lines = []
    for i, u in enumerate(stats['recent_users'], 1):
        uname = f"@{u['username']}" if u.get('username') else f"ID: {u['user_id']}"
        fname = html.escape(u.get('first_name') or 'Nomaʼlum')
        time_str = u.get('last_active') or ''
        recent_lines.append(f"{i}. <b>{fname}</b> ({uname}) — <code>{time_str}</code>")

    recent_text = "\n".join(recent_lines) if recent_lines else "<i>Hozircha foydalanuvchilar yoʻq</i>"

    text = (
        "📊 <b>BOT FOYDALANISH STATISTIKASI:</b>\n\n"
        f"👥 <b>Jami foydalanuvchilar:</b> {stats['total_users']} ta\n"
        f"🟢 <b>Bugungi faol foydalanuvchilar:</b> {stats['active_today']} ta\n"
        f"🚫 <b>Botni bloklaganlar:</b> {stats['blocked_users']} ta\n"
        f"📄 <b>Yaratilgan Asosnomalar:</b> {stats['total_generations']} ta\n\n"
        f"🕒 <b>Soʻnggi faol foydalanuvchilar:</b>\n{recent_text}"
    )

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Yangilash", callback_data="admin_stats"),
            InlineKeyboardButton("📢 Xabar tarqatish", callback_data="admin_broadcast_prompt"),
        ],
        [
            InlineKeyboardButton("⬅️ Admin menyusi", callback_data="admin_panel"),
            InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu"),
        ]
    ])

    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def admin_broadcast_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts admin to enter broadcast message."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    session['admin_action'] = 'awaiting_broadcast'

    stats = db.get_stats()
    text = (
        "📢 <b>BARCHA FOYDALANUVCHILARGA XABAR TARQATISH:</b>\n\n"
        f"Hozirda bazada <b>{stats['total_users']} ta</b> foydalanuvchi mavjud.\n\n"
        "Iltimos, barchaga yubormoqchi boʻlgan xabaringizni yozib yuboring.\n"
        "<i>(Oddiy matn, rasm, video yoki fayl yuborishingiz mumkin. Xabar qanday boʻlsa shunday nusxalanadi)</i>."
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="admin_panel")]
    ])

    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def admin_broadcast_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores incoming broadcast message and asks for final confirmation."""
    session = init_session(context.user_data)
    user = update.effective_user
    if not config.is_admin(user) or session.get('admin_action') != 'awaiting_broadcast':
        return False

    session['broadcast_source'] = {
        'chat_id': update.effective_chat.id,
        'message_id': update.message.message_id
    }
    session['admin_action'] = None

    stats = db.get_stats()
    text = (
        "⚠️ <b>DIQQAT! XABARNI TASDIQLASH:</b>\n\n"
        f"Ushbu xabar bazadagi <b>{stats['total_users']} ta</b> foydalanuvchiga yuboriladi.\n\n"
        "Haqiqatan ham xabarni tarqatishni xohlaysizmi?"
    )

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Ha, yuborilsin!", callback_data="admin_broadcast_send"),
            InlineKeyboardButton("❌ Bekor qilish", callback_data="admin_panel"),
        ]
    ])

    msg = await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
    session['dashboard_msg_id'] = msg.message_id
    return True


async def admin_broadcast_send_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Executes the broadcast loop."""
    query = update.callback_query
    await query.answer("Xabar tarqatish boshlandi...")
    session = init_session(context.user_data)

    src = session.get('broadcast_source')
    if not src:
        await safe_edit_or_reply(query, "❌ Tarqatish uchun xabar topilmadi.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Orqaga", callback_data="admin_panel")]]), session=session)
        return

    active_user_ids = db.get_all_active_users()
    total = len(active_user_ids)

    status_msg = await query.message.edit_text(
        f"⏳ <b>Xabar tarqatilmoqda...</b>\n"
        f"Jami foydalanuvchilar: {total} ta\n"
        f"Iltimos, kuting...",
        parse_mode="HTML"
    )

    sent = 0
    blocked = 0
    failed = 0

    for i, uid in enumerate(active_user_ids):
        try:
            await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=src['chat_id'],
                message_id=src['message_id']
            )
            sent += 1
            await asyncio.sleep(0.04)  # 25 messages per second safe limit
        except Forbidden:
            db.set_user_blocked(uid, True)
            blocked += 1
        except TelegramError as e:
            if "retry after" in str(e).lower():
                await asyncio.sleep(1.5)
                try:
                    await context.bot.copy_message(
                        chat_id=uid,
                        from_chat_id=src['chat_id'],
                        message_id=src['message_id']
                    )
                    sent += 1
                except Exception:
                    failed += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    session['broadcast_source'] = None

    result_text = (
        "✅ <b>XABAR TARQATISH YAKUNLANDI!</b>\n\n"
        f"• 📨 <b>Muvaffaqiyatli yetkazildi:</b> {sent} ta\n"
        f"• 🚫 <b>Botni bloklaganlar:</b> {blocked} ta\n"
        f"• ⚠️ <b>Yetkazib boʻlmadi (xatolik):</b> {failed} ta\n"
        f"• 👥 <b>Jami urinishlar:</b> {total} ta"
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Admin menyusi", callback_data="admin_panel")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")],
    ])

    await safe_edit_or_reply(query, result_text, reply_markup=kb, session=session)


async def admin_users_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows paginated list of all users with their @usernames, full names, last active, and generated count."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)

    data = query.data or "admin_users_list_0"
    offset_str = data.replace("admin_users_list_", "")
    offset = int(offset_str) if offset_str.isdigit() else 0
    limit = 10

    total_count = db.count_users()
    users = db.get_users_list(limit=limit, offset=offset)

    if not users:
        list_text = "<i>Foydalanuvchilar topilmadi.</i>"
    else:
        lines = []
        for i, u in enumerate(users, start=offset + 1):
            uname = f"@{u['username']}" if u.get('username') else "<i>(usernamesiz)</i>"
            fname = html.escape(u.get('first_name') or "")
            lname = html.escape(u.get('last_name') or "")
            full_name = f"{fname} {lname}".strip() or "Nomaʼlum"
            gens = u.get('gen_count', 0)
            last_act = u.get('last_active') or "Nomaʼlum"
            lines.append(
                f"{i}. <b>{full_name}</b> ({uname})\n"
                f"   🆔 <code>{u['user_id']}</code> | 🕒 {last_act} | 📄 <b>{gens} ta</b> asosnoma"
            )
        list_text = "\n\n".join(lines)

    text = (
        f"👥 <b>BOT FOYDALANUVCHILARI ROʻYXATI:</b>\n\n"
        f"Jami roʻyxatdan oʻtganlar: <b>{total_count} ta</b>\n"
        f"Sahifa: <b>{offset // limit + 1} / {max(1, (total_count + limit - 1) // limit)}</b>\n\n"
        f"{list_text}"
    )

    nav_buttons = []
    if offset >= limit:
        nav_buttons.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"admin_users_list_{offset - limit}"))
    if offset + limit < total_count:
        nav_buttons.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"admin_users_list_{offset + limit}"))

    buttons = []
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([
        InlineKeyboardButton("👑 Admin menyusi", callback_data="admin_panel"),
        InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")
    ])

    kb = InlineKeyboardMarkup(buttons)
    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def admin_force_sub_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin interface to configure mandatory channel subscription."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)

    enabled = db.get_setting('force_sub_enabled', '0') == '1'
    channel = db.get_setting('force_sub_channel', 'Belgilanmagan')
    channel_url = db.get_setting('force_sub_channel_url', 'Belgilanmagan')

    status_str = "🟢 <b>YOQILGAN</b>" if enabled else "🔴 <b>OʻCHIRILGAN</b>"
    text = (
        "📢 <b>MAJBURIY KANAL OBUNASI SOZLAMALARI:</b>\n\n"
        f"• Holat: {status_str}\n"
        f"• Kanal: <code>{html.escape(channel)}</code>\n"
        f"• Havola: {html.escape(channel_url)}\n\n"
        "<i>💡 Eslatma: Ushbu funksiya yoqilgan boʻlsa, foydalanuvchilar botdan foydalanishdan oldin "
        "koʻrsatilgan kanalga aʼzo boʻlishi shart qilinadi.</i>\n\n"
        "<b>Muhim:</b> Bot kanalga administrator qilib qoʻshilgan boʻlishi zarur (aʼzolarni tekshira olishi uchun)!"
    )

    toggle_btn_text = "🔴 Oʻchirish" if enabled else "🟢 Yoqish"
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(toggle_btn_text, callback_data="toggle_force_sub"),
            InlineKeyboardButton("✏️ Kanalni oʻzgartirish", callback_data="prompt_set_channel"),
        ],
        [
            InlineKeyboardButton("👑 Admin menyusi", callback_data="admin_panel"),
            InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu"),
        ]
    ])

    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def toggle_force_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggles force subscription ON or OFF."""
    query = update.callback_query
    session = init_session(context.user_data)
    enabled = db.get_setting('force_sub_enabled', '0') == '1'
    new_state = '0' if enabled else '1'
    db.set_setting('force_sub_enabled', new_state)
    await query.answer("Holat oʻzgartirildi!")
    await admin_force_sub_menu_callback(update, context)


async def prompt_set_channel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts admin to enter new channel username or link."""
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    session['admin_action'] = 'awaiting_channel'

    text = (
        "✏️ <b>MAJBURIY KANALNI BIRIKTIRISH:</b>\n\n"
        "Iltimos, kanalingizning username yoki havolasini yuboring.\n\n"
        "Masalan:\n"
        "• <code>@ilm_fan_yangiliklari</code>\n"
        "• <code>https://t.me/ilm_fan_yangiliklari</code>\n"
        "• Yoki kanal ID si: <code>-1001234567890</code>"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="admin_force_sub_menu")]
    ])
    await safe_edit_or_reply(query, text, reply_markup=kb, session=session)


async def admin_set_channel_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Saves the channel username and URL provided by admin."""
    session = init_session(context.user_data)
    if session.get('admin_action') != 'awaiting_channel':
        return False

    raw_text = update.message.text.strip()
    session['admin_action'] = None

    if "t.me/" in raw_text:
        ch_name = raw_text.split("t.me/")[-1].strip().split("/")[0]
        channel_username = f"@{ch_name}" if not ch_name.startswith("@") and not ch_name.startswith("-") else ch_name
        channel_url = f"https://t.me/{ch_name.lstrip('@')}"
    elif raw_text.startswith("@"):
        channel_username = raw_text
        channel_url = f"https://t.me/{raw_text.lstrip('@')}"
    elif raw_text.startswith("-100") or raw_text.startswith("-"):
        channel_username = raw_text
        channel_url = "https://t.me"
    else:
        channel_username = f"@{raw_text}"
        channel_url = f"https://t.me/{raw_text}"

    db.set_setting('force_sub_channel', channel_username)
    db.set_setting('force_sub_channel_url', channel_url)
    db.set_setting('force_sub_enabled', '1')

    msg = await update.message.reply_text(
        f"✅ <b>Kanal muvaffaqiyatli saqlandi va majburiy obuna yoqildi!</b>\n\n"
        f"• Kanal: <code>{channel_username}</code>\n"
        f"• Havola: {channel_url}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 Admin menyusi", callback_data="admin_panel")]
        ])
    )
    session['dashboard_msg_id'] = msg.message_id
    return True
