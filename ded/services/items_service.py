from typing import List, Optional
from services.base_service import BaseService
from repository.items_repository import ItemsRepository
from dto.items_dto import ItemsDTO


class ItemsService(BaseService):
    def __init__(self):
        super().__init__(ItemsRepository())

    def get_all_dto(self, skip: int = 0, limit: int = 100) -> List[ItemsDTO]:
        items = self.get_all(skip, limit)
        return [ItemsDTO.from_model(i) for i in items]

    def get_by_id_dto(self, item_id: int) -> Optional[ItemsDTO]:
        item = self.get_by_id(item_id)
        return ItemsDTO.from_model(item) if item else None

    def create_item(self, name: str, code: str, item_type: str):
        return self.repository.create(name=name, code=code, item_type=item_type)

    def update_item(self, item_id: int, name: str = None, code: str = None, item_type: str = None):
        return self.repository.update(item_id, name=name, code=code, item_type=item_type)