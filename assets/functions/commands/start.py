from telegram import Update
from telegram.ext import ContextTypes


# команда /start
async def start(update: Update, context: ContextTypes):
    try:
        if context.user_data['launched']:
            pass

    except KeyError:
        context.user_data['ozon_articles'] = {}
        context.user_data['wb_articles'] = {}
        context.user_data['timer'] = 1800
        # это нужно для того, чтобы при повторном запуске
        # команды /start артикулы не очищались
        context.user_data['launched'] = True

    await update.message.reply_text(
        "Бот успешно запущен!\n\nДля запуска проверки добавьте артикулы "
        "отслеживаемых товаров. Используйте команду "
        "/help при возникновении трудностей.")
