import uuid
from flask import request, Blueprint
from views.base_view import BaseAPIView
from services.items_service import ItemsService

items_bp = Blueprint("items", __name__)

class ItemListAPI(BaseAPIView):
    def __init__(self):
        self.service = ItemsService()

    def get(self):
        items = self.service.get_all_dto()
        return self._success_response({"items": [i.to_dict() for i in items]})

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "code" not in data or "item_type" not in data:
            return self._error_response("Укажите name, code и item_type")

        try:
            item = self.service.create_item(
                name=data["name"], code=data["code"], item_type=data["item_type"]
            )
            return self._success_response({"message": "Элемент создан", "item_id": item.id}, 201)
        except ValueError as e:
            return self._error_response(str(e))

class ItemDetailAPI(BaseAPIView):
    def __init__(self):
        self.service = ItemsService()

    def get(self, item_id):
        item = self.service.get_by_id_dto(item_id)
        if not item:
            return self._not_found_response("Элемент")
        return self._success_response(item.to_dict())

    def put(self, item_id):
        data = request.get_json()
        if not data:
            return self._error_response("Нет данных")

        try:
            item = self.service.update_item(
                item_id, name=data.get("name"), code=data.get("code"), item_type=data.get("item_type")
            )
            if not item:
                return self._not_found_response("Элемент")
            return self._success_response({"message": "Элемент обновлён"})
        except ValueError as e:
            return self._error_response(str(e))

    def delete(self, item_id):
        item = self.service.get_by_id(item_id)
        if not item:
            return self._not_found_response("Элемент")
        self.service.delete(item_id)
        return self._success_response({"message": "Элемент удалён"})

items_bp.add_url_rule("/", view_func=ItemListAPI.as_view("items_list"))
items_bp.add_url_rule("/<int:item_id>", view_func=ItemDetailAPI.as_view("item_detail"))