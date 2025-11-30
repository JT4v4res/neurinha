from dataclasses import dataclass
import socket


@dataclass
class Connection:
    conn: socket.socket = None
    addr = None
    open: bool = False
