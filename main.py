import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def check_ozon(article_num):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на ozon.ru

    Args:
        article_num (str): артикул товара
    """

    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    browser.minimize_window()

    browser.get(f"https://www.ozon.ru/product/{article_num}")
    try:
        price = browser.find_element(
            By.CLASS_NAME, "kx6").text

    except NoSuchElementException:
        price = False

    browser.close()
    return price


def check_wb(article_num):
    """Вытаскивает цену из карточки товара с
        артикулом article_num на wildberries.ru

    Args:
        article_num (str): артикул товара
    """

    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    browser.minimize_window()

    browser.get(
        f"https://www.wildberries.ru/catalog/{article_num}/detail.aspx")

    try:
        # ждем, пока страница прогрузится
        price = WebDriverWait(browser, timeout=5).until(
            lambda brows: brows.find_element(By.CLASS_NAME, "price-block__final-price").text)
        # может произойти такое, что страница полностью
        # загрузилась, но когда артикул неверный
        # на странице написано о том, что
        # что то пошло не так. а ведь
        # WebDriverWait ждет появления элемента (цены)
        # на странице. поэтому после окончания таймаута
        # мы еще раз проверяем, что на странице нет того
        # самого элемента (цены)
        price = browser.find_element(
            By.CLASS_NAME, "price-block__final-price").text

    except NoSuchElementException:
        price = False

    except TimeoutException:
        try:
            browser.find_element(
                By.CLASS_NAME, "error500__title")
            price = False

        except NoSuchElementException:
            price = "TIMEOUT"

    browser.close()
    return price


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# команда /start
async def start(update: Update, context: ContextTypes):
    try:
        if context.user_data['launched']:
            pass

    except KeyError:
        context.user_data['ozon_articles'] = {}
        context.user_data['wb_articles'] = {}
        # это нужно для того, чтобы при повторном запуске
        # команды /start артикулы не очищались
        context.user_data['launched'] = True

    await update.message.reply_text(
        "Бот успешно запущен!\n\nДля запуска проверки добавьте артикулы "
        "отслеживаемых товаров. Используйте команду "
        "/help при возникновении трудностей.")


async def start_checking(update: Update, context: ContextTypes):
    if not context.user_data['ozon_articles'] \
            and not context.user_data['wb_articles']:
        await update.message.reply_text(
            "Для запуска проверки добавьте артикулы "
            "отслеживаемых товаров. Используйте команду "
            "/help при возникновении трудностей.")

    else:
        chat_id = update.effective_message.chat_id
        context.job_queue.run_repeating(task, interval=TIMER, chat_id=chat_id,
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


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False

    for job in current_jobs:
        job.schedule_removal()

    return True


# команда /help
async def help_cmd(update: Update, context: ContextTypes):
    await update.message.reply_text(
        "Справка по использованию бота:\n"
        "/articles - управление артикулами отслеживаемых товаров\n"
        "/startchecking - запустить проверку отслеживаемых товаров\n"
        "/resetarticles - сбросить все артикулы\n"
        "/stop - остановить работу бота."
    )


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
        # если некорректный формат артикула
        if not check_ozon(article):
            await update.message.reply_text(
                "Некорректный артикул! "
                "Пожалуйста, проверьте правильность введённых данных и попробуйте снова.",
                reply_markup=markup)

            return 3

        context.user_data['ozon_articles'][article] = ''

        await update.message.reply_text(
            f"OZON артикул {article} успешно добавлен!"
        )

    elif context.user_data['cur_platform'] == 'Wildberries':
        res = check_wb(article)
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

        context.user_data['wb_articles'][article] = ''

        await update.message.reply_text(
            f"Wildberries артикул {article} успешно добавлен!"
        )

    else:
        await update.message.reply_text(
            "Используйте клавиатуру для взаимодействия!")

        return 3

    return ConversationHandler.END


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
                f"Вы не добавляли этот артикул"
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
                f"Вы не добавляли этот артикул"
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


async def perform_reset(update: Update, context: ContextTypes):
    if update.message.text == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.",
            reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    platform = update.message.text

    if platform == "OZON":
        context.user_data['ozon_articles'] = {}

    elif platform == "Wildberries":
        context.user_data['wb_articles'] = {}

    elif platform == "Все":
        context.user_data['ozon_articles'] = {}
        context.user_data['wb_articles'] = {}

    else:
        await update.message.reply_text(
            "Используйте клавиатуру для взаимодействия!")

        return 1

    await update.message.reply_text(
        "Артикулы успешно сброшены!")

    return ConversationHandler.END


async def stop(update: Update, context: ContextTypes):
    chat_id = update.effective_message.chat_id

    job_removed = remove_job_if_exists(str(chat_id), context)

    if job_removed:
        await update.message.reply_text(
            "Проверка остановлена! Используйте команду "
            "/help при возникновении трудностей.")
    else:
        await update.message.reply_text(
            "Вы не запускали проверку! Используйте команду "
            "/help при возникновении трудностей.")

    return ConversationHandler.END


def main():
    # Создаём объект Application.
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('articles', articles)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_platform)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_action)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_user_article)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, del_user_article)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    # сброс артикулов
    resetarticles_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('resetarticles', resetarticles)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_reset)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(resetarticles_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("startchecking", start_checking))
    application.add_handler(CommandHandler("stop", stop))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    BOT_TOKEN = "6064533705:AAFy_PObiHjdS1hpWy93BYAM8UtmdO8uCzg"
    TIMER = 1800  # в секундах

    main()
