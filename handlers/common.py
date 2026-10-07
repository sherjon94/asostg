import asyncio
import html
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError
import config
from core import DEFAULT_META, format_short_name, cyr2lat, t, BOT_LANGUAGES, DOC_LANGUAGES

DEFAULT_SAMPLE_COMMISSION = [
    ['Илмий даражалар берувчи илмий кенгаш раиси', ''],
    ['Илмий даражалар берувчи илмий кенгаш котиби', ''],
    ['Илмий даражалар берувчи илмий кенгаш аъзоси', ''],
    ['Илмий раҳбар', ''],
    ['Илмий раҳбар', ''],
    ['Таянч докторант', ''],
]

user_locks = {}


def get_user_lock(user_id: int) -> asyncio.Lock:
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]


def init_session(user_data: dict) -> dict:
    if 'bot_lang' not in user_data:
        user_data['bot_lang'] = 'uz-latn'
    if 'lang' not in user_data:
        user_data['lang'] = 'uz-cyrl'
    if 'dashboard_msg_id' not in user_data:
        user_data['dashboard_msg_id'] = None
    if 'files' not in user_data:
        user_data['files'] = {}
    if 'filenames' not in user_data:
        user_data['filenames'] = {}
    if 'sources_count' not in user_data:
        user_data['sources_count'] = {}
    if 'ai_pcts' not in user_data:
        user_data['ai_pcts'] = None
    if 'phrases' not in user_data:
        user_data['phrases'] = {}
    if 'editing_field' not in user_data:
        user_data['editing_field'] = None
    if 'pending_file' not in user_data:
        user_data['pending_file'] = None
    if 'meta' not in user_data:
        user_data['meta'] = {
            'fio': '',
            'topic': '',
            'spec': '',
            'university': '',
            'degree': 'фалсафа доктори (PhD) диссертацияси',
            'status': 'tayanch',
            'commission': [list(row) for row in DEFAULT_SAMPLE_COMMISSION],
        }
    return user_data


def get_status_text(session: dict) -> str:
    bot_l = session.get('bot_lang', 'uz-latn')
    doc_l = session.get('lang', 'uz-cyrl')
    bot_l_name = BOT_LANGUAGES.get(bot_l, bot_l)
    doc_l_name = DOC_LANGUAGES.get(doc_l, doc_l)

    files = session.get('files', {})
    filenames = session.get('filenames', {})
    counts = session.get('sources_count', {})
    ai_pcts = session.get('ai_pcts')
    meta = session.get('meta', {})

    # 1. Hisobot fayllari holati
    def _file_status(key, label_key):
        label = t(label_key, bot_l)
        if key in files:
            cnt = counts.get(key, 0)
            cnt_str = f" ({t('sources_count', bot_l, cnt=cnt)})" if cnt else ""
            fn_clean = html.escape(str(filenames.get(key, key + '.pdf')))
            return f"• {label}: ✅ <b>{fn_clean}</b>{cnt_str}"
        return f"• {label}: {t('not_uploaded', bot_l)}"

    uz_stat = _file_status('uz', 'rep_uz')
    ru_stat = _file_status('ru', 'rep_ru')
    eng_stat = _file_status('eng', 'rep_eng')

    if 'ai' in files and ai_pcts:
        fn_ai = html.escape(str(filenames.get('ai', 'si.pdf')))
        ai_stat = (f"• {t('rep_ai', bot_l)}: ✅ <b>{fn_ai}</b> "
                   f"(SI: {ai_pcts[0]}%, Ehtimoliy: {ai_pcts[1]}%, Original: {ai_pcts[2]}%)")
    elif 'ai' in files:
        fn_ai = html.escape(str(filenames.get('ai', 'si.pdf')))
        ai_stat = f"• {t('rep_ai', bot_l)}: ✅ <b>{fn_ai}</b>"
    else:
        ai_stat = f"• {t('rep_ai', bot_l)}: {t('not_uploaded', bot_l)}"

    if 'namuna' in files:
        fn_sam = html.escape(str(filenames.get('namuna', 'namuna.docx')))
        sample_stat = f"• {t('rep_sample', bot_l)}: ✅ <b>{fn_sam}</b> ({t('sample_active', bot_l)})"
    else:
        sample_stat = f"• {t('rep_sample', bot_l)}: {t('sample_optional', bot_l)}"

    # 2. Hujjat rekvizitlari
    raw_fio = meta.get('fio') or ""
    raw_uni = meta.get('university') or ""
    raw_topic = meta.get('topic') or ""
    raw_spec = meta.get('spec') or ""
    raw_degree = meta.get('degree') or "фалсафа доктори (PhD) диссертацияси"

    def _format_field(val: str, is_topic: bool = False) -> str:
        if val and str(val).strip():
            v = cyr2lat(str(val).strip()) if bot_l in ('uz-latn', 'en') else str(val).strip()
            ev = html.escape(v)
            return f"«{ev}»" if is_topic else ev
        return f"<i>{t('empty', bot_l)}</i>"

    e_fio = _format_field(raw_fio)
    e_uni = _format_field(raw_uni)
    e_topic = _format_field(raw_topic, is_topic=True)
    e_spec = _format_field(raw_spec)

    degree_val = cyr2lat(raw_degree) if bot_l in ('uz-latn', 'en') else raw_degree
    e_degree = html.escape(str(degree_val))

    status_label = config.STATUS_LABELS.get(meta.get('status', 'tayanch'), "Tayanch doktorant")
    if bot_l in ('uz-latn', 'en'):
        status_label = cyr2lat(status_label)
    e_status = html.escape(str(status_label))

    text = (
        f"{t('files_header', bot_l)}\n"
        f"{uz_stat}\n"
        f"{ru_stat}\n"
        f"{eng_stat}\n"
        f"{ai_stat}\n"
        f"{sample_stat}\n\n"
        f"{t('meta_header', bot_l)}\n"
        f"{t('fio_label', bot_l)} {e_fio}\n"
        f"{t('uni_label', bot_l)} {e_uni}\n"
        f"{t('status_label', bot_l)} {e_status}\n"
        f"{t('topic_label', bot_l)} {e_topic}\n"
        f"{t('spec_label', bot_l)} {e_spec}\n"
        f"{t('degree_label', bot_l)} {e_degree}\n\n"
        f"{t('bot_lang_label', bot_l)} <b>{bot_l_name}</b>\n"
        f"{t('doc_lang_label', bot_l)} <b>{doc_l_name}</b>\n\n"
        f"{t('admin_label', bot_l)} @{config.ADMIN_USERNAME}\n\n"
        f"{t('tip_files', bot_l)}"
    )
    return text


