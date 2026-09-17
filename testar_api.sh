#!/bin/bash
# Script de teste da API do cinema.
# Sobe o servidor Flask (se ainda nao estiver rodando), cadastra dados de
# teste e verifica se cada validacao responde com o status HTTP esperado.
#
# Como usar:
#   chmod +x testar_api.sh
#   ./testar_api.sh
#
# Funciona em Linux, Mac e Windows (Git Bash). Os arquivos temporarios sao
# criados na propria pasta do projeto (nao em /tmp), porque o /tmp do Git
# Bash e o /tmp que o curl.exe do Windows enxerga nem sempre sao o mesmo
# lugar - isso e o que causava o erro "FileNotFoundError" no Windows.

BASE="http://127.0.0.1:5000"
RESP_FILE="./.resposta_teste.json"
TOTAL=0
FALHOU=0

# ---------- sobe o servidor se ainda nao estiver rodando ----------
PYTHON_CMD="python3"
command -v python3 >/dev/null 2>&1 || PYTHON_CMD="python"

if ! curl -s -o /dev/null "$BASE/"; then
    echo "Servidor nao esta rodando, subindo com '$PYTHON_CMD app.py'..."
    ("$PYTHON_CMD" app.py > "./.cinema_app_teste.log" 2>&1 &)
    sleep 2
fi

# ---------- funcao auxiliar de teste ----------
# testar "descricao" METODO "url" 'corpo_json' status_esperado
testar() {
    DESC="$1"; METODO="$2"; URL="$3"; CORPO="$4"; ESPERADO="$5"
    TOTAL=$((TOTAL + 1))

    if [ -n "$CORPO" ]; then
        STATUS=$(curl -s -o "$RESP_FILE" -w "%{http_code}" -X "$METODO" "$BASE$URL" \
            -H "Content-Type: application/json" -d "$CORPO")
    else
        STATUS=$(curl -s -o "$RESP_FILE" -w "%{http_code}" -X "$METODO" "$BASE$URL")
    fi

    if [ "$STATUS" == "$ESPERADO" ]; then
        echo "OK   [$STATUS] $DESC"
    else
        echo "FALHOU [esperado $ESPERADO, veio $STATUS] $DESC"
        echo "       resposta: $(cat "$RESP_FILE" 2>/dev/null)"
        FALHOU=$((FALHOU + 1))
    fi
}

# extrai o id do corpo da ultima resposta (sem depender de python)
ultimo_id() {
    grep -o '"id"[[:space:]]*:[[:space:]]*[0-9]*' "$RESP_FILE" | head -1 | grep -o '[0-9]*$'
}

echo "===================== FILMES ====================="
testar "cadastrar filme valido" POST /api/filmes \
    '{"nome":"Duna: Parte 2","data_estreia":"01/03/2024","data_saida":"01/06/2024","duracao":166}' 201
FILME_ID=$(ultimo_id)

testar "cadastrar filme sem nome (invalido)" POST /api/filmes \
    '{"data_estreia":"01/03/2024","data_saida":"01/06/2024","duracao":166}' 400

testar "cadastrar filme com data invalida" POST /api/filmes \
    '{"nome":"Filme X","data_estreia":"2024-03-01","data_saida":"01/06/2024","duracao":100}' 400

testar "cadastrar filme com duracao negativa" POST /api/filmes \
    '{"nome":"Filme Y","data_estreia":"01/03/2024","data_saida":"01/06/2024","duracao":-10}' 400

testar "cadastrar filme com estreia depois da saida" POST /api/filmes \
    '{"nome":"Filme Z","data_estreia":"01/06/2024","data_saida":"01/03/2024","duracao":100}' 400

testar "listar filmes" GET /api/filmes "" 200
testar "buscar filme existente" GET "/api/filmes/$FILME_ID" "" 200
testar "buscar filme inexistente" GET /api/filmes/9999 "" 404
testar "editar filme valido" PUT "/api/filmes/$FILME_ID" '{"duracao":170}' 200
testar "editar filme inexistente" PUT /api/filmes/9999 '{"duracao":170}' 404
testar "editar filme com duracao invalida" PUT "/api/filmes/$FILME_ID" '{"duracao":0}' 400

echo
echo "===================== SALAS ====================="
testar "cadastrar sala valida" POST /api/salas '{"numero":1,"capacidade":50,"tipo":"2D"}' 201
SALA_ID=$(ultimo_id)

