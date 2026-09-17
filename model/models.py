import sqlite3
import datetime

DB_NAME = "cinema.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_estreia TEXT NOT NULL,
        data_saida TEXT NOT NULL,
        duracao INTEGER NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL,
        capacidade INTEGER NOT NULL,
        tipo TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sala_id INTEGER NOT NULL,
        filme_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora_inicio INTEGER NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS tipos_ingresso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        valor_ingresso REAL NOT NULL
    )""")
    conn.commit()
    conn.close()


def data_valida(data_str):
    try:
        datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except (ValueError, TypeError):
        return False


# ---------- FILMES ----------

def criar_filme(nome, data_estreia, data_saida, duracao):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO filmes (nome, data_estreia, data_saida, duracao) VALUES (?, ?, ?, ?)",
        (nome, data_estreia, data_saida, duracao),
    )
    conn.commit()
    filme = conn.execute("SELECT * FROM filmes WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(filme)


def listar_filmes():
    conn = get_conn()
    filmes = conn.execute("SELECT * FROM filmes").fetchall()
    conn.close()
    return [dict(f) for f in filmes]


def buscar_filme(filme_id):
    conn = get_conn()
    filme = conn.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,)).fetchone()
    conn.close()
    return dict(filme) if filme else None


def atualizar_filme(filme_id, nome, data_estreia, data_saida, duracao):
    conn = get_conn()
    conn.execute(
        "UPDATE filmes SET nome=?, data_estreia=?, data_saida=?, duracao=? WHERE id=?",
        (nome, data_estreia, data_saida, duracao, filme_id),
    )
    conn.commit()
    conn.close()
    return buscar_filme(filme_id)


def remover_filme(filme_id):
    conn = get_conn()
    conn.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))
    conn.commit()
    conn.close()


# ---------- SALAS ----------

def criar_sala(numero, capacidade, tipo):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO salas (numero, capacidade, tipo) VALUES (?, ?, ?)",
        (numero, capacidade, tipo),
    )
    conn.commit()
    sala = conn.execute("SELECT * FROM salas WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(sala)


def listar_salas():
    conn = get_conn()
    salas = conn.execute("SELECT * FROM salas").fetchall()
    conn.close()
    return [dict(s) for s in salas]


def buscar_sala(sala_id):
    conn = get_conn()
    sala = conn.execute("SELECT * FROM salas WHERE id = ?", (sala_id,)).fetchone()
    conn.close()
    return dict(sala) if sala else None


def atualizar_sala(sala_id, numero, capacidade, tipo):
    conn = get_conn()
    conn.execute(
        "UPDATE salas SET numero=?, capacidade=?, tipo=? WHERE id=?",
        (numero, capacidade, tipo, sala_id),
    )
    conn.commit()
    conn.close()
    return buscar_sala(sala_id)


def remover_sala(sala_id):
    conn = get_conn()
    conn.execute("DELETE FROM salas WHERE id = ?", (sala_id,))
    conn.commit()
    conn.close()


# ---------- SESSOES ----------

def criar_sessao(sala_id, filme_id, data, hora_inicio):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO sessoes (sala_id, filme_id, data, hora_inicio) VALUES (?, ?, ?, ?)",
        (sala_id, filme_id, data, hora_inicio),
    )
    conn.commit()
    sessao = conn.execute("SELECT * FROM sessoes WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(sessao)


def listar_sessoes(data=None):
    conn = get_conn()
    if data:
        sessoes = conn.execute("SELECT * FROM sessoes WHERE data = ?", (data,)).fetchall()
    else:
        sessoes = conn.execute("SELECT * FROM sessoes").fetchall()
    conn.close()
    return [dict(s) for s in sessoes]


def buscar_sessao(sessao_id):
    conn = get_conn()
    sessao = conn.execute("SELECT * FROM sessoes WHERE id = ?", (sessao_id,)).fetchone()
    conn.close()
    return dict(sessao) if sessao else None


def existe_conflito_sessao(sala_id, data, hora_inicio, ignorar_id=None):
    conn = get_conn()
    if ignorar_id:
        conflito = conn.execute(
            "SELECT * FROM sessoes WHERE sala_id=? AND data=? AND hora_inicio=? AND id != ?",
            (sala_id, data, hora_inicio, ignorar_id),
        ).fetchone()
    else:
        conflito = conn.execute(
            "SELECT * FROM sessoes WHERE sala_id=? AND data=? AND hora_inicio=?",
            (sala_id, data, hora_inicio),
        ).fetchone()
    conn.close()
    return conflito is not None


def atualizar_sessao(sessao_id, sala_id, filme_id, data, hora_inicio):
    conn = get_conn()
    conn.execute(
        "UPDATE sessoes SET sala_id=?, filme_id=?, data=?, hora_inicio=? WHERE id=?",
        (sala_id, filme_id, data, hora_inicio, sessao_id),
    )
    conn.commit()
    conn.close()
    return buscar_sessao(sessao_id)


def remover_sessao(sessao_id):
    conn = get_conn()
    conn.execute("DELETE FROM sessoes WHERE id = ?", (sessao_id,))
    conn.commit()
    conn.close()


# ---------- TIPOS DE INGRESSO ----------

def criar_tipo_ingresso(tipo, valor_ingresso):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO tipos_ingresso (tipo, valor_ingresso) VALUES (?, ?)",
        (tipo, valor_ingresso),
    )
    conn.commit()
    tipo_ingresso = conn.execute("SELECT * FROM tipos_ingresso WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(tipo_ingresso)


def listar_tipos_ingresso():
    conn = get_conn()
    tipos = conn.execute("SELECT * FROM tipos_ingresso").fetchall()
    conn.close()
    return [dict(t) for t in tipos]


def buscar_tipo_ingresso(tipo_id):
    conn = get_conn()
    tipo_ingresso = conn.execute("SELECT * FROM tipos_ingresso WHERE id = ?", (tipo_id,)).fetchone()
    conn.close()
    return dict(tipo_ingresso) if tipo_ingresso else None


def atualizar_tipo_ingresso(tipo_id, tipo, valor_ingresso):
    conn = get_conn()
    conn.execute(
        "UPDATE tipos_ingresso SET tipo=?, valor_ingresso=? WHERE id=?",
        (tipo, valor_ingresso, tipo_id),
    )
    conn.commit()
    conn.close()
    return buscar_tipo_ingresso(tipo_id)


def remover_tipo_ingresso(tipo_id):
    conn = get_conn()
    conn.execute("DELETE FROM tipos_ingresso WHERE id = ?", (tipo_id,))
    conn.commit()
    conn.close()
