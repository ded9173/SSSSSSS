from flask import Blueprint, request, jsonify, Response
from PIL import Image
import io

from puzzle_captcha import puzzle_captcha

puzzle_captcha_bp = Blueprint(
    "puzzle_captcha_bp",
    __name__,
)

@puzzle_captcha_bp.route("/generate", methods=["GET"])
def generate():
    try:
        data = puzzle_captcha.generate()
        return jsonify({
            "token": data["token"],
            "fragments": data["fragments"],
            "grid_size": data["grid_size"],
            "correct_order": data["correct_order"],
            "num_pieces": data.get("num_pieces", len(data["fragments"])),
            "reference_image": data.get("reference_image"),
        }), 200

    except Exception as e:
        return jsonify({
            "error": "internal server error",
            "message": f"Ошибка генерации: {str(e)}",
        }), 500

@puzzle_captcha_bp.route("/fragment/<token>/<int: index>", methods=["GET"])
def get_fragments(token, index):
    try:
        img = puzzle_captcha.get_fragment_image(token, index)
        if img is None:
            return jsonify({"error": "Fragment not found"}), 404

        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, (0, 0), img)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    buffer_data = buffered.getvalue()

    response = Response(buffer_data, mimetype="image/png")
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@puzzle_captcha_bp.route("/reference/<token>", methods=['GET'])
def get_reference(token):
    try:
        img = puzzle_captcha.get_reference_image(token)
        if img is None:
            return jsonify({"error": "Reference not found"}), 404

        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, (0, 0), img)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        buffer_data = buffered.getvalue()

        response = Response(buffer_data, mimetype="image/png")
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@puzzle_captcha_bp.route("/verify", methods=['POST'])
def verify():
    data = request.get_json()
    if not data or "token" not in data or "fragments" not in data:
        return jsonify({
            "error": "Bad request",
            "message": "Укажите token и fragment_order"
        }), 400

    token = data["token"]
    fragment_order = data["fragment_order"]

    if not isinstance(fragment_order, list) or len(fragment_order) < 1:
        return jsonify({
            "error": "Bad request",
            "message": "fragment_order должен быть массивом"
        }), 400

    is_valid = puzzle_captcha.verify(token, fragment_order)

    return jsonify({
        "valid": is_valid,
        "message": "Пазл собран верно" if is_valid else "Пазл собран неверно"
    })

