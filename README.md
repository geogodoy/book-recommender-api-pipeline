# Book Recommender API Pipeline

**Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering**

Uma API RESTful completa para consulta de livros com pipeline de dados automatizado, desenvolvida como parte do Tech Challenge da primeira fase do curso de Machine Learning Engineering.

## 📋 Descrição do Projeto

Este projeto implementa um **pipeline completo de dados** e uma **API RESTful robusta** para servir informações de livros extraídas via web scraping do site [Books to Scrape](https://books.toscrape.com/). 

### 🎯 Objetivos
- **Extração automatizada** de dados de livros via web scraping
- **API RESTful** performática com documentação interativa
- **Pipeline ETL** completo (Extração → Transformação → Carregamento)
- **Arquitetura escalável** para integração futura com modelos de ML
- **Containerização** com Docker para deploy simplificado

### 🔧 Características Técnicas
- **Framework:** FastAPI com documentação automática (Swagger/ReDoc)
- **Banco de Dados:** SQLite com SQLAlchemy ORM
- **Validação:** Pydantic para schemas de request/response
- **Performance:** Endpoints otimizados com indexação de banco
- **Observabilidade:** Health checks e endpoints de status

## 🏗️ Arquitetura do Sistema

```
book-recommender-api-pipeline/
├── 📁 data/                    # Camada de Dados
│   ├── books.csv              # Dados extraídos (formato raw)
│   └── books.db               # Base de dados SQLite (formato estruturado)
├── 📁 scripts/                 # Pipeline ETL
│   ├── scrape_books.py        # Extrator: Web scraping automatizado
│   └── csv_to_db.py           # Carregador: CSV → Database
├── 📁 api/                     # Camada de Aplicação
│   ├── database.py            # Configuração do ORM e modelos
│   ├── models.py              # Modelos de dados (SQLAlchemy)
│   ├── schemas.py             # Schemas de validação (Pydantic)
│   └── crud.py                # Operações de banco (CRUD)
├── 📄 main.py                  # Aplicação FastAPI principal
├── 📄 setup.py                 # Automação de setup inicial
├── 📄 requirements.txt         # Dependências do projeto
├── 📄 Dockerfile              # Containerização
└── 📄 docker-compose.yml      # Orquestração de containers
```

### 🔄 Fluxo de Dados
```
[Books to Scrape] → [Web Scraper] → [CSV] → [ETL Pipeline] → [SQLite] → [FastAPI] → [Cliente]
```

> 📊 **Documentação Detalhada:** Para uma análise completa do pipeline com diagramas interativos, métricas de performance e arquitetura detalhada, consulte [PIPELINE.md](./PIPELINE.md)

## 🚀 Instalação e Configuração

### 📋 Pré-requisitos
- **Python 3.8+** (recomendado: 3.9 ou superior)
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonagem do repositório)
- **4GB RAM** mínimo para processamento dos dados
- **Conexão com internet** para web scraping inicial

### ⚡ Setup Automático (Recomendado)

O projeto inclui um script de setup totalmente automatizado que:
- ✅ Cria ambiente virtual Python
- ✅ Instala todas as dependências
- ✅ Executa web scraping (se necessário)
- ✅ Configura o banco de dados SQLite
- ✅ Valida a instalação

```bash
# Clone o repositório
git clone <repository-url>
cd book-recommender-api-pipeline

# Execute o setup automático
python setup.py
```

**Saída esperada:**
```
🚀 Setting up Book Recommender API...
==================================================
🐍 Creating Python virtual environment...
✅ Virtual environment created successfully!
📦 Installing required dependencies...
✅ Dependencies installed successfully!
📄 No existing data found, running scraper...
🕷️  Running web scraper...
✅ Scraping completed!
🗃️  Setting up database...
✅ Database setup completed!
==================================================
✅ Setup completed successfully!
```

### 🔧 Setup Manual (Avançado)

Para maior controle do processo de instalação:

