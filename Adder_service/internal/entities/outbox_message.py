from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json

@dataclass
class Outbox:
    payload: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "NONPROCESSED"
    sent_at: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    json_message: str = field(init=False)

    def __post_init__(self):
        self.json_message = json.dumps({
            "id": self.id,
            "payload": self.payload,
            "status": self.status,
            "created_at": self.created_at.isoformat() + "Z",
            "sent_at": self.sent_at.isoformat() + "Z"
        })
