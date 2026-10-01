from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ItemsDTO:
    item_id: int
    name: str
    code: str
    item_type: str
    created_at: Optional[str] = None

    @classmethod
    def from_model(cls, item) -> "ItemsDTO":
        return cls(
            item_id=item.id,
            name=item.name,
            code=item.code,
            item_type=item.item_type,
            created_at=item.created_at.isoformat() if item.created_at else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)