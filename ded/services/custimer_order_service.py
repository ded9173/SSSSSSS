from typing import List, Optional
from services.base_service import BaseService
from repository.countreparties_order_repository import CountrepartiesOrderRepository
from dto.sales_order_dto import SalesOrderDTO
from models import CustomerOrder, CustomerOrderItem, CostPrice
from extensions import db

class CustomerOrderService(BaseService):
    def __init__(self):
        super().__init__(CountrepartiesOrderRepository())

    def get_all_dto(self) -> List[SalesOrderDTO]:
        orders = self.get_all()
        return [SalesOrderDTO.from_model(o) for o in orders]

    def get_by_id_dto(self, order_id: int) -> Optional[SalesOrderDTO]:
        order = self.get_by_id(order_id)
        return SalesOrderDTO.from_model(order) if order else None

    def calculate_cost(self, order_id: int) -> dict:
        order = self.get_by_id(order_id)
        if not order:
            return {'error': 'Заказ не найден'}

        total = 0.0
        items_detail = []

        for item in order.items:
            # Ищем себестоимость для товара
            cost_price_record = db.session.execute(
                db.select(CostPrice)
                .where(CostPrice.item_id == item.item_id)
                .order_by(CostPrice.id.desc())
                .limit(1)
            ).scalar_one_or_none()

            unit_price = float(item.unit_price) if item.unit_price else (
                float(cost_price_record.cost_price) if cost_price_record else 0.0
            )
            discount = float(item.discount) if item.discount else 0.0
            quantity = float(item.quantity)

            item_total = (unit_price * quantity) - discount
            total += item_total

            items_detail.append({
                'id': item.id,
                'item_id': item.item_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount': discount,
                'cost_price': float(cost_price_record.cost_price) if cost_price_record else 0.0,
                'total': item_total
            })

        return {
            'order_id': order.id,
            'order_number': order.order_number,
            'total_amount': total,
            'items': items_detail
        }