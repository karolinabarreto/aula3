import os

from flask import Flask, jsonify, send_from_directory

import models
from controllers import api

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

SWAGGER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cinema API - Documentacao (Swagger)</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function () {
            SwaggerUIBundle({
                url: "/static/openapi.json",
                dom_id: "#swagger-ui"
            });
        };
    </script>
</body>
</html>
"""


def create_app(db_path=None):
    """Cria a aplicacao Flask.

    db_path permite apontar para outro arquivo de banco (os testes
    automatizados usam um banco temporario, para nao mexer no cinema.db).
    """
    if db_path:
        models.DB_NAME = db_path
    models.init_db()

    app = Flask(__name__, static_folder=STATIC_DIR)
    app.register_blueprint(api)

    # View: pagina web que exibe filmes, sessoes, salas e ingressos.
    # Ela nao acessa o banco diretamente - busca tudo pela API REST (fetch).
    @app.route("/")
    def index():
        return send_from_directory(STATIC_DIR, "index.html")

    @app.route("/api")
    def api_index():
        return jsonify({
            "mensagem": "API de venda de ingressos de cinema",
            "documentacao": "/docs",
            "endpoints": {
                "filmes": "/api/filmes",
                "salas": "/api/salas",
                "sessoes": "/api/sessoes",
                "tipos_ingresso": "/api/tipos-ingresso",
            },
        })

    @app.route("/docs")
    def docs():
        return SWAGGER_HTML

    return app


if __name__ == "__main__":
    app = create_app()
    print(f"[cinema] usando banco de dados em: {models.DB_NAME}")
    print("[cinema] site: http://127.0.0.1:5000  |  API: http://127.0.0.1:5000/api")
    app.run(debug=True, host="0.0.0.0", port=5000)
