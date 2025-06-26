from dataclasses import dataclass
import uuid


@dataclass
class Disc:
    disc_id: uuid.UUID
    artist_id: uuid.UUID
    name: str


@dataclass
class DiscValoration:
    disc_id: uuid.UUID
    valoration: int