#### 1. **Preparação do Ambiente**
```bash
# Clone o repositório
git clone <repository-url>
cd book-recommender-api-pipeline

# Crie ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

#### 2. **Extração de Dados (Web Scraping)**
```bash
# Execute o scraper para obter dados atualizados
python scripts/scrape_books.py

# Verificar dados extraídos
ls -la data/books.csv
```

#### 3. **Configuração do Banco de Dados**
```bash
# Carregue dados CSV para SQLite
python scripts/csv_to_db.py

# Verificar banco criado
ls -la data/books.db
```

#### 4. **Validação da Instalação**
```bash
# Teste rápido da API
python -c "
from api.database import get_db, Book
from sqlalchemy.orm import Session
next(get_db()).query(Book).count()
print('✅ Database OK!')
"
```

### 🐳 Instalação com Docker (Opcional)

Para ambiente completamente isolado:

```bash
# Build da imagem
docker build -t book-recommender-api .

# Execução do container
docker run -p 8000:8000 book-recommender-api

# Ou usando docker-compose
docker-compose up --build
```

### 📦 Dependências do Projeto

```txt
requests==2.32.3        # Requisições HTTP para scraping
beautifulsoup4==4.12.3  # Parsing HTML
pandas==2.2.2           # Manipulação de dados
fastapi==0.116.0        # Framework web
uvicorn[standard]==0.35.0  # Servidor ASGI
python-dotenv==1.1.1    # Variáveis de ambiente
sqlalchemy==2.0.36      # ORM de banco de dados
gunicorn==21.2.0        # Servidor WSGI para produção
psutil==5.9.8           # Informações do sistema
```

### 🔍 Verificação de Problemas Comuns

**Erro de permissão no Python:**
```bash
# Use o flag --user se não tiver privilégios admin
pip install --user -r requirements.txt
```

**Erro no web scraping:**
```bash
# Verifique conectividade
curl -I https://books.toscrape.com/
# Se OK, execute novamente o scraper
python scripts/scrape_books.py
```

**Banco de dados não criado:**
```bash
# Verifique se o diretório data/ existe
mkdir -p data
# Execute novamente o carregamento
python scripts/csv_to_db.py
```

## 🎯 Executando a API

### 🚀 Métodos de Execução

#### **Método 1: Script de Execução (Recomendado)**
```bash
# Execute o script otimizado
python run_api.py
```

#### **Método 2: Comando Direto**
```bash
# Execução direta da aplicação
python main.py
```

#### **Método 3: Uvicorn Manual**
```bash
# Execução com controle total dos parâmetros
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### **Método 4: Com Ambiente Virtual**
```bash
# Ative o ambiente virtual primeiro
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Execute a API
python main.py
```

#### **Método 5: Produção com Gunicorn**
```bash
# Para ambiente de produção
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### **Método 6: Docker**
```bash
# Usando Docker
docker run -p 8000:8000 book-recommender-api

# Ou com Docker Compose
docker-compose up
```

### 📍 URLs de Acesso

Após iniciar a API, acesse:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **API Principal** | `http://localhost:8000` | Endpoint raiz |
| **Documentação Swagger** | `http://localhost:8000/docs` | Interface interativa da API |
| **Documentação ReDoc** | `http://localhost:8000/redoc` | Documentação alternativa |
| **Health Check** | `http://localhost:8000/api/v1/health` | Status da API |
| **Status Rápido** | `http://localhost:8000/api/v1/status` | Verificação básica |

### 🔧 Configuração de Ambiente

#### **Variáveis de Ambiente Suportadas**
```bash
# Porta da aplicação (padrão: 8000)
export PORT=8000

# URL do banco de dados (padrão: sqlite:///./data/books.db)
export DATABASE_URL="sqlite:///./data/books.db"

# Ambiente de execução
export ENVIRONMENT="development"  # ou "production"
```

#### **Arquivo .env (Opcional)**
```bash
# Crie um arquivo .env na raiz do projeto
PORT=8000
DATABASE_URL=sqlite:///./data/books.db
ENVIRONMENT=development
```

### 📊 Monitoramento da Execução

#### **Verificação Rápida**
```bash
# Teste se a API está respondendo
curl http://localhost:8000/api/v1/status

# Resposta esperada:
# {"status": "ok", "message": "API is running"}
```

