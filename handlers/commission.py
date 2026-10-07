# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core import t
from .common import init_session, DEFAULT_SAMPLE_COMMISSION, get_main_keyboard, safe_edit_or_reply


async def commission_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    comm = session.get('meta', {}).get('commission', DEFAULT_SAMPLE_COMMISSION)

    lines = [f"{t('comm_title', bot_l)}\n"]
    buttons = []

    for i, row in enumerate(comm):
        title, name = (row + ['', ''])[:2]
        name_disp = name if name else f"<i>{t('comm_empty', bot_l)}</i>"
        lines.append(f"<b>{i+1}. {title}:</b>\n   └ 👤 {name_disp}")
        btn_text = t("btn_comm_edit", bot_l, num=i+1)
        buttons.append([InlineKeyboardButton(btn_text, callback_data=f"edit_comm_member_{i}")])

    buttons.append([InlineKeyboardButton(t("btn_comm_reset", bot_l), callback_data="reset_commission")])
    buttons.append([InlineKeyboardButton(t("btn_back", bot_l), callback_data="main_menu")])

    kb = InlineKeyboardMarkup(buttons)
    await safe_edit_or_reply(query, "\n".join(lines), reply_markup=kb, session=session)


async def edit_comm_member_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    idx = int(query.data.replace("edit_comm_member_", ""))
    session['editing_field'] = f"comm_{idx}_name"

    comm = session.get('meta', {}).get('commission', DEFAULT_SAMPLE_COMMISSION)
    title = comm[idx][0] if idx < len(comm) else "Aʼzo"

    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_cancel", bot_l), callback_data="menu_commission")]])
    await safe_edit_or_reply(
        query,
        f"<b>{idx+1}. {title}</b>\n\n"
        f"Iltimos, ushbu aʼzoning F.I.Sh ini yozib yuboring (Masalan: <code>Г.Е. Тастанова</code> yoki boʻsh qoldirish uchun <code>-</code>):",
        reply_markup=kb,
        session=session
    )


async def reset_commission_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    session = init_session(context.user_data)
    bot_l = session.get('bot_lang', 'uz-latn')
    await query.answer(t("comm_reset_done", bot_l))
    session['meta']['commission'] = [list(row) for row in DEFAULT_SAMPLE_COMMISSION]
    await commission_menu_callback(update, context)