def get_main_keyboard(session: dict) -> InlineKeyboardMarkup:
    bot_l = session.get('bot_lang', 'uz-latn')
    files = session.get('files', {})
    has_reports = any(k in files for k in ('uz', 'ru', 'eng'))

    buttons = []
    if has_reports:
        buttons.append([InlineKeyboardButton(t("btn_generate", bot_l), callback_data="gen_docx")])

    buttons.append([
        InlineKeyboardButton(t("btn_edit_meta", bot_l), callback_data="menu_edit_meta"),
        InlineKeyboardButton(t("btn_commission", bot_l), callback_data="menu_commission"),
    ])
    buttons.append([
        InlineKeyboardButton(t("btn_bot_lang", bot_l), callback_data="menu_bot_lang"),
        InlineKeyboardButton(t("btn_doc_lang", bot_l), callback_data="menu_doc_lang"),
    ])
    has_any_file = bool(files)
    btn_clear_label = "📁 Fayllar / Tozalash" if (has_any_file and bot_l == 'uz-latn') else ("📁 Файллар / Тозалаш" if (has_any_file and bot_l == 'uz-cyrl') else t("btn_clear", bot_l))
    buttons.append([
        InlineKeyboardButton(t("btn_sample_test", bot_l), callback_data="load_sample_files"),
        InlineKeyboardButton(btn_clear_label, callback_data="manage_files"),
    ])
    buttons.append([
        InlineKeyboardButton(t("btn_help", bot_l), callback_data="help_menu"),
        InlineKeyboardButton(t("btn_feedback", bot_l), callback_data="feedback_prompt"),
    ])
    buttons.append([
        InlineKeyboardButton(t("btn_donate", bot_l), callback_data="donate_menu"),
        InlineKeyboardButton(t("btn_admin_chat", bot_l, admin=config.ADMIN_USERNAME), url=config.ADMIN_URL),
    ])
    return InlineKeyboardMarkup(buttons)


async def safe_edit_or_reply(query, text, reply_markup=None, parse_mode="HTML", session=None):
    """Edits message if it has text, otherwise replies with a new message, tracking dashboard_msg_id."""
    if query.message and query.message.text:
        try:
            await query.message.edit_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
            if session is not None:
                session['dashboard_msg_id'] = query.message.message_id
            return
        except BadRequest as e:
            if "message is not modified" in str(e).lower():
                if session is not None:
                    session['dashboard_msg_id'] = query.message.message_id
                return
        except Exception:
            pass

    try:
        msg = await query.message.reply_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
        if session is not None:
            session['dashboard_msg_id'] = msg.message_id
    except Exception:
        if query.message and query.message.chat:
            msg = await query.message.chat.send_message(text, parse_mode=parse_mode, reply_markup=reply_markup)
            if session is not None:
                session['dashboard_msg_id'] = msg.message_id


async def update_dashboard(bot, chat_id: int, session: dict, custom_text: str = None, custom_keyboard=None):
    """
    Updates the main dashboard message in-place.
    If dashboard message does not exist or cannot be edited, sends a new one and records its message_id.
    """
    text = custom_text if custom_text is not None else get_status_text(session)
    reply_markup = custom_keyboard if custom_keyboard is not None else get_main_keyboard(session)
    msg_id = session.get('dashboard_msg_id')

    if msg_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            return
        except BadRequest as e:
            err = str(e).lower()
            if "message is not modified" in err:
                return  # Message already matches desired state
            # Message to edit not found, deleted, or expired - fall through to send fresh
        except TelegramError as e:
            err = str(e).lower()
            if "retry after" in err or "flood" in err:
                await asyncio.sleep(1.2)
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=msg_id,
                        text=text,
                        parse_mode="HTML",
                        reply_markup=reply_markup
                    )
                    return
                except Exception:
                    pass
        except Exception:
            pass

    # If msg_id was None or editing failed, send a new dashboard message
    try:
        new_msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        session['dashboard_msg_id'] = new_msg.message_id
    except Exception as e:
        print(f"Error in update_dashboard: {e}")