#### **Health Check Completo**
```bash
# Verificação completa com status do banco
curl http://localhost:8000/api/v1/health

# Resposta esperada:
# {
#   "status": "healthy",
#   "database_connected": true,
#   "total_books": 1
# }
```

#### **Logs da Aplicação**
```bash
# Para ver logs detalhados durante execução
python main.py --log-level debug

# Ou usando uvicorn
uvicorn main:app --log-level debug
```

### ⚡ Performance e Otimização

#### **Configuração para Desenvolvimento**
```bash
# Modo desenvolvimento com auto-reload
uvicorn main:app --reload --log-level info
```

#### **Configuração para Produção**
```bash
# Múltiplos workers para melhor performance
gunicorn main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### 🛑 Parar a API

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

## 📚 Documentação Completa da API

### 🌐 URLs Importantes
| Recurso | URL | Descrição |
|---------|-----|-----------|
| **API Principal** | `http://localhost:8000` | Endpoint raiz |
| **Documentação Swagger** | `http://localhost:8000/docs` | Interface interativa (recomendado) |
| **Documentação ReDoc** | `http://localhost:8000/redoc` | Documentação alternativa |
| **Health Check** | `http://localhost:8000/api/v1/health` | Status da API |

### 📋 Schemas de Dados

#### **Schema do Livro (Book)**
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

#### **Schema de Health Check**
```json
{
  "status": "healthy",
  "database_connected": true,
  "total_books": 1000
}
```

#### **Schema de Estatísticas Gerais**
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

#### **Schema de Estatísticas por Categoria**
```json
{
  "category": "Poetry",
  "book_count": 19,
  "average_price": 42.35,
  "min_price": 13.99,
  "max_price": 57.25
}
```

### 🔗 Endpoints Principais

#### **📖 Listar Livros**
```http
GET /api/v1/books
```

**Parâmetros de Query:**
- `skip` (int, opcional): Número de livros a pular (padrão: 0)
- `limit` (int, opcional): Número de livros a retornar (padrão: 100, máx: 1000)

**Validações:**
- `skip >= 0`
- `1 <= limit <= 1000`

**Response:** `List[Book]`

---

#### **🔍 Buscar Livro por ID**
```http
GET /api/v1/books/{book_id}
```

**Parâmetros de Path:**
- `book_id` (int, obrigatório): ID único do livro

**Response:** `Book`

**Códigos de Status:**
- `200`: Livro encontrado
- `404`: Livro não encontrado

---

#### **🔎 Buscar Livros**
```http
GET /api/v1/books/search
```

**Parâmetros de Query:**
- `title` (str, opcional): Busca parcial no título do livro
- `category` (str, opcional): Nome exato da categoria
- `skip` (int, opcional): Paginação (padrão: 0)
- `limit` (int, opcional): Limite de resultados (padrão: 100)

**Validações:**
- Pelo menos um parâmetro (`title` ou `category`) é obrigatório
- Busca por título é case-insensitive
- Busca por categoria é case-sensitive e exata

**Response:** `List[Book]`

---

#### **📂 Listar Categorias**
```http
GET /api/v1/categories
```

**Response:** `List[str]`
```json
[
  "Travel",
  "Mystery",
  "Poetry",
  "Fiction",
  "..."
]
```

---

#### **💰 Filtrar por Faixa de Preço**
```http
GET /api/v1/books/price-range
```

**Parâmetros de Query:**
- `min_price` (float, opcional): Preço mínimo (>= 0)
- `max_price` (float, opcional): Preço máximo (>= 0)
- `skip` (int, opcional): Paginação (padrão: 0)
- `limit` (int, opcional): Limite de resultados (padrão: 100)

**Validações:**
- Se ambos informados: `min_price <= max_price`
- Preços devem ser >= 0

**Response:** `List[Book]`

---

#### **⭐ Top Livros Mais Bem Avaliados**
```http
GET /api/v1/books/top-rated
```

