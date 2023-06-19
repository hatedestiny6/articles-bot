from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler


async def del_user_article(update: Update, context: ContextTypes):
    if update.message.text == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.",
            reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    article = update.message.text
    reply_keyboard = [['На главную']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if context.user_data['cur_platform'] == 'OZON':
        # если артикула нет в списке
        if article not in list(context.user_data['ozon_articles'].keys()):
            await update.message.reply_text(
                f"Вы не добавляли этот артикул "
                f"в список артикулов {context.user_data['cur_platform']}! "
                "Проверьте правильность введённых данных и попробуйте снова.",
                reply_markup=markup
            )

            return 4

        else:
            del context.user_data['ozon_articles'][article]

            await update.message.reply_text(
                f"OZON артикул {article} успешно удален!"
            )

    elif context.user_data['cur_platform'] == 'Wildberries':
        # если артикула нет в списке
        if article not in list(context.user_data['wb_articles'].keys()):
            await update.message.reply_text(
                f"Вы не добавляли этот артикул "
                f"в список артикулов {context.user_data['cur_platform']}!"
                "Проверьте правильность введённых данных и попробуйте снова.",
                reply_markup=markup
            )

            return 4

        else:
            del context.user_data['wb_articles'][article]

            await update.message.reply_text(
                f"Wildberries артикул {article} успешно удален!"
            )

    else:
        await update.message.reply_text(
            "Используйте клавиатуру для взаимодействия!")

        return 4

    return ConversationHandler.END