testar "cadastrar sala com tipo invalido" POST /api/salas \
    '{"numero":2,"capacidade":50,"tipo":"4D"}' 400
testar "cadastrar sala com capacidade negativa" POST /api/salas \
    '{"numero":3,"capacidade":-5,"tipo":"2D"}' 400

testar "listar salas" GET /api/salas "" 200
testar "buscar sala existente" GET "/api/salas/$SALA_ID" "" 200
testar "buscar sala inexistente" GET /api/salas/9999 "" 404
testar "editar sala valida" PUT "/api/salas/$SALA_ID" '{"capacidade":80}' 200
testar "editar sala inexistente" PUT /api/salas/9999 '{"capacidade":80}' 404
testar "remover sala inexistente" DELETE /api/salas/9999 "" 404

echo
echo "================ TIPOS DE INGRESSO ================"
testar "cadastrar tipo de ingresso valido" POST /api/tipos-ingresso \
    '{"tipo":"2D","valor_ingresso":30}' 201
TIPO_ID=$(ultimo_id)

testar "cadastrar tipo invalido (nao e 2D/3D)" POST /api/tipos-ingresso \
    '{"tipo":"4D","valor_ingresso":30}' 400
testar "cadastrar tipo com valor negativo" POST /api/tipos-ingresso \
    '{"tipo":"3D","valor_ingresso":-10}' 400

testar "listar tipos de ingresso" GET /api/tipos-ingresso "" 200
testar "buscar tipo existente" GET "/api/tipos-ingresso/$TIPO_ID" "" 200
testar "buscar tipo inexistente" GET /api/tipos-ingresso/9999 "" 404
testar "editar tipo valido" PUT "/api/tipos-ingresso/$TIPO_ID" '{"valor_ingresso":35}' 200
testar "remover tipo inexistente" DELETE /api/tipos-ingresso/9999 "" 404

echo
echo "===================== SESSOES ====================="
testar "cadastrar sessao valida" POST /api/sessoes \
    "{\"sala_id\":$SALA_ID,\"filme_id\":$FILME_ID,\"data\":\"10/03/2024\",\"hora_inicio\":20}" 201
SESSAO_ID=$(ultimo_id)

testar "cadastrar sessao com sala inexistente" POST /api/sessoes \
    "{\"sala_id\":9999,\"filme_id\":$FILME_ID,\"data\":\"10/03/2024\",\"hora_inicio\":21}" 400
testar "cadastrar sessao com filme inexistente" POST /api/sessoes \
    "{\"sala_id\":$SALA_ID,\"filme_id\":9999,\"data\":\"10/03/2024\",\"hora_inicio\":21}" 400
testar "cadastrar sessao com hora fora do intervalo (0-23)" POST /api/sessoes \
    "{\"sala_id\":$SALA_ID,\"filme_id\":$FILME_ID,\"data\":\"10/03/2024\",\"hora_inicio\":25}" 400
testar "cadastrar sessao duplicada (mesma sala/data/hora)" POST /api/sessoes \
    "{\"sala_id\":$SALA_ID,\"filme_id\":$FILME_ID,\"data\":\"10/03/2024\",\"hora_inicio\":20}" 409

testar "listar sessoes" GET /api/sessoes "" 200
testar "listar sessoes filtrando por data" GET "/api/sessoes?data=10/03/2024" "" 200
testar "buscar sessao existente" GET "/api/sessoes/$SESSAO_ID" "" 200
testar "buscar sessao inexistente" GET /api/sessoes/9999 "" 404
testar "editar sessao valida" PUT "/api/sessoes/$SESSAO_ID" '{"hora_inicio":21}' 200
testar "editar sessao inexistente" PUT /api/sessoes/9999 '{"hora_inicio":21}' 404

echo
echo "================== REMOCAO (limpeza) =================="
testar "remover sessao" DELETE "/api/sessoes/$SESSAO_ID" "" 200
testar "remover tipo de ingresso" DELETE "/api/tipos-ingresso/$TIPO_ID" "" 200
testar "remover sala" DELETE "/api/salas/$SALA_ID" "" 200
testar "remover filme" DELETE "/api/filmes/$FILME_ID" "" 200

echo
echo "===================================================="
echo "Total de testes: $TOTAL | Falhas: $FALHOU"
if [ "$FALHOU" -eq 0 ]; then
    echo "TODOS OS TESTES PASSARAM."
else
    echo "Existem testes com falha, veja os detalhes acima."
fi

rm -f "$RESP_FILE"
