from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def timer(update: Update, context: ContextTypes):
    await update.message.reply_text(
        f"Текущее значение таймера - {context.user_data['timer']} секунд.\n\n"
        "Для изменения введите новое значение таймера В СЕКУНДАХ! "
        "Значение не должно быть меньше 10!\n\n"
        "При необходимости используйте клавиатуру.",
        reply_markup=ReplyKeyboardMarkup([["На главную"]])
    )

    return 1
