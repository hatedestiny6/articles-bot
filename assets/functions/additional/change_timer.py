from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from assets.functions.additional.remove_job_if_exists import remove_job_if_exists


async def change_timer(update: Update, context: ContextTypes):
    if update.message.text == "На главную":
        await update.message.reply_text(
            "Вы вернулись на главную. Используйте команду "
            "/help при возникновении трудностей.",
            reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    new_value = update.message.text

    try:
        if int(new_value) < 10:
            await update.message.reply_text(
                "Введенное значение меньше 10! "
                "Введите корректное значение и попробуйте снова."
            )

            return 1

        else:
            chat_id = update.effective_message.chat_id

            job_removed = remove_job_if_exists(str(chat_id), context)
            context.user_data['timer'] = new_value

            if job_removed:
                await update.message.reply_text(
                    "Текущая проверка остановлена!"
                )

            await update.message.reply_text(
                "Значение таймера успешно изменено! "
                "Запустите проверку вновь, "
                "используя команду /startchecking.",
                reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "Некорректное значение! "
            "Проверьте правильность введенных данных и попробуйте снова."
        )

        return 1