**Parâmetros de Query:**
- `limit` (int, opcional): Número de livros a retornar (padrão: 20, máx: 100)

**Ordenação:** Rating (Five → Four → Three → Two → One), depois por título

**Response:** `List[Book]`

### 📊 Endpoints de Estatísticas

#### **📈 Estatísticas Gerais**
```http
GET /api/v1/stats/overview
```

**Response:** `StatsOverview`

Retorna contagem total de livros, preço médio, distribuição de ratings e número de categorias.

---

#### **📊 Estatísticas por Categoria**
```http
GET /api/v1/stats/categories
```

**Response:** `List[CategoryStats]`

Para cada categoria: contagem de livros, preço médio, preço mínimo e máximo.

### 🔧 Endpoints de Monitoramento

#### **❤️ Health Check Completo**
```http
GET /api/v1/health
```

**Response:** `HealthCheck`

Verifica conectividade com banco de dados e integridade dos dados.

---

#### **⚡ Status Rápido**
```http
GET /api/v1/status
```

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

Endpoint ultra-rápido para verificação básica.

---

#### **💾 Status dos Dados**
```http
GET /api/v1/data-status
```

**Response:**
```json
{
  "has_data": true,
  "status": "data_loaded"
}
```

Verificação específica da existência de dados no banco.

### 🚫 Códigos de Erro

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| **400** | Bad Request | Parâmetros inválidos |
| **404** | Not Found | Livro não encontrado |
| **422** | Unprocessable Entity | Dados de entrada inválidos |
| **500** | Internal Server Error | Erro interno do servidor |

### 🔒 Headers de Response

Todos os endpoints retornam:
```http
Content-Type: application/json
```

### 📝 Observações Importantes

1. **Paginação:** Sempre use os parâmetros `skip` e `limit` para navegação eficiente
2. **Performance:** Endpoints de estatísticas podem ser mais lentos em datasets grandes
3. **Cache:** Resultados são calculados em tempo real (sem cache)
4. **Encoding:** Todas as strings utilizam UTF-8
5. **Timestamps:** Não há campos de data/hora nos dados atuais

## 🧪 Exemplos Práticos de Uso

### 🚀 Testando com cURL

#### **1. Verificar Status da API**
```bash
curl -X GET "http://localhost:8000/api/v1/status" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

---

#### **2. Health Check Completo**
```bash
curl -X GET "http://localhost:8000/api/v1/health" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "status": "healthy",
  "database_connected": true,
  "total_books": 1000
}
```

---

#### **3. Listar Primeiros 5 Livros**
```bash
curl -X GET "http://localhost:8000/api/v1/books?skip=0&limit=5" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": "Three",
    "availability": "In stock",
    "category": "Poetry",
    "image_url": "http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
    "link": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
  },
  {
    "id": 2,
    "title": "Tipping the Velvet",
    "price": 53.74,
    "rating": "One",
    "availability": "In stock",
    "category": "Historical Fiction",
    "image_url": "http://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg",
    "link": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
  }
]
```

---

#### **4. Buscar Livro por ID**
```bash
curl -X GET "http://localhost:8000/api/v1/books/1" \
  -H "accept: application/json"
```

**Response:**
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

---

#### **5. Buscar Livros por Título**
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=light&limit=3" \
  -H "accept: application/json"
```

**Response:**
```json
[
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
]
```

---

#### **6. Buscar Livros por Categoria**
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?category=Poetry&limit=2" \
  -H "accept: application/json"
```

**Response:**
```json
[
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
]
```

---

#### **7. Listar Todas as Categorias**
```bash
curl -X GET "http://localhost:8000/api/v1/categories" \
  -H "accept: application/json"
