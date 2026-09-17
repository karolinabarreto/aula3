from flask import Flask, jsonify

import models
from controllers import api

app = Flask(__name__)
models.init_db()
app.register_blueprint(api)
print(f"[cinema] usando banco de dados em: {models.DB_NAME}")


@app.route("/")
def index():
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
    return """
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
