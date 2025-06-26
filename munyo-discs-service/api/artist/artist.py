from dataclasses import dataclass
import uuid


@dataclass
class Artist:
    artist_id: uuid.UUID
    name: str
