from typing import List, Optional
from services.base_service import BaseService
from repositories.user_repository import UserRepository
from dto.user_dto import UserDTO
from auth import hash_password

class UserService(BaseService):
    def __init__(self):
        super().__init__(UserRepository())

    def get_all_dto(self) -> List[UserDTO]:
        users = self.get_all()
        return [UserDTO.from_model(u) for u in users]

    def create_user(self, login: str, password: str, role: str = "Пользователь"):
        return self.repository.create(
            login=login, password_hash=hash_password(password), role=role
        )

    def update_user(self, user_id: int, role: str = None, is_blocked: bool = None):
        return self.repository.update(user_id, role=role, is_blocked=is_blocked)