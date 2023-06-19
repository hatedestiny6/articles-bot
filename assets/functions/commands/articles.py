from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


# команда /articles
async def articles(update: Update, context: ContextTypes):
    ozon_articles = ', '.join(context.user_data['ozon_articles'])
    wb_articles = ', '.join(context.user_data['wb_articles'])

    reply_keyboard = [['OZON', 'Wildberries'],
                      ['На главную']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Текущие просматриваемые товары:\n"
        f"OZON: {ozon_articles if ozon_articles else 'Не задано!'}\n"
        f"Wildberries: {wb_articles if wb_articles else 'Не задано!'}\n\n"
        "Используйте клавиатуру для управления артикулами товаров.",
        reply_markup=markup
    )

    return 1
