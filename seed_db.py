"""
Popula o cinema.db com alguns dados de exemplo, usando as mesmas classes
e validacoes do models.py (ou seja, os dados de exemplo passam pelas
mesmas regras que qualquer requisicao POST passaria).

Se o cinema.db ja existir e ja tiver dados, rodar este script de novo so
acrescenta mais registros (nao apaga nada). Para comecar do zero, apague
o arquivo cinema.db antes de rodar.

Uso:
    python3 seed_db.py
"""

from models import init_db, Filme, Sala, Sessao, TipoIngresso


def seed():
    init_db()

    filmes_exemplo = [
        {"nome": "Duna: Parte 2", "data_estreia": "01/03/2024", "data_saida": "01/06/2024", "duracao": 166},
        {"nome": "Divertida Mente 2", "data_estreia": "13/06/2024", "data_saida": "13/09/2024", "duracao": 100},
        {"nome": "Coringa: Delirio a Dois", "data_estreia": "03/10/2024", "data_saida": "03/01/2025", "duracao": 138},
    ]
    filmes_criados = []
    for dados in filmes_exemplo:
        if Filme.validar(dados) is None:
            filmes_criados.append(Filme.cadastrar(dados))

    salas_exemplo = [
        {"numero": 1, "capacidade": 80, "tipo": "2D"},
        {"numero": 2, "capacidade": 60, "tipo": "3D"},
        {"numero": 3, "capacidade": 120, "tipo": "2D"},
    ]
    salas_criadas = []
    for dados in salas_exemplo:
        if Sala.validar(dados) is None:
            salas_criadas.append(Sala.cadastrar(dados))

    tipos_exemplo = [
        {"tipo": "2D", "valor_ingresso": 28.0},
        {"tipo": "3D", "valor_ingresso": 38.0},
    ]
    for dados in tipos_exemplo:
        if TipoIngresso.validar(dados) is None:
            TipoIngresso.cadastrar(dados)

    if len(filmes_criados) >= 3 and len(salas_criadas) >= 3:
        sessoes_exemplo = [
            {"sala_id": salas_criadas[0].id, "filme_id": filmes_criados[0].id, "data": "20/03/2024", "hora_inicio": 20},
            {"sala_id": salas_criadas[1].id, "filme_id": filmes_criados[1].id, "data": "20/06/2024", "hora_inicio": 18},
            {"sala_id": salas_criadas[2].id, "filme_id": filmes_criados[2].id, "data": "05/10/2024", "hora_inicio": 21},
        ]
        for dados in sessoes_exemplo:
            erro = Sessao.validar(dados)
            ja_existe = Sessao.existe_conflito(dados["sala_id"], dados["data"], dados["hora_inicio"])
            if erro is None and not ja_existe:
                Sessao.cadastrar(dados)

    print("Banco de dados populado com sucesso (cinema.db).")
    print(f"- {len(Filme.listar())} filmes")
    print(f"- {len(Sala.listar())} salas")
    print(f"- {len(TipoIngresso.listar())} tipos de ingresso")
    print(f"- {len(Sessao.listar())} sessoes")


if __name__ == "__main__":
    seed()
