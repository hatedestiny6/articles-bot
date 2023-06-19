from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def resetarticles(update: Update, context: ContextTypes):
    reply_keyboard = [['OZON', 'Wildberries', 'Все'],
                      ['На главную']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Артикулы какой площадки вы хотите сбросить?\n\n"
        "Используйте клавиатуру для взаимодействия.",
        reply_markup=markup
    )

    return 1
