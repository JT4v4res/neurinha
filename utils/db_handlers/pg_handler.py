from settings import (
    PG_DATABASE,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
    HISTORY_TABLE_NAME
)
import psycopg
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_postgres import PostgresChatMessageHistory


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    sync_connection = psycopg.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
    )

    return PostgresChatMessageHistory(
        HISTORY_TABLE_NAME, session_id, sync_connection=sync_connection
    )


def insert_elegant_message(message_author: str, message: str):
    conn = psycopg.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
    )
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO elegant_messages (message_author, message, created_at)
            VALUES (%s, %s, current_timestamp)
        """,
            (message_author, message),
        )
        conn.commit()
    conn.close()
