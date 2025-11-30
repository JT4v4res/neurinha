from settings import (
    PG_DATABASE,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
    HISTORY_TABLE_NAME,
)
import psycopg
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_postgres import PostgresChatMessageHistory
import uuid
import traceback
import logging


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


def create_session(session_id: uuid._uuid):
    conn = psycopg.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sessions (session_id, is_active, created_at)
                VALUES (%s, %s, current_timestamp)
                """,
                (session_id, True),
            )
            conn.commit()

            logging.info(
                f"""
                Sucessfully created new session with session_id: {session_id}
                """
            )
            created_session = True
    except (psycopg.errors.DatabaseError,):
        logging.error(
            f"""
            Failure to create new session: {traceback.format_exc()}
            """
        )
        created_session = False

    return (
        "Session created"
        if created_session
        else "Unable to create session, check the logs"
    )


def get_all_sessions() -> list[str]:
    fmtd_response = []

    conn = psycopg.connect(
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM sessions;
                """
            )

            rows = cur.fetchall()

            for row in rows:
                fmtd_response.append(
                    {"session_id": row[1], "is_active": row[2], "created_at": row[-1]}
                )

            logging.info(
                f"""
            found {len(rows)}
            """
            )
    except (psycopg.errors.DatabaseError):
        logging.error(
            f"""
            Failure to fetch rows: {traceback.format_exc()}
            """
        )

        rows = None

    return fmtd_response