```

**Response:**
```json
[
  "Travel",
  "Mystery",
  "Historical Fiction",
  "Sequential Art",
  "Classics",
  "Philosophy",
  "Romance",
  "Women's Fiction",
  "Fiction",
  "Poetry"
]
```

---

#### **8. Filtrar por Faixa de Preço**
```bash
curl -X GET "http://localhost:8000/api/v1/books/price-range?min_price=50&max_price=55&limit=3" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": "Three",
    "availability": "In stock",
    "category": "Poetry",
    "image_url": "http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
    "link": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
  },
  {
    "id": 2,
    "title": "Tipping the Velvet",
    "price": 53.74,
    "rating": "One",
    "availability": "In stock",
    "category": "Historical Fiction",
    "image_url": "http://books.toscrape.com/media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg",
    "link": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
  }
]
```

---

#### **9. Top Livros Mais Bem Avaliados**
```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated?limit=3" \
  -H "accept: application/json"
```

**Response:**
```json
[
  {
    "id": 5,
    "title": "The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull",
    "price": 17.93,
    "rating": "Five",
    "availability": "In stock",
    "category": "Default",
    "image_url": "http://books.toscrape.com/media/cache/3d/54/3d54940e57e662c4dd1f3ff00c78cc64.jpg",
    "link": "http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html"
  }
]
```

---

#### **10. Estatísticas Gerais**
```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "total_books": 1000,
  "average_price": 35.67,
  "rating_distribution": {
    "Five": 213,
    "Four": 213,
    "Three": 200,
    "Two": 190,
    "One": 184
  },
  "categories_count": 50
}
```

---

#### **11. Estatísticas por Categoria**
```bash
curl -X GET "http://localhost:8000/api/v1/stats/categories" \
  -H "accept: application/json" | head -20
```

**Response (primeiras categorias):**
```json
[
  {
    "category": "Travel",
    "book_count": 11,
    "average_price": 32.15,
    "min_price": 10.99,
    "max_price": 56.50
  },
  {
    "category": "Mystery",
    "book_count": 32,
    "average_price": 28.45,
    "min_price": 12.25,
    "max_price": 58.99
  },
  {
    "category": "Poetry",
    "book_count": 19,
    "average_price": 42.35,
    "min_price": 13.99,
    "max_price": 57.25
  }
]
```

### 🐍 Testando com Python

#### **Exemplo com requests:**
```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# 1. Health Check
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# 2. Buscar livros
response = requests.get(f"{BASE_URL}/books", params={"limit": 5})
books = response.json()
print(f"Total livros: {len(books)}")

# 3. Buscar por categoria
response = requests.get(f"{BASE_URL}/books/search", 
                       params={"category": "Poetry", "limit": 3})
poetry_books = response.json()
for book in poetry_books:
    print(f"- {book['title']} (${book['price']})")

# 4. Estatísticas
response = requests.get(f"{BASE_URL}/stats/overview")
stats = response.json()
print(f"Total de livros: {stats['total_books']}")
print(f"Preço médio: ${stats['average_price']:.2f}")
```

### 🧪 Script de Testes Automatizados

Execute o script de testes para verificar todos os endpoints:

```bash
python test_api.py
```

**Saída esperada:**
```
🧪 Testing Book Recommender API
===============================
✅ API Status: OK
✅ Health Check: healthy
✅ Books listing: 100 books found
✅ Book by ID: Found book with ID 1
✅ Search by title: Found books matching 'light'
✅ Search by category: Found books in 'Poetry'
✅ Categories: 50 categories found
✅ Price range: Found books between $20-$30
✅ Top rated: Found top 10 rated books
✅ Stats overview: Retrieved general statistics
✅ Category stats: Retrieved stats for all categories
===============================
✅ All tests passed!
```

## 📊 Estrutura dos Dados

### 🏗️ Modelo de Dados (Book)

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| **id** | Integer | Identificador único (chave primária) | `1` |
| **title** | String | Nome completo do livro | `"A Light in the Attic"` |
| **price** | Float | Preço em libras esterlinas | `51.77` |
| **rating** | String | Avaliação textual (One a Five) | `"Three"` |
| **availability** | String | Status de disponibilidade | `"In stock"` |
| **category** | String | Categoria/gênero do livro | `"Poetry"` |
| **image_url** | Text | URL da capa do livro | `"http://books.toscrape.com/media/..."` |
| **link** | Text | URL da página do livro | `"http://books.toscrape.com/catalogue/..."` |

### 💾 Estrutura do Banco de Dados

O projeto utiliza **SQLite** como banco local com índices otimizados:

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    price FLOAT,
    rating VARCHAR,
    availability VARCHAR,
    category VARCHAR,
    image_url TEXT,
    link TEXT
);

-- Índices para performance
CREATE INDEX idx_books_price ON books(price);
CREATE INDEX idx_books_rating ON books(rating);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_books_title ON books(title);
```

