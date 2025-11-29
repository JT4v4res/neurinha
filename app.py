import logging
import logging.handlers
import os
from handlers.commands.start import start
from handlers.commands.elegant_message import save_elegant_message
from handlers.messages.echo import echo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from settings import (
    LOGS_DIR,
    LOGS_FILENAME,
    TOKEN
)
from utils.custom_formatter import CustomFormatter


try:
    os.mkdir(LOGS_DIR)
except FileExistsError:
    print(f'"{LOGS_FILENAME}" directory already exists')

fmt = "[%(asctime)s] - [%(levelname)s] - %(message)s"

file_handler = logging.handlers.TimedRotatingFileHandler(
    "./logs/bentinho.log", when="midnight"
)
file_handler.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(CustomFormatter(fmt))

logging.basicConfig(
    format=fmt,
    style="%",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[file_handler, stdout_handler],
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)

    elegant_message_handler = CommandHandler(
        "elegant_message", save_elegant_message)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(elegant_message_handler)

    application.run_polling()
