from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SpecificationMaterialDTO:
    spec_mat_id: int
    item_id: int
    material_id: Optional[int]
    quantity: float
    name: Optional[str] = None

    @classmethod
    def from_model(cls, spec) -> "SpecificationMaterialDTO":
        return cls(
            spec_mat_id=spec.id,
            item_id=spec.item_id,
            material_id=spec.material_id,
            quantity=float(spec.quantity) if spec.quantity else 0.0,
            name=spec.name,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SpecificationOperationDTO:
    spec_op_id: int
    item_id: int
    operation_id: Optional[int]
    operation_time: float
    name: Optional[str] = None

    @classmethod
    def from_model(cls, spec) -> "SpecificationOperationDTO":
        return cls(
            spec_op_id=spec.id,
            item_id=spec.item_id,
            operation_id=spec.material_id,
            operation_time=float(spec.operation_time) if spec.operation_time else 0.0,
            name=spec.name,
        )

    def to_dict(self) -> dict:
        return asdict(self)