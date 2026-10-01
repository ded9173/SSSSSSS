from flask import Blueprint, request, jsonify
from models import Specification, Item
from extensions import db

specification_bp = Blueprint('specification', __name__)


@specification_bp.route('/', methods=['GET'])
def list_specification():
    specs = db.session.execute(db.select(Specification)).scalars().all()
    return jsonify({
        "specifications": [
            {
                "specification_id": s.id,
                "name": s.name,
                "item_id": s.item_id,
                "material_id": s.material_id,
                "quantity": float(s.quantity) if s.quantity else 0,
                "operation_time": float(s.operation_time) if s.operation_time else 0,
            }
            for s in specs
        ]
    }), 200


@specification_bp.route('/', methods=['POST'])
def create_specification():
    data = request.get_json()
    if not data or "name" not in data or "item_id" not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "Укажите name и item_id",
        }), 400

    new_spec = Specification(
        name=data["name"],
        item_id=data["item_id"],
        material_id=data.get("material_id"),
        quantity=data.get("quantity", 0),
        operation_time=data.get("operation_time", 0),
    )
    db.session.add(new_spec)
    db.session.commit()

    return jsonify({
        "message": "Спецификация создана",
        "specification_id": new_spec.id,
    }), 201