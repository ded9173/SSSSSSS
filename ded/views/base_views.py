from flask import jsonify
from flask.views import MethodView

class BaseAPIView(MethodView):

    decorators = []

    def _success_response(self, data, status=200):
        return jsonify(data), status

    def _error_response(self, message, status=400):
        return jsonify({"error": "Error", "message": message}), status

    def _not_found_response(self, resource="Ресурс"):
        return jsonify({"error": "Not Found", "message": f"{resource} не найден"}), 404


