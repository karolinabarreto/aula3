# Sistema de Venda de Ingressos de Cinema — API REST (MVC)

[![Testes](https://github.com/giovana-oy22/aula3/actions/workflows/testes.yml/badge.svg)](https://github.com/giovana-oy22/aula3/actions/workflows/testes.yml)

## Equipe
- Alexandre Harboe Azevedo (NUSP 15436950)
- Felipe Dutra Bernardo (NUSP 15451280)
- Karolina Vasconcellos Barreto (NUSP 15508831)
- Giovana Une Oyakawa (NUSP 15455343)

## Descrição

Evolução do sistema de venda de ingressos de cinema do exercício anterior
para uma aplicação **MVC**, acessível por **API REST**, com os dados
salvos em **banco de dados** (SQLite).

Permite **cadastrar, listar, editar e remover** filmes, salas, sessões e
tipos de ingresso, mantendo os mesmos atributos do exercício anterior.

### Novidades desta versão

- Página web em `http://127.0.0.1:5000/` que exibe os filmes em cartaz
  (com cartaz), as sessões, as salas e os tipos de ingresso. Os dados são
  buscados pela API REST (`fetch` em `/api/...`).
- Novo campo `cartaz` no filme (caminho ou URL da imagem).
- 25 testes automatizados com pytest, rodando no GitHub Actions a cada commit.

## Arquitetura (MVC)

```
aula3/
├── app.py                  # create_app(): cria a app Flask, inicializa o banco e registra as rotas
├── controllers.py          # Controller: rotas da API REST, validam entrada e chamam o model
├── models.py               # Model: conexão com o banco (SQLite) e funções de CRUD
├── seed_db.py              # popula o banco com dados de exemplo
├── static/
│   ├── index.html          # View: site do cinema (consome a API REST)
│   ├── cartazes/           # imagens dos cartazes
│   └── openapi.json        # especificação da API (Swagger)
├── tests/test_api.py       # testes automatizados (pytest)
├── .github/workflows/testes.yml   # CI: roda os testes a cada push
├── requirements.txt        # dependências da aplicação
├── requirements-dev.txt    # dependências dos testes
└── README.md
```

- **Model** (`models.py`): classes `Filme`, `Sala`, `Sessao` e
  `TipoIngresso` — no mesmo espírito do `cinema.py` original (classes
  simples representando cada entidade), mas agora cada uma carrega seus
  próprios métodos de CRUD (`cadastrar`, `listar`, `buscar`, `atualizar`,
  `remover`) e persiste no SQLite em vez de listas em memória.
- **Controller** (`controllers.py`): rotas Flask que recebem a requisição,
  validam os dados e chamam os métodos das classes do model.
- **View**: a página `static/index.html`, servida em `/`, que busca os
  dados pela API REST e monta a tela no navegador. As respostas JSON da
  API também funcionam como view para outros clientes.

## Requisitos

- Python 3.10+
- pip
- Um navegador moderno (para o site)

O banco (`cinema.db`, SQLite) é criado automaticamente na primeira
execução — não é preciso instalar nenhum SGBD separado.

## Como rodar

```bash
git clone <URL_DO_REPOSITORIO>
cd aula4

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
python3 app.py
```

- Site do cinema: `http://127.0.0.1:5000/`
- Raiz da API (lista de endpoints): `http://127.0.0.1:5000/api`
- Documentação Swagger: `http://127.0.0.1:5000/docs`

## Cartazes

Os filmes de exemplo são filmes em cartaz em setembro de 2026. As imagens
ficam em `static/cartazes/` com o nome indicado no `seed_db.py` (ex.:
`homem-aranha-um-novo-dia.jpg`). Se a imagem não existir, a página mostra uma imagem
padrão. Também é possível cadastrar o `cartaz` como uma URL completa.

## Testes automatizados

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

Os testes (`tests/test_api.py`) chamam os endpoints de CRUD de filmes,
salas, sessões e tipos de ingresso usando um banco temporário. O workflow
`.github/workflows/testes.yml` roda os testes a cada `push` e o resultado
aparece no badge no topo deste README.

## Documentação (Swagger)

Com o servidor rodando, acesse `http://127.0.0.1:5000/docs` para abrir a
documentação interativa (Swagger UI), com todos os endpoints, os campos
esperados em cada requisição e a possibilidade de testar direto pelo
navegador (botão "Try it out").

O arquivo com a especificação (OpenAPI 3.0) fica em
`static/openapi.json`.

## Banco de dados já populado / persistência

O banco (`cinema.db`) é criado automaticamente na primeira execução — mas
o repositório já vem com um `cinema.db` **pronto e populado** (3 filmes com
cartaz, 3 salas, 2 tipos de ingresso e 6 sessões de exemplo), então você já pode
testar a API sem precisar cadastrar nada manualmente primeiro.

**Se o `cinema.db` já existir na pasta, a aplicação reaproveita ele** —
`python3 app.py` nunca apaga ou recria dados que já estão lá (só cria as
tabelas que ainda não existirem). Ou seja, os dados persistem entre uma
execução e outra normalmente.

Para popular (ou repopular) o banco com os dados de exemplo manualmente:
```bash
python3 seed_db.py
```

Para começar do zero (banco vazio): apague o arquivo `cinema.db` e rode
`python3 app.py` de novo — ele recria as tabelas vazias automaticamente.


## Teste manual rápido (script)

Além dos testes automatizados, o arquivo `testar_api.sh` cadastra dados de teste e verifica todas as
validações (sucesso, erro 400, 404 e 409) de uma vez. Se o servidor não
estiver rodando, ele sobe a aplicação sozinho.

```bash
chmod +x testar_api.sh
./testar_api.sh
```

No final ele mostra quantos testes passaram/falharam.

## URLs de acesso

Base: `http://127.0.0.1:5000`

| Recurso | Cadastrar | Listar | Buscar por id | Editar | Remover |
|---|---|---|---|---|---|
| Filmes | `POST /api/filmes` | `GET /api/filmes` | `GET /api/filmes/<id>` | `PUT /api/filmes/<id>` | `DELETE /api/filmes/<id>` |
| Salas | `POST /api/salas` | `GET /api/salas` | `GET /api/salas/<id>` | `PUT /api/salas/<id>` | `DELETE /api/salas/<id>` |
| Sessões | `POST /api/sessoes` | `GET /api/sessoes` (filtro opcional `?data=dd/mm/aaaa`) | `GET /api/sessoes/<id>` | `PUT /api/sessoes/<id>` | `DELETE /api/sessoes/<id>` |
| Tipos de ingresso | `POST /api/tipos-ingresso` | `GET /api/tipos-ingresso` | `GET /api/tipos-ingresso/<id>` | `PUT /api/tipos-ingresso/<id>` | `DELETE /api/tipos-ingresso/<id>` |

### Corpo esperado (JSON)

**Filme** (`cartaz` é opcional)
```json
{"nome": "Duna: Parte 2", "data_estreia": "01/03/2024", "data_saida": "01/06/2024", "duracao": 166,
 "cartaz": "/static/cartazes/duna-parte-2.svg"}
```

**Sala**
```json
{"numero": 1, "capacidade": 50, "tipo": "2D"}
```

**Sessão**
```json
{"sala_id": 1, "filme_id": 1, "data": "10/03/2024", "hora_inicio": 20}
```
Na resposta, a sessão também traz `assentos`: uma lista de 0s (livre) do
tamanho da capacidade da sala, criada automaticamente no cadastro — igual
ao `cinema.py` original.

**Tipo de ingresso**
```json
{"tipo": "2D", "valor_ingresso": 30.0}
```

## Exemplo com curl

```bash
curl -X POST http://127.0.0.1:5000/api/filmes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Duna: Parte 2","data_estreia":"01/03/2024","data_saida":"01/06/2024","duracao":166}'

curl http://127.0.0.1:5000/api/filmes
```

## Validações

- **Filme**: nome obrigatório; `cartaz`, se enviado, deve ser texto; datas no formato `dd/mm/aaaa`; estreia não
  pode ser depois da saída; duração inteira e positiva.
- **Sala**: número e capacidade inteiros positivos; tipo `2D` ou `3D`.
- **Sessão**: sala e filme precisam existir; data válida; hora entre 0 e
  23; não pode repetir sala + data + hora.
- **Tipo de ingresso**: tipo `2D` ou `3D`; valor positivo.

Erros retornam `400` (dados inválidos), `404` (não encontrado) ou `409`
(conflito de sessão).
