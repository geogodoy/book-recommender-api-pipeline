# Execução da API (Runbook)

Este guia descreve como executar a API, URLs úteis de acesso, monitoramento básico, configurações de performance e como encerrar a aplicação.

Para instalação e configuração do ambiente, consulte `INSTALLATION.md`.

## Métodos de Execução

### Método 1: Script de Execução (Recomendado)
```bash
# Execute o script otimizado
python main.py
```

### Método 2: Comando Direto
```bash
# Execução direta da aplicação
python main.py
```

### Método 3: Uvicorn Manual
```bash
# Execução com controle total dos parâmetros
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Método 4: Com Ambiente Virtual
```bash
# Ative o ambiente virtual primeiro
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Execute a API
python main.py
```

### Método 5: Produção com Gunicorn
```bash
# Para ambiente de produção
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Método 6: Docker
```bash
# Usando Docker
docker run -p 8000:8000 book-recommender-api

# Ou com Docker Compose
docker-compose up
```

## URLs de Acesso

Após iniciar a API, acesse:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| API Principal | `http://localhost:8000` | Endpoint raiz |
| Documentação Swagger | `http://localhost:8000/docs` | Interface interativa da API |
| Documentação ReDoc | `http://localhost:8000/redoc` | Documentação alternativa |
| Health Check | `http://localhost:8000/api/v1/health` | Status da API |
| Status Rápido | `http://localhost:8000/api/v1/status` | Verificação básica |

## Monitoramento da Execução

Para exemplos práticos de chamadas (cURL e Python) com respostas, consulte:
- `API_EXAMPLES.md`: [Exemplos de Chamadas](./API_EXAMPLES.md)

## Performance e Otimização

### Configuração para Desenvolvimento
```bash
# Modo desenvolvimento com auto-reload
uvicorn main:app --reload --log-level info
```

### Configuração para Produção
```bash
# Múltiplos workers para melhor performance
gunicorn main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

## Parar a API

```bash
# Se executando em primeiro plano: Ctrl+C

# Se executando em background:
# Encontre o processo
ps aux | grep "python main.py"

# Mate o processo (substitua PID pelo número encontrado)
kill <PID>

# Ou force kill se necessário
kill -9 <PID>
```