from flask import Blueprint, request, jsonify
from models import Countreparty
from extensions import db

countreparties_bp = Blueprint('countreparties', __name__)


@countreparties_bp.route('/', methods=['GET'])
def list_countreparties():
    items = db.session.execute(db.select(Countreparty)).scalars().all()
    return jsonify({
        "countreparties": [
            {
                "countreparties_id": c.id,
                "name": c.name,
                "inn": c.inn,
                "address": c.address,
                "phone": c.phone,
                "type": c.type,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in items
        ]
    }), 200


@countreparties_bp.route('/', methods=['POST'])
def create_countreparties():
    data = request.get_json()
    if not data or "name" not in data or "type" not in data:
        return jsonify({
            "error": "Bad request",
            "message": "Необходимо указать name и type",
        }), 400

    new = Countreparty(
        name=data["name"],
        inn=data.get("inn"),
        address=data.get("address"),
        phone=data.get("phone"),
        type=data["type"],
    )
    db.session.add(new)
    db.session.commit()

    return jsonify({
        "message": "Контрагент создан",
        "client_id": new.id,
    }), 201


@countreparties_bp.route('/<int:countreparties_id>', methods=['GET'])
def get_countreparties(countreparties_id):
    c = db.session.get(Countreparty, countreparties_id)
    if not c:
        return jsonify({"error": "Not found", "message": "Контрагент не найден"}), 404

    return jsonify({
        "countreparties_id": c.id,
        "name": c.name,
        "inn": c.inn,
        "address": c.address,
        "phone": c.phone,
        "type": c.type,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }), 200


@countreparties_bp.route('/<int:countreparties_id>', methods=['PUT'])
def update_countreparties(countreparties_id):
    c = db.session.get(Countreparty, countreparties_id)
    if not c:
        return jsonify({"error": "Not Found", "message": "Контрагент не найден"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message": "Нет данных"}), 400

    c.name = data.get("name", c.name)
    c.inn = data.get("inn", c.inn)
    c.address = data.get("address", c.address)
    c.phone = data.get("phone", c.phone)
    c.type = data.get("type", c.type)

    db.session.commit()
    return jsonify({"message": "Контрагент обновлён"}), 200


@countreparties_bp.route('/<int:countreparties_id>', methods=['DELETE'])
def delete_countreparties(countreparties_id):
    c = db.session.get(Countreparty, countreparties_id)
    if not c:
        return jsonify({"error": "Not Found", "message": "Контрагент не найден"}), 404

    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Контрагент удалён"}), 200