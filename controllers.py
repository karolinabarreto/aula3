from flask import Blueprint, jsonify, request

from models import Filme, Sala, Sessao, TipoIngresso

api = Blueprint("api", __name__, url_prefix="/api")


# ================= FILMES =================

@api.route("/filmes", methods=["POST"])
def cadastrar_filme():
    dados = request.get_json() or {}
    erro = Filme.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(Filme.cadastrar(dados).to_dict()), 201


@api.route("/filmes", methods=["GET"])
def listar_filmes():
    return jsonify([f.to_dict() for f in Filme.listar()])


@api.route("/filmes/<int:filme_id>", methods=["GET"])
def buscar_filme(filme_id):
    filme = Filme.buscar(filme_id)
    if not filme:
        return jsonify({"erro": "Filme nao encontrado."}), 404
    return jsonify(filme.to_dict())


@api.route("/filmes/<int:filme_id>", methods=["PUT"])
def editar_filme(filme_id):
    filme = Filme.buscar(filme_id)
    if not filme:
        return jsonify({"erro": "Filme nao encontrado."}), 404
    dados = {**filme.to_dict(), **(request.get_json() or {})}
    erro = Filme.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(filme.atualizar(dados).to_dict())


@api.route("/filmes/<int:filme_id>", methods=["DELETE"])
def remover_filme(filme_id):
    filme = Filme.buscar(filme_id)
    if not filme:
        return jsonify({"erro": "Filme nao encontrado."}), 404
    filme.remover()
    return jsonify({"mensagem": "Filme removido com sucesso."})


# ================= SALAS =================

@api.route("/salas", methods=["POST"])
def cadastrar_sala():
    dados = request.get_json() or {}
    erro = Sala.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(Sala.cadastrar(dados).to_dict()), 201


@api.route("/salas", methods=["GET"])
def listar_salas():
    return jsonify([s.to_dict() for s in Sala.listar()])


@api.route("/salas/<int:sala_id>", methods=["GET"])
def buscar_sala(sala_id):
    sala = Sala.buscar(sala_id)
    if not sala:
        return jsonify({"erro": "Sala nao encontrada."}), 404
    return jsonify(sala.to_dict())


@api.route("/salas/<int:sala_id>", methods=["PUT"])
def editar_sala(sala_id):
    sala = Sala.buscar(sala_id)
    if not sala:
        return jsonify({"erro": "Sala nao encontrada."}), 404
    dados = {**sala.to_dict(), **(request.get_json() or {})}
    erro = Sala.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(sala.atualizar(dados).to_dict())


@api.route("/salas/<int:sala_id>", methods=["DELETE"])
def remover_sala(sala_id):
    sala = Sala.buscar(sala_id)
    if not sala:
        return jsonify({"erro": "Sala nao encontrada."}), 404
    sala.remover()
    return jsonify({"mensagem": "Sala removida com sucesso."})


# ================= SESSOES =================

@api.route("/sessoes", methods=["POST"])
def cadastrar_sessao():
    dados = request.get_json() or {}
    erro = Sessao.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    if Sessao.existe_conflito(dados["sala_id"], dados["data"], dados["hora_inicio"]):
        return jsonify({"erro": "Ja existe uma sessao nessa sala, data e horario."}), 409
    return jsonify(Sessao.cadastrar(dados).to_dict()), 201


@api.route("/sessoes", methods=["GET"])
def listar_sessoes():
    return jsonify([s.to_dict() for s in Sessao.listar(request.args.get("data"))])


@api.route("/sessoes/<int:sessao_id>", methods=["GET"])
def buscar_sessao(sessao_id):
    sessao = Sessao.buscar(sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessao nao encontrada."}), 404
    return jsonify(sessao.to_dict())


@api.route("/sessoes/<int:sessao_id>", methods=["PUT"])
def editar_sessao(sessao_id):
    sessao = Sessao.buscar(sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessao nao encontrada."}), 404
    dados = {**sessao.to_dict(), **(request.get_json() or {})}
    erro = Sessao.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    if Sessao.existe_conflito(dados["sala_id"], dados["data"], dados["hora_inicio"], ignorar_id=sessao_id):
        return jsonify({"erro": "Ja existe uma sessao nessa sala, data e horario."}), 409
    return jsonify(sessao.atualizar(dados).to_dict())


@api.route("/sessoes/<int:sessao_id>", methods=["DELETE"])
def remover_sessao(sessao_id):
    sessao = Sessao.buscar(sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessao nao encontrada."}), 404
    sessao.remover()
    return jsonify({"mensagem": "Sessao removida com sucesso."})


# ================= TIPOS DE INGRESSO =================

@api.route("/tipos-ingresso", methods=["POST"])
def cadastrar_tipo_ingresso():
    dados = request.get_json() or {}
    erro = TipoIngresso.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(TipoIngresso.cadastrar(dados).to_dict()), 201


@api.route("/tipos-ingresso", methods=["GET"])
def listar_tipos_ingresso():
    return jsonify([t.to_dict() for t in TipoIngresso.listar()])


@api.route("/tipos-ingresso/<int:tipo_id>", methods=["GET"])
def buscar_tipo_ingresso(tipo_id):
    tipo_ingresso = TipoIngresso.buscar(tipo_id)
    if not tipo_ingresso:
        return jsonify({"erro": "Tipo de ingresso nao encontrado."}), 404
    return jsonify(tipo_ingresso.to_dict())


@api.route("/tipos-ingresso/<int:tipo_id>", methods=["PUT"])
def editar_tipo_ingresso(tipo_id):
    tipo_ingresso = TipoIngresso.buscar(tipo_id)
    if not tipo_ingresso:
        return jsonify({"erro": "Tipo de ingresso nao encontrado."}), 404
    dados = {**tipo_ingresso.to_dict(), **(request.get_json() or {})}
    erro = TipoIngresso.validar(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(tipo_ingresso.atualizar(dados).to_dict())


@api.route("/tipos-ingresso/<int:tipo_id>", methods=["DELETE"])
def remover_tipo_ingresso(tipo_id):
    tipo_ingresso = TipoIngresso.buscar(tipo_id)
    if not tipo_ingresso:
        return jsonify({"erro": "Tipo de ingresso nao encontrado."}), 404
    tipo_ingresso.remover()
    return jsonify({"mensagem": "Tipo de ingresso removido com sucesso."})
