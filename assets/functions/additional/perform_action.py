from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler


async def perform_action(update: Update, context: ContextTypes):
    action = update.message.text
    reply_keyboard = [['На главную']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if action == "Добавить":
        await update.message.reply_text(
            "Отправьте артикул отслеживаемого товара.\n"
            "ВАЖНО! Перед тем, как добавить артикул, проводится "
            "проверка артикула на валидность.",
            reply_markup=markup
        )

        return 3

    elif action == "Удалить":
        await update.message.reply_text(
            "Отправьте артикул удаляемого товара.\n",
            reply_markup=markup
        )

        return 4

    elif action == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.",
            reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    else:
        await update.message.reply_text(
            "Используйте клавиатуру для взаимодействия!")

        return 2
