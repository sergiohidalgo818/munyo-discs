from dataclasses import dataclass
import uuid


@dataclass
class Spotify:
    client_id: str
    client_secret: str
    connection_id: uuid.UUID
