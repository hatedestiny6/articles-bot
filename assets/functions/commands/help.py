from telegram import Update
from telegram.ext import ContextTypes


# команда /help
async def help_cmd(update: Update, context: ContextTypes):
    await update.message.reply_text(
        "Справка по использованию бота:\n"
        "/articles - управление артикулами отслеживаемых товаров\n"
        "/startchecking - запустить мониторинг отслеживаемых товаров\n"
        "/resetarticles - сбросить артикулы\n"
        "/timer - изменить значение таймера\n"
        "/stopchecking - остановить мониторинг отслеживаемых товаров."
    )
