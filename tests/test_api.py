"""Testes automatizados do CRUD da API (rodam com: pytest -v).

Cada teste usa um banco SQLite temporario e vazio, entao o cinema.db
nao e alterado.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app  # noqa: E402

FILME = {"nome": "Homem-Aranha: Um Novo Dia", "data_estreia": "29/07/2026", "data_saida": "15/10/2026",
         "duracao": 150, "cartaz": "/static/cartazes/homem-aranha-um-novo-dia.jpg"}
SALA = {"numero": 1, "capacidade": 50, "tipo": "2D"}
TIPO = {"tipo": "2D", "valor_ingresso": 30.0}


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=str(tmp_path / "teste.db"))
    app.config["TESTING"] = True
    return app.test_client()


def criar_sessao(client, **extra):
    filme = client.post("/api/filmes", json=FILME).get_json()
    sala = client.post("/api/salas", json=SALA).get_json()
    dados = {"sala_id": sala["id"], "filme_id": filme["id"], "data": "24/09/2026", "hora_inicio": 20, **extra}
    return client.post("/api/sessoes", json=dados)


# ---------------- Filmes ----------------

def test_criar_filme(client):
    resp = client.post("/api/filmes", json=FILME)
    assert resp.status_code == 201
    assert resp.get_json()["nome"] == "Homem-Aranha: Um Novo Dia"
    assert resp.get_json()["cartaz"] == FILME["cartaz"]


def test_criar_filme_invalido(client):
    assert client.post("/api/filmes", json={**FILME, "nome": ""}).status_code == 400
    assert client.post("/api/filmes", json={**FILME, "duracao": -1}).status_code == 400


def test_criar_filme_com_estreia_depois_da_saida(client):
    assert client.post("/api/filmes", json={**FILME, "data_estreia": "30/10/2026"}).status_code == 400


def test_listar_filmes(client):
    client.post("/api/filmes", json=FILME)
    client.post("/api/filmes", json={**FILME, "nome": "Minha Melhor Amiga"})
    assert len(client.get("/api/filmes").get_json()) == 2


def test_buscar_filme(client):
    filme = client.post("/api/filmes", json=FILME).get_json()
    assert client.get(f"/api/filmes/{filme['id']}").get_json() == filme


def test_buscar_filme_inexistente(client):
    assert client.get("/api/filmes/999").status_code == 404


def test_editar_filme(client):
    filme = client.post("/api/filmes", json=FILME).get_json()
    resp = client.put(f"/api/filmes/{filme['id']}", json={"duracao": 155})
    assert resp.status_code == 200
    assert client.get(f"/api/filmes/{filme['id']}").get_json()["duracao"] == 155


def test_remover_filme(client):
    filme = client.post("/api/filmes", json=FILME).get_json()
    assert client.delete(f"/api/filmes/{filme['id']}").status_code == 200
    assert client.get(f"/api/filmes/{filme['id']}").status_code == 404


# ---------------- Salas ----------------

def test_criar_sala(client):
    resp = client.post("/api/salas", json=SALA)
    assert resp.status_code == 201
    assert resp.get_json()["capacidade"] == 50


def test_criar_sala_tipo_invalido(client):
    assert client.post("/api/salas", json={**SALA, "tipo": "4D"}).status_code == 400


def test_listar_salas(client):
    client.post("/api/salas", json=SALA)
    assert len(client.get("/api/salas").get_json()) == 1


def test_editar_sala(client):
    sala = client.post("/api/salas", json=SALA).get_json()
    client.put(f"/api/salas/{sala['id']}", json={"tipo": "3D"})
    assert client.get(f"/api/salas/{sala['id']}").get_json()["tipo"] == "3D"


def test_editar_sala_inexistente(client):
    assert client.put("/api/salas/999", json={"tipo": "3D"}).status_code == 404


def test_remover_sala(client):
    sala = client.post("/api/salas", json=SALA).get_json()
    assert client.delete(f"/api/salas/{sala['id']}").status_code == 200
    assert client.get("/api/salas").get_json() == []


# ---------------- Sessoes ----------------

def test_criar_sessao_com_assentos_livres(client):
    resp = criar_sessao(client)
    assert resp.status_code == 201
    assert resp.get_json()["assentos"] == [0] * 50


def test_criar_sessao_com_filme_inexistente(client):
    assert criar_sessao(client, filme_id=999).status_code == 400


def test_criar_sessao_em_horario_ocupado(client):
    sessao = criar_sessao(client).get_json()
    dados = {k: sessao[k] for k in ("sala_id", "filme_id", "data", "hora_inicio")}
    assert client.post("/api/sessoes", json=dados).status_code == 409


def test_listar_sessoes_por_data(client):
    criar_sessao(client)
    assert len(client.get("/api/sessoes?data=24/09/2026").get_json()) == 1
    assert client.get("/api/sessoes?data=01/01/2027").get_json() == []


def test_editar_sessao(client):
    sessao = criar_sessao(client).get_json()
    client.put(f"/api/sessoes/{sessao['id']}", json={"hora_inicio": 22})
    assert client.get(f"/api/sessoes/{sessao['id']}").get_json()["hora_inicio"] == 22


def test_remover_sessao(client):
    sessao = criar_sessao(client).get_json()
    assert client.delete(f"/api/sessoes/{sessao['id']}").status_code == 200
    assert client.get(f"/api/sessoes/{sessao['id']}").status_code == 404


# ---------------- Tipos de ingresso ----------------

def test_criar_tipo_ingresso(client):
    resp = client.post("/api/tipos-ingresso", json=TIPO)
    assert resp.status_code == 201
    assert resp.get_json()["valor_ingresso"] == 30.0


def test_criar_tipo_ingresso_valor_negativo(client):
    assert client.post("/api/tipos-ingresso", json={**TIPO, "valor_ingresso": -5}).status_code == 400


def test_editar_tipo_ingresso(client):
    tipo = client.post("/api/tipos-ingresso", json=TIPO).get_json()
    client.put(f"/api/tipos-ingresso/{tipo['id']}", json={"valor_ingresso": 35.0})
    assert client.get(f"/api/tipos-ingresso/{tipo['id']}").get_json()["valor_ingresso"] == 35.0


def test_remover_tipo_ingresso(client):
    tipo = client.post("/api/tipos-ingresso", json=TIPO).get_json()
    assert client.delete(f"/api/tipos-ingresso/{tipo['id']}").status_code == 200
    assert client.get("/api/tipos-ingresso").get_json() == []


# ---------------- Pagina ----------------

def test_pagina_inicial_usa_a_api(client):
    html = client.get("/").get_data(as_text=True)
    assert "/api/filmes" in html and "/api/sessoes" in html
