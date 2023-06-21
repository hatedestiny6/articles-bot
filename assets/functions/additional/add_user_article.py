from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from assets.functions.checking.check_ozon import check_ozon
from assets.functions.checking.check_wb import check_wb

from assets.functions.parsing.parse_ozon import parse_ozon
from assets.functions.parsing.parse_wb import parse_wb


async def add_user_article(update: Update, context: ContextTypes):
    if update.message.text == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.",
            reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    article = update.message.text
    reply_keyboard = [['На главную']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    # уведомим пользователя что бот работает
    # потому что делаем запрос к веб странице
    # и бот "подвисает", ожидвя ответа
    await update.message.reply_text("Идет проверка артикула...")

    if context.user_data['cur_platform'] == 'OZON':
        price = check_ozon(article)
        # если некорректный формат артикула
        if not price:
            await update.message.reply_text(
                "Некорректный артикул! "
                "Пожалуйста, проверьте правильность введённых данных и попробуйте снова.",
                reply_markup=markup)

            return 3

        await update.message.reply_text("Проверка прошла успешно! "
                                        "Собираю информацию о товаре...")

        brand, name, discount, ozon_card = parse_ozon(article)

        message = f"<b>Информация о товаре:</b>\n"\
            f"• <b>Артикул:</b> {article}\n"\
            f"• <b>Бренд:</b> {brand}\n"\
            f"• <b>Наименование:</b> {name}\n"

        if discount:
            message += f"• <b>Скидка:</b> {discount}\n"
            message += f"• <b>Цена со скидкой:</b> {price}\n\n"

        else:
            message += f"• <b>Цена:</b> {price}\n\n"

        try:
            if "при оплате Ozon Картой" in ozon_card:
                message += "✅<b>Ozon Карта применяется</b>\n"
                message += f"• {ozon_card}"

            else:
                message += "❌<b>Ozon Карта не применяется</b>\n"

        except TypeError:
            message += "❌<b>Ozon Карта не применяется</b>\n"

        keyboard = [[InlineKeyboardButton("Добавить",
                                          callback_data=f"{article},ozon_articles,{price}")],
                    [InlineKeyboardButton("Отмена",
                                          callback_data='None')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message,
                                        parse_mode="HTML",
                                        reply_markup=reply_markup)
        # await update.message.reply_text(
        #     f"OZON артикул {article} успешно добавлен!"
        # )

    elif context.user_data['cur_platform'] == 'Wildberries':
        res = check_wb(article, context.user_data['browser'])
        # если некорректный формат артикула
        if not res:
            await update.message.reply_text(
                "Некорректный артикул! "
                "Пожалуйста, проверьте правильность введённых данных и попробуйте снова.",
                reply_markup=markup)

            return 3

        elif res == "TIMEOUT":
            await update.message.reply_text(
                "Превышено время ожидания! "
                "Пожалуйста, проверьте ваше интернет-соединение и попробуйте снова.",
                reply_markup=markup)

            return 3

        await update.message.reply_text("Проверка прошла успешно! "
                                        "Собираю информацию о товаре...")

        brand, name, discs, old_price = parse_wb(
            context.user_data['browser'])

        message = f"<b>Информация о товаре:</b>\n"\
            f"• <b>Артикул:</b> {article}\n"\
            f"• <b>Бренд:</b> {brand}\n"\
            f"• <b>Наименование:</b> {name}\n"

        if not discs:
            message += f"• <b>Цена:</b> {res}\n\n"

        elif len(discs) == 1:
            key, value = list(discs.items())[0]

            if 'покупателя' in key:
                message += f"• <b>Цена:</b> {old_price}₽\n\n"
                message += "<b>✅ СПП применяется</b>\n"
                message += f"• <b>СПП:</b> {key.split()[-1]}%\n"
                message += f"• <b>Цена с учетом СПП:</b> {value.strip()}₽\n"

            else:
                message += f"• <b>Скидка:</b> {key.split()[-1]}%\n"
                message += f"• <b>Цена со скидкой:</b> {value.strip()}₽\n\n"

        else:
            for discount, d_price in discs.items():
                if "покупателя" in discount:
                    # message += f"• <b>Цена:</b> {old_price}₽\n\n"
                    message += "<b>✅ СПП применяется</b>\n"
                    message += f"• <b>СПП:</b> {discount.split()[-1]}%\n"
                    message += f"• <b>Цена с учетом СПП:</b> {d_price.strip()}₽\n"

                else:
                    message += f"• <b>Скидка:</b> {discount.split()[-1]}%\n"
                    message += f"• <b>Цена со скидкой:</b> {d_price.strip()}₽\n\n"

        if "СПП" not in message:
            message += "<b>❌ СПП не применяется</b>"

        res = ''.join(res.split()[:-1])

        keyboard = [[InlineKeyboardButton("Добавить",
                                          callback_data=f"{article},wb_articles,{res}")],
                    [InlineKeyboardButton("Отмена",
                                          callback_data='None')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message,
                                        parse_mode="HTML",
                                        reply_markup=reply_markup)

    else:
        await update.message.reply_text(
            "Используйте клавиатуру для взаимодействия!")

        return 3

    return ConversationHandler.END
