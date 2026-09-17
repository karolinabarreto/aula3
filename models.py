import os
import sqlite3
import datetime

# Caminho fixo, relativo a pasta ONDE ESTA ESTE ARQUIVO (models.py) - nao
# depende de qual pasta voce esta quando roda "python3 app.py". Isso evita
# o problema classico de rodar o comando de outro lugar e a aplicacao
# criar um cinema.db novo e vazio ali, em vez de usar o que ja existe.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "cinema.db")


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
        hora_inicio INTEGER NOT NULL,
        assentos TEXT NOT NULL DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS tipos_ingresso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        valor_ingresso REAL NOT NULL
    )""")
    conn.commit()
    conn.close()


# mesma funcao auxiliar do cinema.py original, usada pelas 4 classes
def _data_valida(data_str):
    try:
        datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except (ValueError, TypeError):
        return False


# ==================== FILME ====================
# Mesmos atributos do cinema.py original: nome, data_estreia, data_saida,
# duracao (+ "id", que faz o papel do antigo "codigo").

class Filme:

    def __init__(self, id=None, nome=None, data_estreia=None, data_saida=None, duracao=None):
        self.id = id
        self.nome = nome
        self.data_estreia = data_estreia
        self.data_saida = data_saida
        self.duracao = duracao

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_estreia": self.data_estreia,
            "data_saida": self.data_saida,
            "duracao": self.duracao,
        }

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Filme(row["id"], row["nome"], row["data_estreia"], row["data_saida"], row["duracao"])

    # mesmas regras da funcao cadastrar_filme do cinema.py original
    @staticmethod
    def validar(dados):
        nome = dados.get("nome")
        data_estreia = dados.get("data_estreia")
        data_saida = dados.get("data_saida")
        duracao = dados.get("duracao")

        if not nome or not _data_valida(data_estreia) or not _data_valida(data_saida) \
                or not isinstance(duracao, int) or duracao <= 0:
            return "Dados invalidos. Verifique nome, datas (dd/mm/aaaa) e duracao."

        dt_estreia = datetime.datetime.strptime(data_estreia, "%d/%m/%Y")
        dt_saida = datetime.datetime.strptime(data_saida, "%d/%m/%Y")
        if dt_estreia > dt_saida:
            return "Data de estreia nao pode ser posterior a data de saida."

        return None

    @staticmethod
    def cadastrar(dados):
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO filmes (nome, data_estreia, data_saida, duracao) VALUES (?, ?, ?, ?)",
            (dados["nome"], dados["data_estreia"], dados["data_saida"], dados["duracao"]),
        )
        conn.commit()
        conn.close()
        return Filme.buscar(cur.lastrowid)

    @staticmethod
    def listar():
        conn = get_conn()
        filmes = conn.execute("SELECT * FROM filmes").fetchall()
        conn.close()
        return [Filme._from_row(f) for f in filmes]

    @staticmethod
    def buscar(filme_id):
        conn = get_conn()
        row = conn.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,)).fetchone()
        conn.close()
        return Filme._from_row(row)

    def atualizar(self, dados):
        self.nome = dados.get("nome", self.nome)
        self.data_estreia = dados.get("data_estreia", self.data_estreia)
        self.data_saida = dados.get("data_saida", self.data_saida)
        self.duracao = dados.get("duracao", self.duracao)

        conn = get_conn()
        conn.execute(
            "UPDATE filmes SET nome=?, data_estreia=?, data_saida=?, duracao=? WHERE id=?",
            (self.nome, self.data_estreia, self.data_saida, self.duracao, self.id),
        )
        conn.commit()
        conn.close()
        return self

    def remover(self):
        conn = get_conn()
        conn.execute("DELETE FROM filmes WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()


# ==================== SALA ====================
# Mesmos atributos do cinema.py original: numero, capacidade, tipo.

class Sala:

    def __init__(self, id=None, numero=None, capacidade=None, tipo=None):
        self.id = id
        self.numero = numero
        self.capacidade = capacidade
        self.tipo = tipo

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "capacidade": self.capacidade,
            "tipo": self.tipo,
        }

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Sala(row["id"], row["numero"], row["capacidade"], row["tipo"])

    # mesmas regras da funcao cadastrar_sala do cinema.py original
    @staticmethod
    def validar(dados):
        numero = dados.get("numero")
        capacidade = dados.get("capacidade")
        tipo = dados.get("tipo")

        if not isinstance(numero, int) or numero <= 0 or not isinstance(capacidade, int) \
                or capacidade <= 0 or tipo not in ("2D", "3D"):
            return "Dados invalidos. Verifique numero, capacidade e tipo (2D ou 3D)."

        return None

    @staticmethod
    def cadastrar(dados):
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO salas (numero, capacidade, tipo) VALUES (?, ?, ?)",
            (dados["numero"], dados["capacidade"], dados["tipo"]),
        )
        conn.commit()
        conn.close()
        return Sala.buscar(cur.lastrowid)

    @staticmethod
    def listar():
        conn = get_conn()
        salas = conn.execute("SELECT * FROM salas").fetchall()
        conn.close()
        return [Sala._from_row(s) for s in salas]

    @staticmethod
    def buscar(sala_id):
        conn = get_conn()
        row = conn.execute("SELECT * FROM salas WHERE id = ?", (sala_id,)).fetchone()
        conn.close()
        return Sala._from_row(row)

    def atualizar(self, dados):
        self.numero = dados.get("numero", self.numero)
        self.capacidade = dados.get("capacidade", self.capacidade)
        self.tipo = dados.get("tipo", self.tipo)

        conn = get_conn()
        conn.execute(
            "UPDATE salas SET numero=?, capacidade=?, tipo=? WHERE id=?",
            (self.numero, self.capacidade, self.tipo, self.id),
        )
        conn.commit()
        conn.close()
        return self

    def remover(self):
        conn = get_conn()
        conn.execute("DELETE FROM salas WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()


# ==================== SESSAO ====================
# Mesmos atributos do cinema.py original: sala, filme, data, hora_inicio e
# assentos (lista de 0/1, um por lugar da sala - 0 = livre, 1 = ocupado).
# Aqui guardamos apenas a referencia (sala_id / filme_id) em vez do objeto
# inteiro, que e o jeito normal de representar isso em um banco de dados.

class Sessao:

    def __init__(self, id=None, sala_id=None, filme_id=None, data=None, hora_inicio=None, assentos=None):
        self.id = id
        self.sala_id = sala_id
        self.filme_id = filme_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.assentos = assentos if assentos is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "sala_id": self.sala_id,
            "filme_id": self.filme_id,
            "data": self.data,
            "hora_inicio": self.hora_inicio,
            "assentos": self.assentos,
        }

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        assentos_str = row["assentos"] or ""
        assentos = [int(a) for a in assentos_str.split(",") if a != ""]
        return Sessao(row["id"], row["sala_id"], row["filme_id"], row["data"], row["hora_inicio"], assentos)

    # mesmas regras da funcao cadastrar_sessao do cinema.py original
    @staticmethod
    def validar(dados):
        sala_id = dados.get("sala_id")
        filme_id = dados.get("filme_id")
        data = dados.get("data")
        hora_inicio = dados.get("hora_inicio")

        if Sala.buscar(sala_id) is None or Filme.buscar(filme_id) is None or not _data_valida(data) \
                or not isinstance(hora_inicio, int) or hora_inicio < 0 or hora_inicio > 23:
            return "Dados invalidos. Verifique sala_id, filme_id, data e hora_inicio (0-23)."

        return None

    @staticmethod
    def existe_conflito(sala_id, data, hora_inicio, ignorar_id=None):
        conn = get_conn()
        conflito = conn.execute(
            "SELECT * FROM sessoes WHERE sala_id=? AND data=? AND hora_inicio=? AND id != ?",
            (sala_id, data, hora_inicio, ignorar_id or 0),
        ).fetchone()
        conn.close()
        return conflito is not None

    @staticmethod
    def cadastrar(dados):
        # igual ao original: sessao.assentos = [0] * sala.capacidade
        sala = Sala.buscar(dados["sala_id"])
        assentos = [0] * sala.capacidade
        assentos_str = ",".join(str(a) for a in assentos)

        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO sessoes (sala_id, filme_id, data, hora_inicio, assentos) VALUES (?, ?, ?, ?, ?)",
            (dados["sala_id"], dados["filme_id"], dados["data"], dados["hora_inicio"], assentos_str),
        )
        conn.commit()
        conn.close()
        return Sessao.buscar(cur.lastrowid)

    @staticmethod
    def listar(data=None):
        conn = get_conn()
        if data:
            sessoes = conn.execute("SELECT * FROM sessoes WHERE data = ?", (data,)).fetchall()
        else:
            sessoes = conn.execute("SELECT * FROM sessoes").fetchall()
        conn.close()
        return [Sessao._from_row(s) for s in sessoes]

    @staticmethod
    def buscar(sessao_id):
        conn = get_conn()
        row = conn.execute("SELECT * FROM sessoes WHERE id = ?", (sessao_id,)).fetchone()
        conn.close()
        return Sessao._from_row(row)

    def atualizar(self, dados):
        nova_sala_id = dados.get("sala_id", self.sala_id)

        # se a sala mudou, os assentos sao reiniciados com a nova capacidade
        if nova_sala_id != self.sala_id:
            nova_sala = Sala.buscar(nova_sala_id)
            self.assentos = [0] * nova_sala.capacidade

        self.sala_id = nova_sala_id
        self.filme_id = dados.get("filme_id", self.filme_id)
        self.data = dados.get("data", self.data)
        self.hora_inicio = dados.get("hora_inicio", self.hora_inicio)

        assentos_str = ",".join(str(a) for a in self.assentos)
        conn = get_conn()
        conn.execute(
            "UPDATE sessoes SET sala_id=?, filme_id=?, data=?, hora_inicio=?, assentos=? WHERE id=?",
            (self.sala_id, self.filme_id, self.data, self.hora_inicio, assentos_str, self.id),
        )
        conn.commit()
        conn.close()
        return self

    def remover(self):
        conn = get_conn()
        conn.execute("DELETE FROM sessoes WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()


# ==================== TIPO DE INGRESSO ====================
# No cinema.py original isso era um dicionario (tipo_sala) preenchido pela
# funcao cadastrar_valor_ingresso. Aqui vira uma classe, no mesmo espirito
# das outras, para ficar consistente com o resto da aplicacao.

class TipoIngresso:

    def __init__(self, id=None, tipo=None, valor_ingresso=None):
        self.id = id
        self.tipo = tipo
        self.valor_ingresso = valor_ingresso

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "valor_ingresso": self.valor_ingresso,
        }

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return TipoIngresso(row["id"], row["tipo"], row["valor_ingresso"])

    # mesmas regras da funcao cadastrar_valor_ingresso do cinema.py original
    @staticmethod
    def validar(dados):
        tipo = dados.get("tipo")
        valor_ingresso = dados.get("valor_ingresso")

        if tipo not in ("2D", "3D") or not isinstance(valor_ingresso, (int, float)) \
                or isinstance(valor_ingresso, bool) or valor_ingresso <= 0:
            return "Dados invalidos. Tipo deve ser 2D ou 3D e valor deve ser positivo."

        return None

    @staticmethod
    def cadastrar(dados):
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO tipos_ingresso (tipo, valor_ingresso) VALUES (?, ?)",
            (dados["tipo"], dados["valor_ingresso"]),
        )
        conn.commit()
        conn.close()
        return TipoIngresso.buscar(cur.lastrowid)

    @staticmethod
    def listar():
        conn = get_conn()
        tipos = conn.execute("SELECT * FROM tipos_ingresso").fetchall()
        conn.close()
        return [TipoIngresso._from_row(t) for t in tipos]

    @staticmethod
    def buscar(tipo_id):
        conn = get_conn()
        row = conn.execute("SELECT * FROM tipos_ingresso WHERE id = ?", (tipo_id,)).fetchone()
        conn.close()
        return TipoIngresso._from_row(row)

    def atualizar(self, dados):
        self.tipo = dados.get("tipo", self.tipo)
        self.valor_ingresso = dados.get("valor_ingresso", self.valor_ingresso)

        conn = get_conn()
        conn.execute(
            "UPDATE tipos_ingresso SET tipo=?, valor_ingresso=? WHERE id=?",
            (self.tipo, self.valor_ingresso, self.id),
        )
        conn.commit()
        conn.close()
        return self

    def remover(self):
        conn = get_conn()
        conn.execute("DELETE FROM tipos_ingresso WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
