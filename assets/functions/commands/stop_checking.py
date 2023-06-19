from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from assets.functions.additional.remove_job_if_exists import remove_job_if_exists


async def stopchecking(update: Update, context: ContextTypes):
    chat_id = update.effective_message.chat_id

    job_removed = remove_job_if_exists(str(chat_id), context)

    if job_removed:
        await update.message.reply_text(
            "Мониторинг остановлен! Используйте команду "
            "/help при возникновении трудностей.")
    else:
        await update.message.reply_text(
            "Вы не запускали мониторинг! Используйте команду "
            "/help при возникновении трудностей.")

    return ConversationHandler.END
