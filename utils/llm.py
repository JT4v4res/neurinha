import logging
import uuid
import traceback
from langchain_core.runnables.history import RunnableWithMessageHistory
from settings import CHAIN
from utils.db_handlers.pg_handler import get_by_session_id


async def get_model_response(
    user_first_name: str, user_question: str, telegram_chat_id: int
) -> str:
    logging.info(f"User: {user_first_name} asked: {user_question}")

    try:
        chain_with_history = RunnableWithMessageHistory(
            CHAIN,
            get_by_session_id,
            input_messages_key="question",
            history_messages_key="history",
        )

        session_id = str(uuid.UUID(int=telegram_chat_id))

        result = chain_with_history.invoke(
            {"question": user_question},
            config={"configurable": {"session_id": session_id}},
        )

        logging.info(f'Model response: {result.replace("AI:", "")}')

        return result.replace("AI:", "")
    except Exception:
        logging.error(
            f"""
                Error while generating reponse: {traceback.format_exc()}
            """
        )

        return chain_with_history.invoke(
            {
                "size": "concise",
                "question": "gere uma mensagem de desculpas informando que você não pode responder a essa questão.",
            },
            config={"configurable": {"session_id": session_id}},
        ).replace("AI:", "")
