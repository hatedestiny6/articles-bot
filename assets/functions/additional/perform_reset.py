from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler


async def perform_reset(update: Update, context: ContextTypes):
    if update.message.text == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.",
            reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    platform = update.message.text

    if platform == "OZON":
        context.user_data['ozon_articles'] = {}

    elif platform == "Wildberries":
        context.user_data['wb_articles'] = {}

    elif platform == "Все":
        context.user_data['ozon_articles'] = {}
        context.user_data['wb_articles'] = {}

    else:
        await update.message.reply_text(
            "Используйте клавиатуру для взаимодействия!")

        return 1

    await update.message.reply_text(
        "Артикулы успешно сброшены!")

    return ConversationHandler.END
