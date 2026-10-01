from repository.base_repository import BaseRepository
from models import Specification

class SpecificationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Specification)