from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({"success": False, "error": e.description if hasattr(e, 'description') else "No autorizado"}), 401

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"success": False, "error": e.description if hasattr(e, 'description') else "Petición inválida"}), 400

    @app.errorhandler(HTTPException)
    def handle_generic_http_error(e):
        return jsonify({"success": False, "error": e.description}), e.code