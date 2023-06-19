from telegram import Update
from telegram.ext import ContextTypes


async def inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    ans = query.data.split(',')

    if ans == ["None"]:
        await query.edit_message_text(text="Вы отменили добавление артикула.")

    else:
        context.user_data[ans[1]][ans[0]] = ans[2]
        await query.edit_message_text(text=f"Артикул {ans[0]} успешно добавлен!")
