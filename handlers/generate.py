import html
import io
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from core import build_docx, parse_report, parse_ai, L10N, cyr2lat, db
from .common import init_session, get_main_keyboard, get_status_text, safe_edit_or_reply


async def generate_docx_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Hujjat tayyorlanmoqda...")
    session = init_session(context.user_data)

    files = session.get('files', {})
    if not any(k in files for k in ('uz', 'ru', 'eng')):
        await query.answer("❌ Kamida bitta plagiat hisoboti zarur!", show_alert=True)
        return

    await safe_edit_or_reply(
        query,
        "⏳ <b>Asosnoma (.docx) hujjati shakllantirilmoqda...</b>\n"
        "• Manbalar tasniflanmoqda...\n"
        "• Jadval va imzo bloki tuzilmoqda...",
        session=session
    )

    try:
        reports = {}
        for k in ('uz', 'ru', 'eng'):
            if k in files and files[k]:
                reports[k] = parse_report(files[k])

        ai_pcts = None
        if 'ai' in files and files['ai']:
            ai_pcts = parse_ai(files['ai'])

        meta = session.get('meta', {})
        lang = session.get('lang', 'uz-cyrl')
        phrases = session.get('phrases', {})

        buf, counts = build_docx(
            reports=reports,
            ai_pcts=ai_pcts,
            lang=lang,
            meta=meta,
            phrases_override=phrases
        )

        fio_raw = (meta.get('fio') or 'asosnoma').split()[0]
        if lang in ('uz-latn', 'en'):
            fio_clean = cyr2lat(fio_raw)
        else:
            fio_clean = fio_raw
        fio_clean = re.sub(r'[^A-Za-zА-Яа-яЎўҚқҒғҲҳ0-9_]', '', fio_clean) or 'asosnoma'
        out_filename = f"ASOSNOMA_{fio_clean}_{lang}.docx"

        # Format breakdown stats
        stats_lines = ["📊 <b>Tahlil natijalari va manbalar:</b>\n"]
        lang_names = {'uz': "🇺🇿 Oʻzbekcha", 'ru': "🇷🇺 Ruscha", 'eng': "🇬🇧 Inglizcha"}
        cat_names = {
            'excluded': "Manba istisno",
            'citation': "Iqtiboslik",
            'biblio': "Foydalanilgan adabiyot",
            'common': "Umum qabul qilingan"
        }

        total_sources = 0
        for lk in ('uz', 'ru', 'eng'):
            if lk in counts:
                c = counts[lk]
                sub_total = sum(c.values())
                total_sources += sub_total
                details = [f"{cat_names[cat]}: {c[cat]}" for cat in ('excluded', 'citation', 'biblio', 'common') if c.get(cat, 0) > 0]
                stats_lines.append(f"• <b>{lang_names[lk]}</b>: {sub_total} ta manba ({', '.join(details)})")

        if ai_pcts:
            stats_lines.append(f"• <b>🤖 Sunʼiy intellekt</b>: SI: {ai_pcts[0]}% | Ehtimoliy: {ai_pcts[1]}% | Original: {ai_pcts[2]}%")

        stats_lines.append(f"\n<b>Jami manbalar:</b> {total_sources} ta")
        caption = "\n".join(stats_lines)

        # Log generation to SQLite database
        try:
            db.log_generation(update.effective_user.id, lang, ','.join(reports.keys()), total_sources)
        except Exception:
            pass

        buf.seek(0)

        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇺🇿 Kirillda", callback_data="gen_lang_uz-cyrl"),
                InlineKeyboardButton("🇺🇿 Lotinda", callback_data="gen_lang_uz-latn"),
            ],
            [
                InlineKeyboardButton("🇷🇺 Ruscha", callback_data="gen_lang_ru"),
                InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="gen_lang_en"),
            ],
            [
                InlineKeyboardButton("⬅️ Bosh menyuga qaytish", callback_data="main_menu"),
                InlineKeyboardButton(f"👨‍💻 Admin: @{config.ADMIN_USERNAME}", url=config.ADMIN_URL),
            ]
        ])

        await update.effective_chat.send_document(
            document=buf,
            filename=out_filename,
            caption=f"✅ <b>Asosnoma hujjati muvaffaqiyatli tayyorlandi! ({config.LANG_OPTIONS.get(lang, lang)})</b>\n\n{caption}\n\n<i>Boshqa tilda yuklab olish uchun quyidagi tugmalardan birini bosing:</i>",
            parse_mode="HTML",
            reply_markup=kb
        )

        # Send copy of generated document to Admin
        try:
            admin_id = db.get_admin_id()
            user = update.effective_user
            if admin_id and user and admin_id != user.id:
                buf.seek(0)
                u_name = html.escape(user.full_name or "Nomaʼlum")
                u_handle = f"@{user.username}" if user.username else "<i>usernamesiz</i>"
                admin_caption = (
                    "📑 <b>YANGI ASOSNOMA YARATILDI!</b>\n\n"
                    f"👤 <b>Foydalanuvchi:</b> {u_name} ({u_handle})\n"
                    f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
                    f"🎓 <b>F.I.Sh:</b> {html.escape(str(meta.get('fio', 'Kiritilmagan')))}\n"
                    f"🏛 <b>Muassasa:</b> {html.escape(str(meta.get('university', 'Kiritilmagan')))}\n"
                    f"📚 <b>Mavzu:</b> «{html.escape(str(meta.get('topic', 'Kiritilmagan')))}»\n"
                    f"🔬 <b>Ixtisoslik:</b> {html.escape(str(meta.get('spec', 'Kiritilmagan')))}\n"
                    f"🌐 <b>Hujjat tili:</b> {config.LANG_OPTIONS.get(lang, lang)}\n\n"
                    f"{caption}"
                )
                await context.bot.send_document(
                    chat_id=admin_id,
                    document=buf,
                    filename=out_filename,
                    caption=admin_caption,
                    parse_mode="HTML"
                )
        except Exception as e:
            print(f"Failed to forward document to admin: {e}")

        # Restore dashboard menu message
        await safe_edit_or_reply(query, get_status_text(session), reply_markup=get_main_keyboard(session), session=session)

    except Exception as e:
        err_esc = html.escape(str(e))
        await safe_edit_or_reply(
            query,
            f"❌ Hujjat yaratishda xatolik yuz berdi:\n<code>{err_esc}</code>\n\n" + get_status_text(session),
            reply_markup=get_main_keyboard(session),
            session=session
        )


async def generate_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    new_lang = query.data.replace("gen_lang_", "")
    session = init_session(context.user_data)
    session['lang'] = new_lang
    await generate_docx_callback(update, context)
