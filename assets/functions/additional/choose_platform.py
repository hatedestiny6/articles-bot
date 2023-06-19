from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


# обработчик ситуации когда пользователь
# выбирает ozon или wb
async def choose_platform(update: Update, context: ContextTypes):
    if update.message.text == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.")

        return ConversationHandler.END

    context.user_data['cur_platform'] = update.message.text

    reply_keyboard = [['Добавить', 'Удалить'],
                      ['На главную']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Что вы хотите сделать?\n\n"
        "Используйте клавиатуру для взаимодействия.",
        reply_markup=markup)

    return 2
