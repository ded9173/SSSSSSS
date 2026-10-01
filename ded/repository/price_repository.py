from repository.base_repository import BaseRepository
from models import Price

class PriceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Price)