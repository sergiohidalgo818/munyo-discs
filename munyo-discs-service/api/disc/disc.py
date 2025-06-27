from dataclasses import dataclass
import uuid


@dataclass
class Disc:
    name: str
    artist_id: uuid.UUID
    disc_id: uuid.UUID = uuid.uuid4()


@dataclass
class DiscValoration:
    valoration: int
    disc_id: uuid.UUID = uuid.uuid4()
