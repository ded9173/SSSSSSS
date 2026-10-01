from repository.base_repository import BaseRepository
from models import Countreparty

class CountrepartiesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Countreparty)