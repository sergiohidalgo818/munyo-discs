from dataclasses import dataclass
import uuid


@dataclass
class Playlist:
    name: str
    playlist_id: uuid.UUID = uuid.uuid4()
