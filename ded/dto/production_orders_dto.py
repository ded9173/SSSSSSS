from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ProductionOrderDTO:
    order_id: int
    order_number: str
    order_date: Optional[str]
    subdivision: str = ""
    status: str = "Новый"
    item_id: Optional[int] = None
    created_at: Optional[str] = None

    @classmethod
    def from_model(cls, order) -> "ProductionOrderDTO":
        return cls(
            order_id=order.id,
            order_number=order.order_number,
            order_date=order.order_date.isoformat() if order.order_date else None,
            subdivision=order.subdivision or "",
            status=order.status or "Новый",
            item_id=order.item_id,
            created_at=order.created_at.isoformat() if order.created_at else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)