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

    # filmes em cartaz em setembro de 2026 (datas de estreia no Brasil).
    # Os cartazes ficam em static/cartazes/ (veja o README).
    filmes_exemplo = [
        {"nome": "Vingadores: Ultimato Encore", "data_estreia": "24/09/2026", "data_saida": "22/10/2026",
         "duracao": 181, "cartaz": "/static/cartazes/vingadores-ultimato-encore.jpg"},
        {"nome": "Homem-Aranha: Um Novo Dia", "data_estreia": "29/07/2026", "data_saida": "15/10/2026",
         "duracao": 150, "cartaz": "/static/cartazes/homem-aranha-um-novo-dia.jpg"},
        {"nome": "Minha Melhor Amiga", "data_estreia": "03/09/2026", "data_saida": "08/10/2026",
         "duracao": 100, "cartaz": "/static/cartazes/minha-melhor-amiga.jpg"},
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
        f, sl = filmes_criados, salas_criadas
        sessoes_exemplo = [
            # (sala, filme, data, hora)
            (sl[1], f[0], "24/09/2026", 19), (sl[1], f[0], "25/09/2026", 21),
            (sl[2], f[1], "24/09/2026", 21), (sl[2], f[1], "25/09/2026", 18),
            (sl[0], f[2], "24/09/2026", 16), (sl[0], f[2], "26/09/2026", 15),
        ]
        for sala, filme, data, hora in sessoes_exemplo:
            dados = {"sala_id": sala.id, "filme_id": filme.id, "data": data, "hora_inicio": hora}
            if Sessao.validar(dados) is None and not Sessao.existe_conflito(sala.id, data, hora):
                Sessao.cadastrar(dados)

    print("Banco de dados populado com sucesso (cinema.db).")
    print(f"- {len(Filme.listar())} filmes")
    print(f"- {len(Sala.listar())} salas")
    print(f"- {len(TipoIngresso.listar())} tipos de ingresso")
    print(f"- {len(Sessao.listar())} sessoes")


if __name__ == "__main__":
    seed()
