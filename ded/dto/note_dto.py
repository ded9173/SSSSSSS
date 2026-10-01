from dataclasses import dataclass
from utils import format_note_id, format_date


@dataclass
class NoteDTO:
    id: str
    title_user: str
    content: str
    formatted_date: str

    @classmethod
    def from_model(cls, note, login: str) -> "NoteDTO":
        return cls(
            id=format_note_id(note.note_id),
            title_user=f"{note.title} - {login}",
            content=note.content,
            formatted_date=format_date(note.created_at),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title_user": self.title_user,
            "content": self.content,
            "formatted_date": self.formatted_date,
        }