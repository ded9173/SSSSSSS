from repository.base_repository import BaseRepository
from models import Item

class ItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Item)