from flask import Blueprint, request, jsonify
from sqlalchemy import select
from models import Note, User
from utils import build_note_response
from extensions import db

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["GET"])
def get_notes():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)

    if skip < 0 or limit < 1:
        return jsonify({
            "error": "Bad Request",
            "message": "skip >= 0, limit >= 1"
        }), 400

    stmt = (
        select(Note, User.login)
        .join(User, Note.id_user == User.user_id)
        .offset(skip)
        .limit(limit)
    )
    result = db.session.execute(stmt).all()

    notes = []
    for note, login in result:
        notes.append(build_note_response(note, login))

    total = db.session.execute(
        select(db.func.count(Note.note_id))
    ).scalar()

    return jsonify({"notes": notes, "total": total}), 200


@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({
            "error": "Not Found",
            "message": "Заметка не найдена"
        }), 404

    user = db.session.get(User, note.id_user)
    login = user.login if user else None

    return jsonify(build_note_response(note, login)), 200