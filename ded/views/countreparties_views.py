from flask import request, Blueprint
from views.base_view import BaseAPIView
from services.countreparties_service import CountrepartiesService

countreparties_bp = Blueprint("countreparties", __name__)

class CountrepartiesListAPI(BaseAPIView):
    def __init__(self):
        self.service = CountrepartiesService()

    def get(self):
        countreparties = self.service.get_all_dto()
        return self._success_response({"countreparties": [c.to_dict() for c in countreparties]})

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "type" not in data:
            return self._error_response("Укажите name и type")

        try:
            countreparties = self.service.create_countrepartie(
                name=data["name"], type=data["type"],
                inn=data.get("inn"), address=data.get("address"), phone=data.get("phone")
            )
            return self._success_response({"message": "Контрагент создан", "client_id": countreparties.id}, 201)
        except ValueError as e:
            return self._error_response(str(e))

class CountrepartiesDetailAPI(BaseAPIView):
    def __init__(self):
        self.service = CountrepartiesService()

    def get(self, client_id):
        countreparties = self.service.get_by_id_dto(client_id)
        if not countreparties:
            return self._not_found_response("Контрагент")
        return self._success_response(countreparties.to_dict())

    def put(self, client_id):
        data = request.get_json()
        if not data:
            return self._error_response("Нет данных")

        try:
            countreparties = self.service.update_countrepartie(
                client_id, name=data.get("name"), inn=data.get("inn"),
                address=data.get("address"), phone=data.get("phone"), type=data.get("type")
            )
            if not countreparties:
                return self._not_found_response("Контрагент")
            return self._success_response({"message": "Контрагент обновлён"})
        except ValueError as e:
            return self._error_response(str(e))

    def delete(self, client_id):
        countreparties = self.service.get_by_id(client_id)
        if not countreparties:
            return self._not_found_response("Контрагент")
        self.service.delete(client_id)
        return self._success_response({"message": "Контрагент удалён"})

countreparties_bp.add_url_rule("/", view_func=CountrepartiesListAPI.as_view("countreparties_list"))
countreparties_bp.add_url_rule("/<int:client_id>", view_func=CountrepartiesDetailAPI.as_view("countrepartie_detail"))