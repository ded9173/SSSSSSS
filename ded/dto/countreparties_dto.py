from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class CountrepartiesDTO:
    countreparties_id: int
    name: str
    inn: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    type: str = ""
    created_at: Optional[str] = None

    @classmethod
    def from_model(cls, countreparties) -> "CountrepartiesDTO":
        return cls(
            countreparties_id=countreparties.id,
            name=countreparties.name,
            inn=countreparties.inn,
            address=countreparties.address,
            phone=countreparties.phone,
            type=countreparties.type,
            created_at=countreparties.created_at.isoformat() if countreparties.created_at else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)