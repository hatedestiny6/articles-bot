from telegram import Update
from telegram.ext import ContextTypes

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep


# команда /start
async def start(update: Update, context: ContextTypes):
    try:
        if context.user_data['launched']:
            await update.message.reply_text(
                "Вы уже запускали бота! Используйте команду "
                "/help при возникновении трудностей.")

    except KeyError:
        await update.message.reply_text(
            "Производится инициализация..."
        )
        context.user_data['ozon_articles'] = {}
        context.user_data['wb_articles'] = {}
        context.user_data['timer'] = 1800
        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()))
        browser.set_window_size(800, 800)
        context.user_data['browser'] = browser
        browser.get("https://www.wildberries.ru/security/login")

        await update.message.reply_text(
            "Ожидание авторизации..."
        )

        while browser.current_url != "https://www.wildberries.ru/lk/basket":
            pass

        sleep(1)

        await update.message.reply_text(
            "Авторизация прошла успешно!"
        )
        # это нужно для того, чтобы при повторном запуске
        # команды /start артикулы не очищались
        context.user_data['launched'] = True

        await update.message.reply_text(
            "Бот успешно запущен!\n\nДля запуска проверки добавьте артикулы "
            "отслеживаемых товаров. Используйте команду "
            "/help при возникновении трудностей.")
