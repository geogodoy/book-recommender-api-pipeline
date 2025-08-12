# Referência da API

Para documentação interativa, acesse `http://localhost:8000/docs` (Swagger) ou `http://localhost:8000/redoc` (ReDoc).

## URLs Importantes

| Recurso | URL | Descrição |
|---------|-----|-----------|
| API Principal | `http://localhost:8000` | Endpoint raiz |
| Documentação Swagger | `http://localhost:8000/docs` | Interface interativa (recomendado) |
| Documentação ReDoc | `http://localhost:8000/redoc` | Documentação alternativa |
| Health Check | `http://localhost:8000/api/v1/health` | Status da API |
| Status Rápido | `http://localhost:8000/api/v1/status` | Verificação básica |

## Schemas de Dados

### Schema do Livro (Book)
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": "Three",
  "availability": "In stock",
  "category": "Poetry",
  "image_url": "http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
  "link": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

### Schema de Health Check
```json
{
  "status": "healthy",
  "database_connected": true,
  "total_books": 1000
}
```

### Schema de Estatísticas Gerais
```json
{
  "total_books": 1000,
  "average_price": 35.67,
  "rating_distribution": {
    "One": 50,
    "Two": 100,
    "Three": 200,
    "Four": 350,
    "Five": 300
  },
  "categories_count": 50
}
```

### Schema de Estatísticas por Categoria
```json
{
  "category": "Poetry",
  "book_count": 19,
  "average_price": 42.35,
  "min_price": 13.99,
  "max_price": 57.25
}
```

## Endpoints

### Livros

#### Listar Livros
```http
GET /api/v1/books
```
- Parâmetros de Query:
  - `skip` (int, opcional): padrão 0
  - `limit` (int, opcional): padrão 100, máx 1000
- Validações: `skip >= 0`, `1 <= limit <= 1000`
- Response: `List[Book]`

#### Buscar Livro por ID
```http
GET /api/v1/books/{book_id}
```
- Path: `book_id` (int, obrigatório)
- Response: `Book`
- Códigos: `200`, `404`

#### Buscar Livros (título/categoria)
```http
GET /api/v1/books/search
```
- Query:
  - `title` (str, opcional): busca parcial, case-insensitive
  - `category` (str, opcional): nome exato, case-sensitive
  - `skip` (int, opcional)
  - `limit` (int, opcional)
- Regras: ao menos `title` ou `category`
- Response: `List[Book]`

#### Listar Categorias
```http
GET /api/v1/categories
```
- Response: `List[str]`

#### Filtrar por Faixa de Preço
```http
GET /api/v1/books/price-range
```
- Query:
  - `min_price` (float, opcional, >= 0)
  - `max_price` (float, opcional, >= 0)
  - `skip` (int, opcional)
  - `limit` (int, opcional)
- Validações: se ambos, `min_price <= max_price`
- Response: `List[Book]`

#### Top Livros Mais Bem Avaliados
```http
GET /api/v1/books/top-rated
```
- Query: `limit` (int, opcional, padrão 20, máx 100)
- Ordenação: Rating (Five → One), depois por título
- Response: `List[Book]`

### Estatísticas

#### Estatísticas Gerais
```http
GET /api/v1/stats/overview
```
- Response: `StatsOverview`

#### Estatísticas por Categoria
```http
GET /api/v1/stats/categories
```
- Response: `List[CategoryStats]`

### Monitoramento

#### Health Check Completo
```http
GET /api/v1/health
```
- Response: `HealthCheck`

#### Status Rápido
```http
GET /api/v1/status
```
- Response:
```json
{ "status": "ok", "message": "API is running" }
```

#### Status dos Dados
```http
GET /api/v1/data-status
```
- Response:
```json
{ "has_data": true, "status": "data_loaded" }
```

## Códigos de Erro

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| 400 | Bad Request | Parâmetros inválidos |
| 404 | Not Found | Livro não encontrado |
| 422 | Unprocessable Entity | Dados de entrada inválidos |
| 500 | Internal Server Error | Erro interno do servidor |

### Headers de Response

Todos os endpoints retornam:
```http
Content-Type: application/json
```

### Observações Importantes

1. Paginação: prefira `skip` e `limit` para navegação eficiente
2. Performance: estatísticas podem ser mais lentas em datasets grandes
3. Cache: resultados são calculados em tempo real (sem cache)
4. Encoding: UTF-8 para todas as strings
5. Timestamps: dados atuais não possuem campos de data/hora

## Exemplos de Uso

### cURL

- Verificar Status da API
```bash
curl -X GET "http://localhost:8000/api/v1/status" -H "accept: application/json"
```

- Health Check Completo
```bash
curl -X GET "http://localhost:8000/api/v1/health" -H "accept: application/json"
```

- Listar primeiros 5 livros
```bash
curl -X GET "http://localhost:8000/api/v1/books?skip=0&limit=5" -H "accept: application/json"
```

- Buscar por título
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=light&limit=3" -H "accept: application/json"
```

- Buscar por categoria
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?category=Poetry&limit=2" -H "accept: application/json"
```

- Listar categorias
```bash
curl -X GET "http://localhost:8000/api/v1/categories" -H "accept: application/json"
```

- Filtrar por faixa de preço
```bash
curl -X GET "http://localhost:8000/api/v1/books/price-range?min_price=50&max_price=55&limit=3" -H "accept: application/json"
```

- Top avaliados
```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated?limit=3" -H "accept: application/json"
```

- Estatísticas gerais
```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview" -H "accept: application/json"
```

- Estatísticas por categoria
```bash
curl -X GET "http://localhost:8000/api/v1/stats/categories" -H "accept: application/json"
```

### Python (requests)

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

## Testes de API (Smoke Test)

Execute o script de testes automatizados para verificar os principais endpoints:

```bash
python test_production.py
```

Saída esperada (resumo):
```
Testing Book Recommender API
... All tests passed!
```