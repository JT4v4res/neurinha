# TODO:
# 1. QRCODE Authentication needs to be implemented
# 2. Connection to the Quiz Server needs to be done
# 3. Creation of the handler for the votation in quizzes
# 4. Creation of a platform/frontend for quiz creation
# and quiz playing
# 5. Creation of the command for draw the secret friend
import logging
import logging.handlers
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from settings import LOGS_DIR, LOGS_FILENAME, HANDLERS_DIR, TOKEN
from utils.custom_formatter import CustomFormatter
from utils.load_handlers import recursive_handler_loader


try:
    os.mkdir(LOGS_DIR)
except FileExistsError:
    print(f'"{LOGS_FILENAME}" directory already exists')

logging.getLogger("httpx").setLevel(logging.WARNING)

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

    found_handlers = recursive_handler_loader(HANDLERS_DIR)

    for handler in found_handlers:
        if handler.get("handler_type", "").lower() == "commands":
            application.add_handler(
                CommandHandler(handler.get("name", ""), handler.get("func_inst", None))
            )
            continue

        elif handler.get("handler_type", "").lower() == "messages":
            application.add_handler(
                MessageHandler(
                    filters.TEXT & (~filters.COMMAND), handler.get("func_inst", None)
                )
            )
            continue

    application.run_polling()
