from dataclasses import dataclass


@dataclass
class DataPacket:
    username: str = ""
    current_session: str = ""
    vote = None