### 📈 Pipeline de Dados ETL

```mermaid
graph LR
    A[Books to Scrape] --> B[Web Scraper]
    B --> C[Raw HTML]
    C --> D[BeautifulSoup Parser]
    D --> E[Data Cleaning]
    E --> F[CSV Export]
    F --> G[SQLite Database]
    G --> H[FastAPI]
    H --> I[JSON Response]
```

**Etapas detalhadas:**

1. **🕷️ Extração (scrape_books.py)**
   - Navegação automatizada por todas as páginas
   - Parsing HTML com BeautifulSoup4
   - Extração de metadados estruturados

2. **🔄 Transformação**
   - Limpeza de caracteres especiais
   - Conversão de preços (string → float)
   - Normalização de categorias
   - Validação de URLs

3. **💾 Carregamento (csv_to_db.py)**
   - Criação automática de tabelas
   - Inserção em lote para performance
   - Criação de índices otimizados
   - Validação de integridade

4. **🚀 Disponibilização (FastAPI)**
   - Endpoints RESTful
   - Validação com Pydantic
   - Documentação automática
   - Tratamento de erros

## 🎯 Casos de Uso e Aplicações

### 🤖 Machine Learning
- **Sistema de Recomendação:** Features categóricas e numéricas prontas
- **Análise de Sentimento:** Dados textuais dos títulos
- **Clustering:** Agrupamento por preço/categoria/rating
- **Previsão de Preços:** Regressão baseada em features

### 📊 Analytics e BI
- **Dashboards:** Distribuição de preços e ratings
- **Relatórios:** Performance por categoria
- **Análise de Mercado:** Tendências de preços
- **KPIs:** Métricas de catálogo

### 🛒 E-commerce
- **Catálogo de Produtos:** Base para loja virtual
- **Sistema de Busca:** Filtros avançados
- **Recomendações:** "Livros similares"
- **Gestão de Inventário:** Status de disponibilidade

## 🛠️ Stack Tecnológico

### **Backend Core**
```yaml
Linguagem: Python 3.8+
Framework: FastAPI 0.116.0
Servidor: Uvicorn (ASGI)
ORM: SQLAlchemy 2.0.36
Banco: SQLite (local/desenvolvimento)
```

### **Data Pipeline**
```yaml
Web Scraping: BeautifulSoup4 + Requests
Processamento: Pandas 2.2.2
Validação: Pydantic (schemas)
Serialização: JSON nativo
```

### **Infraestrutura**
```yaml
Containerização: Docker + Docker Compose
Servidor Produção: Gunicorn + Uvicorn Workers
Monitoramento: Health checks nativos
Logs: Python logging + Uvicorn logs
```

### **Dependências Principais**
```python
# requirements.txt detalhado
requests==2.32.3        # HTTP client para scraping
beautifulsoup4==4.12.3  # HTML parsing
pandas==2.2.2           # Data manipulation
fastapi==0.116.0        # Web framework moderno
uvicorn[standard]==0.35.0  # ASGI server
python-dotenv==1.1.1    # Environment variables
sqlalchemy==2.0.36      # SQL toolkit e ORM
gunicorn==21.2.0        # WSGI server para produção
psutil==5.9.8           # System monitoring
```

## 🚀 Roadmap de Desenvolvimento

### **Fase 1: Base (Concluída) ✅**
- [x] Web scraping automatizado
- [x] Pipeline ETL completo
- [x] API RESTful funcional
- [x] Documentação interativa
- [x] Containerização Docker

### **Fase 2: Produção (Em Planejamento) 📋**
- [ ] Deploy em cloud (Render/Railway)
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Logging estruturado
- [ ] Monitoramento de performance

