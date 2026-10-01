def format_note_id(note_id: int) -> str:
    """Форматирует ID заметки: '00001'."""
    return str(note_id).zfill(5)


def format_date(date_obj) -> str:
    """Форматирует дату в YYYY-MM-DD."""
    if date_obj is None:
        return ""
    return date_obj.strftime("%Y-%m-%d")


def build_note_response(note, login: str) -> dict:
    """Создаёт словарь ответа для заметки."""
    return {
        "id": format_note_id(note.note_id),
        "title_user": f"{note.title} ({login})",
        "content": note.content,
        "formatted_date": format_date(note.created_at),
    }