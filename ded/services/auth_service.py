from flask import jsonify
from flask_login import login_user
from auth import verify_password
from extensions import db
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def login(self, data: dict):
        login_value = (data.get("login") or "").strip()
        password_value = (data.get("password") or "").strip()

        if not login_value or not password_value:
            return jsonify({
                "error": "Bad request",
                "message": "Поля login и password обязательны"
            }), 400

        user = self.repository.find_by_login(login_value)

        if not user or not verify_password(password_value, user.password_hash):
            if user:
                self.repository.increment_failed_attempts(user.user_id)
            return jsonify({
                "error": "Unauthorized",
                "message": "Неверный логин или пароль"
            }), 401

        if user.is_blocked:
            return jsonify({
                "error": "Forbidden",
                "message": "Вы заблокированы"
            }), 403

        login_user(user)
        user.failed_attempts = 0
        db.session.commit()

        return jsonify({
            "message": "Авторизация успешна",
            "user_id": user.user_id,
            "login": user.login,
            "role": user.role,
        }), 200