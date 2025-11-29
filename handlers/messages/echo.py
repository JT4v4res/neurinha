from telegram import Update
from telegram.ext import ContextTypes
from utils.llm import get_model_response


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_chat_id = update.effective_chat.id

    user_first_name = update.message.from_user.first_name
    user_last_name = update.message.from_user.last_name

    username = user_first_name + " " + user_last_name

    response = await get_model_response(
        username,
        update.message.text,
        telegram_chat_id
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )
