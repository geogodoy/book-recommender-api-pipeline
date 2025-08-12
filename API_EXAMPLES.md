# Exemplos de Chamadas da API

Este guia reúne exemplos práticos de requisições e respostas, usando cURL e Python (requests).

Para a lista completa de rotas e schemas, consulte `API_REFERENCE.md`.

## Exemplos com cURL

### Status Rápido
```bash
curl -X GET "http://localhost:8000/api/v1/status" -H "accept: application/json"
```
Resposta esperada:
```json
{ "status": "ok", "message": "API is running" }
```

### Health Check Completo
```bash
curl -X GET "http://localhost:8000/api/v1/health" -H "accept: application/json"
```
Exemplo de resposta:
```json
{ "status": "healthy", "database_connected": true, "total_books": 1000 }
```

### Listar primeiros 5 livros
```bash
curl -X GET "http://localhost:8000/api/v1/books?skip=0&limit=5" -H "accept: application/json"
```

### Buscar por título
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=light&limit=3" -H "accept: application/json"
```

### Buscar por categoria
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?category=Poetry&limit=2" -H "accept: application/json"
```

### Listar categorias
```bash
curl -X GET "http://localhost:8000/api/v1/categories" -H "accept: application/json"
```

### Filtrar por faixa de preço
```bash
curl -X GET "http://localhost:8000/api/v1/books/price-range?min_price=50&max_price=55&limit=3" -H "accept: application/json"
```

### Top livros mais bem avaliados
```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated?limit=3" -H "accept: application/json"
```

### Estatísticas gerais
```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview" -H "accept: application/json"
```

### Estatísticas por categoria
```bash
curl -X GET "http://localhost:8000/api/v1/stats/categories" -H "accept: application/json"
```

### Status dos Dados
```bash
curl -X GET "http://localhost:8000/api/v1/data-status" -H "accept: application/json"
```
Exemplo de resposta:
```json
{ "has_data": true, "status": "data_loaded" }
```

## Exemplos com Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Health Check
print("Health:", requests.get(f"{BASE_URL}/health").json())

# Buscar livros
books = requests.get(f"{BASE_URL}/books", params={"limit": 5}).json()
print(f"Total livros: {len(books)}")

# Buscar por categoria
poetry_books = requests.get(
    f"{BASE_URL}/books/search", params={"category": "Poetry", "limit": 3}
).json()
for book in poetry_books:
    print(f"- {book['title']} (${book['price']})")

# Estatísticas
stats = requests.get(f"{BASE_URL}/stats/overview").json()
print(f"Total de livros: {stats['total_books']}")
print(f"Preço médio: ${stats['average_price']:.2f}")
```

## Teste rápido (Smoke Test)

Execute o script de testes para verificar os principais endpoints:

```bash
python test_production.py
```

Saída esperada (resumo):
```
Testing Book Recommender API
... All tests passed!
```