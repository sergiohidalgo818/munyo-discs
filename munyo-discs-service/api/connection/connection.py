from dataclasses import dataclass
import uuid


@dataclass
class Connection:
    connection_id: uuid.UUID
    name: str
    icon_url: str
