from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class UserDTO:
    user_id: int
    login: str
    role: str
    is_blocked: bool = False
    failed_attempts: int = 0
    created_at: Optional[str] = None

    @classmethod
    def from_model(cls, user) -> "UserDTO":
        return cls(
            user_id=user.user_id,
            login=user.login,
            role=user.role,
            is_blocked=user.is_blocked,
            failed_attempts=user.failed_attempts,
            created_at=user.created_at.isoformat() if user.created_at else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)