from typing import List, Optional
from services.base_service import BaseService
from repository.Production_order_repository import ProductionOrderRepository
from dto.production_orders_dto import ProductionOrderDTO
from models import CostPrice
from extensions import db


class ProductionOrderService(BaseService):
    def __init__(self):
        super().__init__(ProductionOrderRepository())

    def get_all_dto(self, skip: int = 0, limit: int = 100) -> List[ProductionOrderDTO]:
        orders = self.get_all(skip, limit)
        return [ProductionOrderDTO.from_model(o) for o in orders]

    def get_by_id_dto(self, order_id: int) -> Optional[ProductionOrderDTO]:
        order = self.get_by_id(order_id)
        return ProductionOrderDTO.from_model(order) if order else None

    def calculate_cost(self, order_id: int) -> dict:
        order = self.get_by_id(order_id)
        if not order:
            return {'error': 'Заказ не найден'}

        total = 0.0
        items_detail = []

        if order.item:
            cost_price_record = db.session.execute(
                db.select(CostPrice)
                .where(CostPrice.item_id == order.item_id)
                .order_by(CostPrice.id.desc())
                .limit(1)
            ).scalar_one_or_none()

            unit_cost = float(cost_price_record.cost_price) if cost_price_record else 0.0

            items_detail.append({
                'item_id': order.item_id,
                'item_name': order.item.name,
                'quantity': 1.0,
                'unit_cost': unit_cost,
                'total_cost': unit_cost,
            })
            total += unit_cost

        return {
            'order_id': order.id,
            'order_number': order.order_number,
            'total_cost': total,
            'items': items_detail,
        }