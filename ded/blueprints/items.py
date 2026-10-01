from flask import Blueprint, request, jsonify
from models import Item
from extensions import db

items_bp = Blueprint('items', __name__)


@items_bp.route('/', methods=['GET'])
def list_items():
    items = db.session.execute(db.select(Item)).scalars().all()
    return jsonify({
        "items": [
            {
                "item_id": item.id,
                "name": item.name,
                "code": item.code,
                "item_type": item.item_type,
                "created_at": item.created_at.isoformat() if item.created_at else None,
            }
            for item in items
        ]
    }), 200


@items_bp.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or "name" not in data or "code" not in data or "item_type" not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "Необходимо указать name, code и item_type",
        }), 400

    if data["item_type"] not in ("Продукция", "Материалы", "Операция"):
        return jsonify({
            "error": "Bad Request",
            "message": "item_type должен быть: Продукция, Материалы или Операция",
        }), 400

    new_item = Item(name=data["name"], code=data["code"], item_type=data["item_type"])
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": f"Элемент '{new_item.name}' создан",
        "item_id": new_item.id,
    }), 201


@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"error": "Not Found", "message": "Элемент не найден"}), 404

    return jsonify({
        "item_id": item.id,
        "name": item.name,
        "code": item.code,
        "item_type": item.item_type,
        "created_at": item.created_at.isoformat() if item.created_at else None,
    }), 200


@items_bp.route('/<int:item_id>', methods=['PUT', 'PATCH'])
def update_item(item_id):
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"error": "Not Found", "message": "Элемент не найден"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message": "Нет данных"}), 400

    if "name" in data:
        item.name = data["name"]
    if "code" in data:
        item.code = data["code"]
    if "item_type" in data:
        if data["item_type"] not in ("Продукция", "Материалы", "Операция"):
            return jsonify({"error": "Bad Request", "message": "Неверный item_type"}), 400
        item.item_type = data["item_type"]

    db.session.commit()
    return jsonify({"message": "Элемент обновлён"}), 200


@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"error": "Not Found", "message": "Элемент не найден"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Элемент удалён"}), 200