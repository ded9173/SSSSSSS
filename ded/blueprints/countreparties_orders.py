from datetime import date
from flask import Blueprint, request, jsonify
from models import CustomerOrder, CustomerOrderItem, Countreparty, User
from extensions import db

countreparties_orders_bp = Blueprint('countreparties_orders', __name__)


@countreparties_orders_bp.route("/", methods=['GET'])
def list_countreparties_orders():
    orders = db.session.execute(db.select(CustomerOrder)).scalars().all()
    return jsonify({
        'countreparties_orders': [
            {
                'id': o.id,
                "order_number": o.order_number,
                "order_date": o.order_date.isoformat() if o.order_date else None,
                "countreparties_id": o.countreparties_id,
                "executor_id": o.executor_id,
                "total_amount": float(o.total_amount) if o.total_amount else 0,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in orders
        ]
    }), 200


@countreparties_orders_bp.route("/", methods=['POST'])
def create_countreparties_order():
    data = request.get_json()
    required = ["order_number", "order_date", "countreparties_id", "executor_id"]
    if not data or not all(f in data for f in required):
        return jsonify({
            "error": "Bad Request",
            "message": f"Укажите {', '.join(required)}"
        }), 400

    od = data["order_date"]
    order_date = date.fromisoformat(od) if isinstance(od, str) else od

    new_order = CustomerOrder(
        order_number=data["order_number"],
        order_date=order_date,
        countreparties_id=data["countreparties_id"],
        executor_id=data["executor_id"],
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
                discount=item_data.get("discount", 0),
            )
            db.session.add(item)
        db.session.commit()

    return jsonify({
        "message": "Заказ создан",
        "countreparties_order_id": new_order.id,
    }), 201


@countreparties_orders_bp.route("/<int:order_id>", methods=['GET'])
def get_countreparties_order(order_id):
    order = db.session.get(CustomerOrder, order_id)
    if not order:
        return jsonify({"error": "Not Found", "message": "Заказ не найден"}), 404

    items = [
        {
            "countreparties_order_item_id": i.id,
            "item_id": i.item_id,
            "quantity": float(i.quantity),
            "unit_price": float(i.unit_price),
            "discount": float(i.discount),
        }
        for i in order.items
    ]

    return jsonify({
        "countreparties_order_id": order.id,
        "order_number": order.order_number,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "countreparties_id": order.countreparties_id,
        "executor_id": order.executor_id,
        "total_amount": float(order.total_amount) if order.total_amount else 0,
        "items": items,
    }), 200


@countreparties_orders_bp.route("/<int:order_id>/cost-calculation", methods=['GET'])
def calculate_cost(order_id):
    order = db.session.get(CustomerOrder, order_id)
    if not order:
        return jsonify({"error": "Not Found", "message": "Заказ не найден"}), 404

    from services.customer_order_service import CustomerOrderService
    service = CustomerOrderService()
    result = service.calculate_cost(order_id)
    return jsonify(result), 200