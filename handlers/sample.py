from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes
import config
from core import parse_report, parse_ai, extract_meta_from_pdf, format_short_name
from .common import (
    init_session, get_status_text, get_main_keyboard,
    DEFAULT_SAMPLE_COMMISSION, safe_edit_or_reply
)


async def load_sample_files_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Namunaviy fayllar yuklanmoqda...")
    session = init_session(context.user_data)

    loaded = []
    for key, path in config.SAMPLE_FILES.items():
        if path.exists():
            try:
                data = path.read_bytes()
                session['files'][key] = data
                session['filenames'][key] = path.name

                if key in ('uz', 'ru', 'eng'):
                    sources = parse_report(data)
                    session['sources_count'][key] = len(sources)
                    extracted = extract_meta_from_pdf(data)
                    if extracted:
                        meta = session.get('meta', {})
                        for mk, mv in extracted.items():
                            if mv and not meta.get(mk):
                                meta[mk] = mv
                        session['meta'] = meta
                elif key == 'ai':
                    pcts = parse_ai(data)
                    session['ai_pcts'] = pcts

                loaded.append(path.name)
            except Exception as e:
                pass

    # Ensure commission matches sample
    meta = session.get('meta', {})
    meta['commission'] = [list(row) for row in DEFAULT_SAMPLE_COMMISSION]
    if meta.get('fio'):
        meta['commission'][-1][1] = format_short_name(meta['fio'])
    session['meta'] = meta

    if loaded:
        text = f"🧪 <b>Namunaviy test fayllari yuklandi:</b> {', '.join(loaded)}\n\n"
    else:
        text = "⚠️ Namunaviy fayllar koʻrsatilgan yoʻlda topilmadi.\n\n"

    text += get_status_text(session)
    await safe_edit_or_reply(query, text, reply_markup=get_main_keyboard(session), session=session)
