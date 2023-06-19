from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler


async def on_main(update: Update, context: ContextTypes):
    await update.message.reply_text(
        "Вы вернулись на главную. Используйте команду "
        "/help при возникновении трудностей.",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
