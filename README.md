# Book Recommender API Pipeline

**Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering**

Uma API RESTful completa para consulta de livros, desenvolvida como parte do Tech Challenge da primeira fase do curso de Machine Learning Engineering.

## 📋 Descrição do Projeto

Este projeto implementa um pipeline completo de dados e uma API pública para servir informações de livros extraídas via web scraping do site [Books to Scrape](https://books.toscrape.com/). A solução foi projetada pensando em escalabilidade e reusabilidade futura em modelos de machine learning.

## 🏗️ Arquitetura

```
book-recommender-api-pipeline/
├── data/                    # Dados armazenados (CSV e SQLite)
├── scripts/                 # Scripts de scraping e ETL
│   ├── scrape_books.py     # Web scraper principal
│   └── csv_to_db.py        # Pipeline CSV → Database
├── api/                    # Módulos da API
│   ├── database.py         # Configuração do banco de dados
│   ├── models.py           # Modelos SQLAlchemy
│   ├── schemas.py          # Schemas Pydantic
│   └── crud.py             # Operações CRUD
├── main.py                 # Aplicação FastAPI principal
├── setup.py                # Script de configuração inicial
├── run_api.py              # Script para executar a API
├── test_api.py             # Script de testes da API
└── requirements.txt        # Dependências do projeto
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip

### Setup Automático
Execute o script de configuração que irá instalar dependências, fazer scraping e configurar o banco:

```bash
python setup.py
```

### Setup Manual

1. **Clone o repositório e instale dependências:**
```bash
git clone <repository-url>
cd book-recommender-api-pipeline
pip install -r requirements.txt
```

2. **Execute o web scraping:**
```bash
python scripts/scrape_books.py
```

3. **Carregue os dados no banco:**
```bash
python scripts/csv_to_db.py
```

## 🎯 Executando a API

### Método 1: Script de execução
```bash
python run_api.py
```

### Método 2: Comando direto
```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### URLs Importantes
- **Documentação Swagger:** `http://localhost:8000/docs`
- **Documentação ReDoc:** `http://localhost:8000/redoc`
- **Health Check:** `http://localhost:8000/api/v1/health`

### Endpoints Core

#### `GET /api/v1/books`
Lista todos os livros disponíveis na base de dados.

**Parâmetros:**
- `skip` (int): Número de livros a pular (paginação)
- `limit` (int): Número de livros a retornar (máx: 1000)

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/books?limit=5"
```

#### `GET /api/v1/books/{id}`
Retorna detalhes completos de um livro específico pelo ID.

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/books/1"
```

#### `GET /api/v1/books/search`
Busca livros por título e/ou categoria.

**Parâmetros:**
- `title` (str): Busca por título (parcial)
- `category` (str): Busca por categoria

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/books/search?title=python&category=programming"
```

#### `GET /api/v1/categories`
Lista todas as categorias de livros disponíveis.

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/categories"
```

#### `GET /api/v1/health`
Verifica status da API e conectividade com os dados.

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/health"
```

### Endpoints de Insights

#### `GET /api/v1/stats/overview`
Estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings).

#### `GET /api/v1/stats/categories`
Estatísticas detalhadas por categoria (quantidade de livros, preços por categoria).

#### `GET /api/v1/books/top-rated`
Lista os livros com melhor avaliação (rating mais alto).

#### `GET /api/v1/books/price-range`
Filtra livros dentro de uma faixa de preço específica.

**Parâmetros:**
- `min_price` (float): Preço mínimo
- `max_price` (float): Preço máximo

## 🧪 Testando a API

Execute o script de testes para verificar todos os endpoints:

```bash
python test_api.py
```

## 📊 Dados Extraídos

O web scraper coleta os seguintes campos de cada livro:

- **Título:** Nome completo do livro
- **Preço:** Valor em libras (convertido para float)
- **Avaliação:** Rating de 1 a 5 estrelas (One, Two, Three, Four, Five)
- **Disponibilidade:** Status de estoque
- **Categoria:** Gênero/categoria do livro
- **Imagem:** URL da capa do livro
- **Link:** URL da página do livro

## 🔧 Estrutura do Banco de Dados

O projeto utiliza SQLite como banco local com a seguinte estrutura:

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    price FLOAT,
    rating VARCHAR,
    availability VARCHAR,
    category VARCHAR,
    image_url TEXT,
    link TEXT
);
```

## 🚀 Pipeline de Dados

1. **Extração:** Web scraping do site Books to Scrape
2. **Transformação:** Limpeza e normalização dos dados
3. **Armazenamento:** Salvamento em CSV e carregamento no SQLite
4. **Disponibilização:** API RESTful para consulta dos dados

## 🎯 Cenários de Uso para ML

Esta API foi projetada para facilitar o desenvolvimento de sistemas de recomendação:

- **Features Categóricas:** Categoria, rating, disponibilidade
- **Features Numéricas:** Preço, ID
- **Features Textuais:** Título (para NLP)
- **Metadata:** URLs de imagens e links

## 📈 Próximos Passos

- [ ] Implementação de autenticação JWT
- [ ] Endpoints específicos para ML (features, training data)
- [ ] Sistema de monitoramento e analytics
- [ ] Deploy em produção (Heroku/Render)
- [ ] Cache Redis para performance
- [ ] Testes automatizados

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local
- **Pandas** - Manipulação de dados
- **BeautifulSoup4** - Web scraping
- **Requests** - Requisições HTTP
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge da Pós-Tech.

---

**Desenvolvido por:** [Seu Nome]  
**Curso:** Pós-Tech | Machine Learning Engineering - Fase 1  
**Data:** 2024