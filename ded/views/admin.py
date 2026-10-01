from flask import request, Blueprint, jsonify
from flask_login import login_required, current_user
from views.base_view import BaseAPIView
from services.user_service import UserService

admin_bp = Blueprint("admin", __name__)

def _require_admin():
    """Проверка прав администратора."""
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized", "message": "Необходима авторизация"}), 401
    if current_user.role != "Администратор":
        return jsonify({"error": "Forbidden", "message": "Доступ запрещён"}), 403
    return None

class AdminUserListAPI(BaseAPIView):
    """Список пользователей."""

    decorators = [login_required]

    def __init__(self):
        self.service = UserService()

    def get(self):
        """Список пользователей."""
        admin_check = _require_admin()
        if admin_check:
            return admin_check
        users = self.service.get_all_dto()
        return self._success_response({"users": [u.to_dict() for u in users]})

class AdminUserCreateAPI(BaseAPIView):
    """Создание пользователя."""

    decorators = [login_required]

    def __init__(self):
        self.service = UserService()

    def post(self):
        """Создание пользователя."""
        admin_check = _require_admin()
        if admin_check:
            return admin_check

        data = request.get_json()
        if not data or "login" not in data or "password" not in data:
            return self._error_response("Укажите login и password")

        login_value = data["login"].strip()
        if not login_value or not data["password"]:
            return self._error_response("Поля обязательны")

        existing = self.service.repository.find_by_login(login_value)
        if existing:
            return self._error_response(f"Пользователь '{login_value}' существует")

        role = data.get("role", "Пользователь")
        if role not in ("Администратор", "Пользователь"):
            return self._error_response("Неверная роль")

        user = self.service.create_user(login=login_value, password=data["password"], role=role)
        return self._success_response({"message": f"Пользователь '{login_value}' создан", "user_id": user.user_id}, 201)

class AdminUserDetailAPI(BaseAPIView):
    """Обновление и удаление пользователя."""

    decorators = [login_required]

    def __init__(self):
        self.service = UserService()

    def put(self, user_id):
        """Обновление пользователя."""
        admin_check = _require_admin()
        if admin_check:
            return admin_check

        user = self.service.get_by_id(user_id)
        if not user:
            return self._not_found_response("Пользователь")

        data = request.get_json()
        if not data:
            return self._error_response("Нет данных")

        role = data.get("role")
        if role is not None and role not in ("Администратор", "Пользователь"):
            return self._error_response("Неверная роль")

        is_blocked = data.get("is_blocked")
        user = self.service.update_user(user_id, role=role, is_blocked=is_blocked)
        if is_blocked is False and user:
            user.failed_attempts = 0
            from extensions import db
            db.session.commit()

        return self._success_response({"message": "Данные обновлены"})

    def delete(self, user_id):
        """Удаление пользователя."""
        admin_check = _require_admin()
        if admin_check:
            return admin_check

        if user_id == current_user.user_id:
            return self._error_response("Нельзя удалить себя")

        user = self.service.get_by_id(user_id)
        if not user:
            return self._not_found_response("Пользователь")

        self.service.delete(user_id)
        return self._success_response({"message": f"Пользователь '{user.login}' удалён"})

admin_bp.add_url_rule("/users/", view_func=AdminUserListAPI.as_view("admin_users_list"))
admin_bp.add_url_rule("/users/",view_func=AdminUserCreateAPI.as_view("admin_users_create"))
admin_bp.add_url_rule("/users/<int:user_id>", view_func=AdminUserDetailAPI.as_view("admin_user_detail"))