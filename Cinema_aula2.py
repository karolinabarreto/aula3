#Equipe
#Alexandre Harboe Azevedo (nusp - 15436950)
#Felipe Dutra Bernardo (nusp - 15451280)
#Karolina Vasconcellos Barreto (nusp - 15508831)
#Giovana Une Oyakawa (nusp - 15455343)

import datetime

filmes = []
salas = []
sessoes = []

tipo_sala = {}

class Filme:

    def __init__(self, nome=None, data_estreia=None, data_saida=None, duracao=None):
        self.codigo = None
        self.nome = nome
        self.data_estreia = data_estreia
        self.data_saida = data_saida
        self.duracao = duracao


class Sala:

    def __init__(self, numero=None, capacidade=None, tipo=None):
        self.numero = numero
        self.capacidade = capacidade
        self.tipo = tipo


class Sessao:
    def __init__(self, sala=None, filme=None, data=None, hora_inicio=None):
        self.codigo = None
        self.sala = sala
        self.filme = filme
        self.data = data
        self.hora_inicio = hora_inicio
        self.assentos = []

def _data_valida(data_str):
    try:
        datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except (ValueError, TypeError):
        return False


def pegar_sala(numero_sala):
    for sala in salas:
        if sala.numero == numero_sala:
            return sala
    return None


def _buscar_filme(codigo_filme):
    for filme in filmes:
        if filme.codigo == codigo_filme:
            return filme
    return None


def _buscar_sessao(codigo_sessao):
    for sessao in sessoes:
        if sessao.codigo == codigo_sessao:
            return sessao
    return None


# US01
def cadastrar_filme(nome, data_estreia, data_saida, duracao):
    if not nome:
        return None

    if not _data_valida(data_estreia) or not _data_valida(data_saida):
        return None

    if duracao <= 0:
        return None

    dt_estreia = datetime.datetime.strptime(data_estreia, "%d/%m/%Y")
    dt_saida = datetime.datetime.strptime(data_saida, "%d/%m/%Y")
    if dt_estreia > dt_saida:
        return None

    if any(f.nome == nome for f in filmes):
        return None

    filme = Filme(nome, data_estreia, data_saida, duracao)
    filme.codigo = len(filmes) + 1
    filmes.append(filme)
    return filme


# US02
def cadastrar_valor_ingresso(tipo, valor_ingresso):
    if tipo not in ("2D", "3D"):
        return False

    if valor_ingresso <= 0:
        return False

    tipo_sala[tipo] = valor_ingresso
    return True


# US03
def cadastrar_sala(numero, capacidade, tipo):
    if numero <= 0 or capacidade <= 0:
        return None

    if pegar_sala(numero) is not None:
        return None

    sala = Sala(numero, capacidade, tipo)
    salas.append(sala)
    return sala


# US04
def cadastrar_sessao(numero_sala, codigo_filme, data_sessao, hora_inicio):
    sala = pegar_sala(numero_sala)
    filme = _buscar_filme(codigo_filme)

    if sala is None or filme is None:
        return None

    if not _data_valida(data_sessao):
        return None

    if hora_inicio < 0 or hora_inicio > 23:
        return None

    for sessao_existente in sessoes:
        if (sessao_existente.sala.numero == numero_sala and
                sessao_existente.data == data_sessao and
                sessao_existente.hora_inicio == hora_inicio):
            return None

    sessao = Sessao(sala, filme, data_sessao, hora_inicio)
    sessao.codigo = len(sessoes) + 1
    sessao.assentos = [0] * sala.capacidade
    sessoes.append(sessao)
    return sessao


# US05
def listar_filmes_por_data(data):
    if not _data_valida(data):
        return "Data invalida."

    linhas = []
    for sessao in sessoes:
        if sessao.data == data and 0 in sessao.assentos:
            valor = tipo_sala.get(sessao.sala.tipo, 0)
            linhas.append("{}: {}, sala {} ({}), {}h, {} reais.".format(
                sessao.codigo, sessao.filme.nome, sessao.sala.numero,
                sessao.sala.tipo, sessao.hora_inicio, valor
            ))

    if not linhas:
        return "Nenhum filme no dia escolhido."

    return "\n".join(linhas)


# US06
def comprarIngressos(codigo_sessao, assentos, tipos_ingresso):
    sessao = _buscar_sessao(codigo_sessao)
    if sessao is None:
        return 0

    if len(assentos) != len(tipos_ingresso):
        return 0

    capacidade = len(sessao.assentos)
    for assento, tipo_ingresso in zip(assentos, tipos_ingresso):
        if assento < 1 or assento > capacidade or sessao.assentos[assento - 1] != 0:
            return 0
        if tipo_ingresso not in (0, 1):
            return 0

    valor_base = tipo_sala.get(sessao.sala.tipo, 0)
    total = 0
    for tipo_ingresso in tipos_ingresso:
        total += valor_base if tipo_ingresso == 0 else valor_base // 2

    for assento in assentos:
        sessao.assentos[assento - 1] = 1

    return total
