# Sistema de Venda de Ingressos de Cinema — API REST (MVC)

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

## Arquitetura (MVC)

```
cinema_app/
├── app.py           # cria a app Flask, inicializa o banco e registra as rotas
├── controllers.py   # Controller: rotas da API REST, validam entrada e chamam o model
├── models.py        # Model: conexão com o banco (SQLite) e funções de CRUD
├── requirements.txt
└── README.md
```

- **Model** (`models.py`): classes `Filme`, `Sala`, `Sessao` e
  `TipoIngresso` — no mesmo espírito do `cinema.py` original (classes
  simples representando cada entidade), mas agora cada uma carrega seus
  próprios métodos de CRUD (`cadastrar`, `listar`, `buscar`, `atualizar`,
  `remover`) e persiste no SQLite em vez de listas em memória.
- **Controller** (`controllers.py`): rotas Flask que recebem a requisição,
  validam os dados e chamam os métodos das classes do model.
- **View**: como é uma API REST, a "view" é a própria resposta em JSON.

## Requisitos

- Python 3.9+
- pip

O banco (`cinema.db`, SQLite) é criado automaticamente na primeira
execução — não é preciso instalar nenhum SGBD separado.

## Como rodar

```bash
git clone <URL_DO_REPOSITORIO>
cd cinema_app

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
python3 app.py
```

A API sobe em `http://127.0.0.1:5000`.

## Documentação (Swagger)

Com o servidor rodando, acesse `http://127.0.0.1:5000/docs` para abrir a
documentação interativa (Swagger UI), com todos os endpoints, os campos
esperados em cada requisição e a possibilidade de testar direto pelo
navegador (botão "Try it out").

O arquivo com a especificação (OpenAPI 3.0) fica em
`static/openapi.json`.

## Banco de dados já populado / persistência

O banco (`cinema.db`) é criado automaticamente na primeira execução — mas
esse zip já vem com um `cinema.db` **pronto e populado** (3 filmes, 3
salas, 2 tipos de ingresso e 3 sessões de exemplo), então você já pode
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

> Por padrão o `cinema.db` fica fora do controle de versão (`.gitignore`),
> como é comum para arquivos de banco de dados. Se quiser versionar o
> banco de exemplo junto com o código, é só remover a linha `cinema.db`
> do `.gitignore` antes de subir pro repositório.

## Testando tudo de uma vez

O arquivo `testar_api.sh` cadastra dados de teste e verifica todas as
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

**Filme**
```json
{"nome": "Duna: Parte 2", "data_estreia": "01/03/2024", "data_saida": "01/06/2024", "duracao": 166}
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

- **Filme**: nome obrigatório; datas no formato `dd/mm/aaaa`; estreia não
  pode ser depois da saída; duração inteira e positiva.
- **Sala**: número e capacidade inteiros positivos; tipo `2D` ou `3D`.
- **Sessão**: sala e filme precisam existir; data válida; hora entre 0 e
  23; não pode repetir sala + data + hora.
- **Tipo de ingresso**: tipo `2D` ou `3D`; valor positivo.

Erros retornam `400` (dados inválidos), `404` (não encontrado) ou `409`
(conflito de sessão).
