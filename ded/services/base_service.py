from typing import List, Optional, Any

class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, item_id: Any) -> Optional[Any]:
        return self.repository.get_by_id(item_id)

    def create(self, **kwargs) -> Any:
        return self.repository.create(**kwargs)

    def update(self, item_id: Any, **kwargs) -> Optional[Any]:
        return self.repository.update(item_id, **kwargs)

    def delete(self, item_id: Any) -> bool:
        return self.repository.delete(item_id)