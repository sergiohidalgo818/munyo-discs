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


@dataclass
class BaseOwnedCdRequest:
    disc: str
    artist: str


@dataclass
class BaseWishedCdRequest:
    artist: str
    disc: str
    stars: int


@dataclass
class ModifyOwnedCdRequest:
    artist: str
    disc: str
    new_artist: str
    new_disc: str


@dataclass
class ModifyWishedCdRequest:
    artist: str
    disc: str
    new_artist: str
    new_disc: str
    stars: int = 0
