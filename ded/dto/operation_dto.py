from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class OperationDTO:
    operation_id: int
    name: str
    code: str
    created_at: Optional[str] = None

    @classmethod
    def from_model(cls, operation) -> "OperationDTO":
        return cls(
            operation_id=operation.id,
            name=operation.name,
            code=operation.code,
            created_at=operation.created_at.isoformat() if operation.created_at else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)