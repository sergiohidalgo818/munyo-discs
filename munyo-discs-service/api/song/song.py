from dataclasses import dataclass
import uuid


@dataclass
class Song:
    name: str
    artist_id: uuid.UUID
    disc_id: uuid.UUID
    song_id: uuid.UUID = uuid.uuid4()