### **Fase 3: ML Ready (Futuro) 🔮**
- [ ] Endpoints específicos para ML
- [ ] Feature store
- [ ] Pipeline de treinamento
- [ ] Modelo de recomendação
- [ ] A/B testing framework

### **Fase 4: Escala (Visão) 🎯**
- [ ] Cache distribuído (Redis)
- [ ] Banco de produção (PostgreSQL)
- [ ] Microserviços
- [ ] Analytics em tempo real
- [ ] Dashboard de métricas

## 🔧 Troubleshooting

### **Problemas Comuns e Soluções**

#### **❌ Erro: "Module not found"**
```bash
# Solução: Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

#### **❌ Erro: "Database not found"**
```bash
# Solução: Recriar base de dados
mkdir -p data
python scripts/csv_to_db.py
```

#### **❌ Erro: "Port already in use"**
```bash
# Solução: Usar porta diferente
python main.py --port 8001

# Ou matar processo que usa a porta
lsof -ti:8000 | xargs kill -9
```

#### **❌ Erro: "No data scraped"**
```bash
# Solução: Verificar conectividade e re-executar
curl -I https://books.toscrape.com/
python scripts/scrape_books.py
```

### **🔍 Logs e Debug**
```bash
# Logs detalhados
uvicorn main:app --log-level debug

# Verificar status dos dados
curl http://localhost:8000/api/v1/data-status

# Teste rápido de conectividade
python -c "import requests; print(requests.get('http://localhost:8000/api/v1/status').json())"
```

## 🤝 Contribuição

### **Como Contribuir**
1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### **Reportar Bugs**
- Use as [GitHub Issues](https://github.com/seu-usuario/book-recommender-api-pipeline/issues)
- Inclua logs relevantes
- Descreva passos para reproduzir o problema

## 📝 Licença

Este projeto foi desenvolvido para fins **educacionais** como parte do **Tech Challenge da Pós-Tech**.

### **Uso Educacional**
- ✅ Estudo pessoal
- ✅ Referência para projetos acadêmicos
- ✅ Base para expansão e melhorias
- ✅ Portfolio profissional

### **Limitações**
- ⚠️ Não usar para fins comerciais sem autorização
- ⚠️ Dados do Books to Scrape sujeitos aos termos do site
- ⚠️ API destinada a demonstração e aprendizado

---

## 👨‍💻 Sobre o Projeto

**Desenvolvido por:** Equipe Tech Challenge  
**Curso:** Pós-Tech | Machine Learning Engineering - Fase 1  
**Instituição:** [Sua Instituição]  
**Data:** 2024  

### **Objetivos Acadêmicos Atingidos:**
- [x] Pipeline ETL completo
- [x] API RESTful robusta
- [x] Documentação profissional
- [x] Containerização
- [x] Práticas de desenvolvimento

### **Tecnologias Demonstradas:**
- [x] Python avançado
- [x] FastAPI moderno
- [x] Web scraping ético
- [x] Banco de dados relacional
- [x] Docker e containerização

---

## 📚 Documentação Completa

| Documento | Descrição | Conteúdo |
|-----------|-----------|----------|
| **[README.md](./README.md)** | Documentação principal | Instalação, configuração, API, exemplos |
| **[PIPELINE.md](./PIPELINE.md)** | Pipeline de dados detalhado | Arquitetura, diagramas, métricas, fluxos |
| **[DEPLOY.md](./DEPLOY.md)** | Instruções de deploy | Produção, cloud, configurações |
| **[DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)** | Deploy com containers | Docker, Kubernetes, orquestração |

### 🔗 Links Rápidos
- 🚀 [Início Rápido](#-setup-automático-recomendado)
- 🏗️ [Arquitetura](./PIPELINE.md#-arquitetura-geral-do-sistema)
- 📚 [Documentação da API](#-documentação-completa-da-api)
- 🧪 [Exemplos de Uso](#-exemplos-práticos-de-uso)
- 🐳 [Deploy Docker](./DOCKER_DEPLOY.md)
- 🔧 [Troubleshooting](#-troubleshooting)