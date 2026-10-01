from repository.base_repository import BaseRepository
from models import ProductionOrder

class ProductionOrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProductionOrder)