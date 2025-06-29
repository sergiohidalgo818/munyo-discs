from dataclasses import dataclass
import uuid


@dataclass
class Artist:
    name: str
    artist_id: uuid.UUID = uuid.uuid4()
