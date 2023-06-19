import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler, CallbackQueryHandler

from assets.functions.commands.articles import articles
from assets.functions.commands.help import help_cmd
from assets.functions.commands.resetarticles import resetarticles
from assets.functions.commands.start import start
from assets.functions.commands.stop_checking import stopchecking
from assets.functions.commands.timer import timer

from assets.functions.additional.add_user_article import add_user_article
from assets.functions.additional.change_timer import change_timer
from assets.functions.additional.choose_platform import choose_platform
from assets.functions.additional.del_user_article import del_user_article
from assets.functions.additional.on_main import on_main
from assets.functions.additional.perform_action import perform_action
from assets.functions.additional.perform_reset import perform_reset
from assets.functions.additional.inline_button import inline_button

from assets.functions.checking.check_ozon import check_ozon
from assets.functions.checking.check_wb import check_wb

from config import BOT_TOKEN


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start_checking(update: Update, context: ContextTypes):
    if not context.user_data['ozon_articles'] \
            and not context.user_data['wb_articles']:
        await update.message.reply_text(
            "Для запуска проверки добавьте артикулы "
            "отслеживаемых товаров. Используйте команду "
            "/help при возникновении трудностей.")

    else:
        chat_id = update.effective_message.chat_id
        context.job_queue.run_repeating(task, interval=int(context.user_data['timer']), chat_id=chat_id,
                                        name=str(chat_id), data=context.user_data)

        await update.message.reply_text(
            "Проверка запущена! Используйте команду "
            "/help при возникновении трудностей.")


async def task(context: ContextTypes):
    """Проверяет изменение цены"""
    # сначала проверяем OZON
    for article in list(context.job.data['ozon_articles'].keys()):
        last_price = context.job.data['ozon_articles'][article]
        cur_price = check_ozon(article)

        if not last_price:
            context.job.data['ozon_articles'][article] = cur_price

        elif cur_price != last_price:
            await context.bot.send_message(context.job.chat_id,
                                           f"В магазине OZON у товара с артикулом {article} "
                                           f"сменилась стоимость с {last_price} на {cur_price}!"
                                           )

            context.job.data['ozon_articles'][article] = cur_price

    # теперь проверяем Wildberries
    for article in list(context.job.data['wb_articles'].keys()):
        last_price = context.job.data['wb_articles'][article]
        cur_price = check_wb(article)

        if not last_price:
            context.job.data['wb_articles'][article] = cur_price

        elif cur_price != last_price:
            await context.bot.send_message(context.job.chat_id,
                                           f"В магазине Wildberries у товара с артикулом {article} "
                                           f"сменилась стоимость с {last_price} на {cur_price}!"
                                           )

            context.job.data['wb_articles'][article] = cur_price


def main():
    # Создаём объект Application.
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('articles', articles)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(filters.Text(['OZON', 'Wildberries']),
                               choose_platform)],
            2: [MessageHandler(filters.Text(['Добавить', 'Удалить']),
                               perform_action)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_user_article)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, del_user_article)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[MessageHandler(filters.Text(['На главную']),
                                  on_main)]
    )

    # сброс артикулов
    resetarticles_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('resetarticles', resetarticles)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(filters.Text(["OZON", "Wildberries", "Все"]),
                               perform_reset)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[MessageHandler(filters.Text(['На главную']), on_main)]
    )

    # смена значения таймера
    timer_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('timer', timer)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_timer)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[MessageHandler(filters.Text(['На главную']), on_main)]
    )

    application.add_handler(conv_handler)
    application.add_handler(resetarticles_handler)
    application.add_handler(timer_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("startchecking", start_checking))
    application.add_handler(CommandHandler("stopchecking", stopchecking))
    application.add_handler(CommandHandler("stopchecking", stopchecking))

    application.add_handler(CallbackQueryHandler(inline_button))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
