from typing import List, Optional
from services.base_service import BaseService
from repository.countreparties_repository import CountrepartiesRepository
from dto.countreparties_dto import CountrepartiesDTO

class CountrepartiesService(BaseService):
    def __init__(self):
        super().__init__(CountrepartiesRepository())

    def get_all_dto(self) -> List[CountrepartiesDTO]:
        clients = self.get_all()
        return [CountrepartiesDTO.from_model(c) for c in clients]

    def get_by_id_dto(self, client_id: int) -> Optional[CountrepartiesDTO]:
        client = self.get_by_id(client_id)
        return CountrepartiesDTO.from_model(client) if client else None

    def create_countrepartie(self, name: str, type: str, inn: str = None, address: str = None, phone: str = None):
        return self.repository.create(name=name, type=type, inn=inn, address=address, phone=phone)

    def update_countrepartie(self, client_id: int, **kwargs):
        return self.repository.update(client_id, **kwargs)