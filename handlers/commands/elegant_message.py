from telegram import Update
from telegram.ext import ContextTypes
import logging
from utils.llm import get_model_response
import traceback
from utils.db_handlers.pg_handler import insert_elegant_message


async def save_elegant_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_chat_id = update.effective_chat.id

    user_first_name = update.message.from_user.first_name
    user_last_name = update.message.from_user.last_name

    username = (
        f"{user_first_name or ''} {user_last_name or ''}".strip()
        or user_first_name
        or "Unknown"
    )

    message = " ".join(context.args)

    logging.info(
        f"""
        Inserting new message {message} from user {username} in database
        """)

    try:
        insert_elegant_message(username, message)

        logging.info(
            f"""
            Successfully inserted message {message} from user {username} in database
            """
        )
    except Exception as e:
        logging.error(
            f"""
            Failed to insert message on database: {traceback.format_exc()}
            """)

    model_query = f"""
        Agradeça ao usuário por ter enviado a seguinte mensagem: {message}
        """

    response = await get_model_response(username, model_query, telegram_chat_id)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
