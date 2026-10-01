import uuid
from datetime import date
from flask import request, Blueprint
from views.base_view import BaseAPIView
from services.customer_order_service import CustomerOrderService
from models import CustomerOrder, CustomerOrderItem
from extensions import db

countreparties_orders_bp = Blueprint("countreparties_orders", __name__)

class CountrepartiesOrderListAPI(BaseAPIView):
    def __init__(self):
        self.service = CustomerOrderService()

    def get(self):
        orders = self.service.get_all_dto()
        return self._success_response({"countreparties_orders": [o.to_dict() for o in orders]})

    def post(self):
        data = request.get_json()
        required_fields = ["order_number", "order_date", "countreparties_id", "executor_id"]
        if not data or not all(field in data for field in required_fields):
            return self._error_response("Укажите order_number, order_date, countreparties_id, executor_id")

        od = data["order_date"]
        order_date = date.fromisoformat(od) if isinstance(od, str) else od

        new_order = CustomerOrder(
            order_number=data["order_number"], order_date=order_date,
            countreparties_id=data["countreparties_id"], executor_id=data["executor_id"]
        )
        db.session.add(new_order)
        db.session.commit()

        if "items" in data:
            for item_data in data["items"]:
                item = CustomerOrderItem(
                    customer_order_id=new_order.id,
                    item_id=item_data["item_id"],
                    quantity=item_data.get("quantity", 1),
                    unit_price=item_data.get("unit_price", 0),
                    discount=item_data.get("discount", 0)
                )
                db.session.add(item)
        db.session.commit()

        return self._success_response({"message": "Заказ создан", "countreparties_order_id": new_order.id}, 201)

class CountrepartiesOrderDetailAPI(BaseAPIView):
    def __init__(self):
        self.service = CustomerOrderService()

    def get(self, order_id):
        order = self.service.get_by_id(order_id)
        if not order:
            return self._not_found_response("Заказ")

        items = []
        for i in order.items:
            items.append({
                "countreparties_order_item_id": i.id,
                "item_id": i.item_id,
                "quantity": float(i.quantity),
                "unit_price": float(i.unit_price),
                "discount": float(i.discount),
            })

        return self._success_response({
            "countreparties_order_id": order.id,
            "order_number": order.order_number,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "countreparties_id": order.countreparties_id,
            "executor_id": order.executor_id,
            "total_amount": float(order.total_amount) if order.total_amount else 0,
            "items": items,
        })

class CountrepartiesOrderCostCalculationAPI(BaseAPIView):
    def __init__(self):
        self.service = CustomerOrderService()

    def get(self, order_id):
        order = self.service.get_by_id(order_id)
        if not order:
            return self._not_found_response("Заказ")
        result = self.service.calculate_cost(order_id)
        return self._success_response(result)

countreparties_orders_bp.add_url_rule("/", view_func=CountrepartiesOrderListAPI.as_view("Countreparties_orders_list"))
countreparties_orders_bp.add_url_rule("/<int:order_id>", view_func=CountrepartiesOrderDetailAPI.as_view("countreparties_order_detail"))
countreparties_orders_bp.add_url_rule(
    "/<int:order_id>/cost-calculation",
    view_func=CountrepartiesOrderCostCalculationAPI.as_view("countreparties_order_cost")
)