from repository.base_repository import BaseRepository
from models import CostPrice

class CostPriceRepository(BaseRepository):
    def __init__(self):
        super().__init__(CostPrice)