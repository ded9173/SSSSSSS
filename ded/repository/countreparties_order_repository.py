from repository.base_repository import BaseRepository
from models import CustomerOrder

class CountrepartiesOrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(CustomerOrder)