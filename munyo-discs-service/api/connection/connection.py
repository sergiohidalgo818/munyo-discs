from dataclasses import dataclass
import uuid


@dataclass
class Connection:
    name: str
    icon_url: str
    connection_id: uuid.UUID = uuid.uuid4()
