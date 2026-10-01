from typing import Optional, List, Any
from extensions import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        return db.session.execute(
            db.select(self.model).offset(skip).limit(limit)
        ).scalars().all()

    def get_by_id(self, item_id: Any) -> Optional[Any]:
        return db.session.get(self.model, item_id)

    def create(self, **kwargs) -> Any:
        item = self.model(**kwargs)
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, item_id: Any, **kwargs) -> Optional[Any]:
        item = self.get_by_id(item_id)
        if item:
            for key, value in kwargs.items():
                if value is not None and hasattr(item, key):
                    setattr(item, key, value)
            db.session.commit()
        return item

    def delete(self, item_id: Any) -> bool:
        item = self.get_by_id(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False