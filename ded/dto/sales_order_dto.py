from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class SalesOrderItemDTO:
    sales_order_item_id: int
    item_id: int
    quantity: float
    unit_price: float
    discount: float = 0.0

    @classmethod
    def from_model(cls, item) -> "SalesOrderItemDTO":
        return cls(
            sales_order_item_id=item.id,
            item_id=item.item_id,
            quantity=float(item.quantity),
            unit_price=float(item.unit_price),
            discount=float(item.discount) if item.discount else 0.0,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SalesOrderDTO:
    sales_order_id: int
    order_number: str
    order_date: Optional[str] = None
    countreparties_id: Optional[int] = None
    executor_id: Optional[int] = None
    total_amount: float = 0.0
    created_at: Optional[str] = None
    items: Optional[List[SalesOrderItemDTO]] = None

    @classmethod
    def from_model(cls, order) -> "SalesOrderDTO":
        items = [SalesOrderItemDTO.from_model(i) for i in order.items] if order.items else None
        return cls(
            sales_order_id=order.id,
            order_number=order.order_number,
            order_date=order.order_date.isoformat() if order.order_date else None,
            countreparties_id=order.countreparties_id,
            executor_id=order.executor_id,
            total_amount=float(order.total_amount) if order.total_amount else 0.0,
            created_at=order.created_at.isoformat() if order.created_at else None,
            items=items,
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        return data