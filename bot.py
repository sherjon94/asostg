# -*- coding: utf-8 -*-
"""Asosnoma Generator Telegram Bot.

Anti-plagiarism (.pdf) hisobotlaridan Asosnoma (.docx) yaratuvchi Telegram bot.
"""
import logging
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import config
from handlers import (
    start_command,
    help_command,
    admin_command,
    clear_session_callback,
    main_menu_callback,
    document_handler,
    assign_type_callback,
    edit_meta_menu_callback,
    toggle_status_callback,
    toggle_degree_callback,
    edit_field_prompt_callback,
    text_input_handler,
    lang_menu_callback,
    set_lang_callback,
    bot_lang_menu_callback,
    set_bot_lang_callback,
    doc_lang_menu_callback,
    set_doc_lang_callback,
    commission_menu_callback,
    edit_comm_member_prompt,
    reset_commission_callback,
    generate_docx_callback,
    generate_lang_callback,
    load_sample_files_callback,
    admin_panel_handler,
    admin_stats_callback,
    admin_broadcast_prompt,
    admin_broadcast_send_callback,
    admin_users_list_callback,
    admin_force_sub_menu_callback,
    toggle_force_sub_callback,
    prompt_set_channel_callback,
    manage_files_menu_callback,
    delete_single_file_callback,
    confirm_clear_all_callback,
    donate_command,
    donate_menu_callback,
    feedback_prompt_handler,
    feedback_cancel_callback,
    admin_reply_command,
    check_force_sub_callback,
)
from core import db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    try:
        if isinstance(update, Update) and update.effective_chat:
            err_text = "⚠️ Kutilmagan texnik xatolik yuz berdi. Iltimos, qayta urinib koʻring yoki /start bosing."
            await update.effective_chat.send_message(err_text)
    except Exception:
        pass


def main():
    token = config.BOT_TOKEN
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 60)
        print("❌ BOT_TOKEN topilmadi yoki kiritilmagan!")
        print("Iltimos, '.env' faylini oching va bot tokeningizni kiriting:")
        print("BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz")
        print("Tokenni Telegramda @BotFather orqali olishingiz mumkin.")
        print("=" * 60 + "\n")
        sys.exit(1)

    db.init_db()

    print("🤖 Asosnoma Generator Bot ishga tushirilmoqda...")
    app = ApplicationBuilder().token(token).build()

    # Global error handler
    app.add_error_handler(error_handler)

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_panel_handler))
    app.add_handler(CommandHandler("donate", donate_command))
    app.add_handler(CommandHandler("feedback", feedback_prompt_handler))
    app.add_handler(CommandHandler("reply", admin_reply_command))
    app.add_handler(CommandHandler("lang", bot_lang_menu_callback))
    app.add_handler(CommandHandler("botlang", bot_lang_menu_callback))
    app.add_handler(CommandHandler("doclang", doc_lang_menu_callback))

    # Force Subscription check
    app.add_handler(CallbackQueryHandler(check_force_sub_callback, pattern="^check_force_sub$"))

    # Feedback callbacks
    app.add_handler(CallbackQueryHandler(feedback_prompt_handler, pattern="^feedback_prompt$"))
    app.add_handler(CallbackQueryHandler(feedback_cancel_callback, pattern="^feedback_cancel$"))

    # Admin Panel callbacks
    app.add_handler(CallbackQueryHandler(admin_panel_handler, pattern="^(admin_panel|admin_info)$"))
    app.add_handler(CallbackQueryHandler(admin_stats_callback, pattern="^admin_stats$"))
    app.add_handler(CallbackQueryHandler(admin_users_list_callback, pattern="^admin_users_list_"))
    app.add_handler(CallbackQueryHandler(admin_force_sub_menu_callback, pattern="^admin_force_sub_menu$"))
    app.add_handler(CallbackQueryHandler(toggle_force_sub_callback, pattern="^toggle_force_sub$"))
    app.add_handler(CallbackQueryHandler(prompt_set_channel_callback, pattern="^prompt_set_channel$"))
    app.add_handler(CallbackQueryHandler(admin_broadcast_prompt, pattern="^admin_broadcast_prompt$"))
    app.add_handler(CallbackQueryHandler(admin_broadcast_send_callback, pattern="^admin_broadcast_send$"))

    # File management & Selective deletion
    app.add_handler(CallbackQueryHandler(manage_files_menu_callback, pattern="^(manage_files|clear_session)$"))
    app.add_handler(CallbackQueryHandler(delete_single_file_callback, pattern="^del_file_"))
    app.add_handler(CallbackQueryHandler(confirm_clear_all_callback, pattern="^confirm_clear_all$"))

    # Donate callback
    app.add_handler(CallbackQueryHandler(donate_menu_callback, pattern="^donate_menu$"))

    # Callback queries
    app.add_handler(CallbackQueryHandler(generate_docx_callback, pattern="^gen_docx$"))
    app.add_handler(CallbackQueryHandler(generate_lang_callback, pattern="^gen_lang_"))
    app.add_handler(CallbackQueryHandler(edit_meta_menu_callback, pattern="^menu_edit_meta$"))

    # Language callbacks
    app.add_handler(CallbackQueryHandler(bot_lang_menu_callback, pattern="^menu_bot_lang$"))
    app.add_handler(CallbackQueryHandler(set_bot_lang_callback, pattern="^set_bot_lang_"))
    app.add_handler(CallbackQueryHandler(doc_lang_menu_callback, pattern="^(menu_doc_lang|menu_lang)$"))
    app.add_handler(CallbackQueryHandler(set_doc_lang_callback, pattern="^(set_doc_lang_|set_lang_)"))

    app.add_handler(CallbackQueryHandler(commission_menu_callback, pattern="^menu_commission$"))
    app.add_handler(CallbackQueryHandler(load_sample_files_callback, pattern="^load_sample_files$"))
    app.add_handler(CallbackQueryHandler(help_command, pattern="^help_menu$"))
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))

    # Sub-callbacks
    app.add_handler(CallbackQueryHandler(toggle_status_callback, pattern="^toggle_status$"))
    app.add_handler(CallbackQueryHandler(toggle_degree_callback, pattern="^toggle_degree$"))
    app.add_handler(CallbackQueryHandler(edit_field_prompt_callback, pattern="^edit_field_"))
    app.add_handler(CallbackQueryHandler(edit_comm_member_prompt, pattern="^edit_comm_member_"))
    app.add_handler(CallbackQueryHandler(reset_commission_callback, pattern="^reset_commission$"))
    app.add_handler(CallbackQueryHandler(set_lang_callback, pattern="^set_lang_"))
    app.add_handler(CallbackQueryHandler(assign_type_callback, pattern="^assign_"))

    # Documents & text & photos
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    app.add_handler(MessageHandler(filters.PHOTO, text_input_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_input_handler))

    print("✅ Bot muvaffaqiyatli ishga tushdi! Xabarlar qabul qilinmoqda...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
