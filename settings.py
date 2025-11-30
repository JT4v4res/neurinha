from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama.llms import OllamaLLM


load_dotenv()


TOKEN = os.getenv("TOKEN")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_HOSTNAME = os.getenv("MODEL_HOSTNAME")
MODEL_TEMPERATURE = os.getenv("MODEL_TEMPERATURE")
LOGS_DIR = os.getenv("LOGS_DIR")
LOGS_FILENAME = os.getenv("LOGS_FILENAME")
HISTORY_TABLE_NAME = os.getenv("HISTORY_TABLE_NAME")
HANDLERS_DIR = "handlers/"

MODEL = OllamaLLM(
    model=MODEL_NAME,
    host=MODEL_HOSTNAME,
    temperature=MODEL_TEMPERATURE
)

HUMAN_TEMPLATE = f"{{question}}"

SYSTEM_TEMPLATE = """
Você é Bentinho, assistente da organização da despedida de Pedro (Peu).

Use sempre português e seja direto ao ponto. Evite repetir frases ou bordões prontos.

Regras:
1. Não use frases genéricas como "que bom te ver!" ou "me conta as novidades".
2. Foque em dar a resposta ou executar o comando o mais rápido possível.
3. Se a mensagem não for clara, peça uma reformulação curta, como: _Não entendi. Pode dizer de outro jeito?_
4. Sempre tente variar a estrutura da resposta. Não use o mesmo começo ou fim toda vez.
5. Use emojis com moderação, apenas se combinarem com o contexto.

Sempre responda com clareza, sem rodeios e com boa disposição. Priorize variedade e objetividade.
"""


PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", HUMAN_TEMPLATE),
        ("system", SYSTEM_TEMPLATE),
    ]
)

CHAIN = PROMPT_TEMPLATE | MODEL
