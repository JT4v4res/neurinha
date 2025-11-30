import socket
from settings import SERVER_HOST, SERVER_PORT
from classes.connection import Connection


# NOTE:
# The DataPacket class needs to be import in
# order to be used to help on data exchanging
# mechanisms that may be implemented soon
# TODO:
# 1. Create the authentication logic
# 2. Create the active sessions handling
# 3. Create the server logger
# 4. Create the message transmission logic
def handle_connection(conn: Connection) -> None:
    # TODO: Implement the logic for handling
    # and managing the current connections
    # to share the messages between
    # votation interface and the bot
    while conn.open:
        pass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(1)

    new_conn = Connection()
    new_conn.conn, new_conn.addr, new_conn.open = *(s.accept()), True

    with new_conn.conn as conn:
        print("Connected by", new_conn.addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            conn.sendall(data)
