# Instalação e Configuração

Este guia consolida todas as instruções de instalação, setup e configuração do projeto.

## Pré-requisitos

- Python 3.8+ (recomendado: 3.9 ou superior)
- pip (gerenciador de pacotes Python)
- Git (para clonagem do repositório)
- 4GB RAM mínimo para processamento dos dados
- Conexão com internet para web scraping inicial

## Setup Automático (Recomendado)

O projeto inclui um script de setup totalmente automatizado que:
- Cria ambiente virtual Python
- Instala todas as dependências
- Executa web scraping (se necessário)
- Configura o banco de dados SQLite
- Valida a instalação

```bash
# Clone o repositório
git clone <repository-url>
cd book-recommender-api-pipeline

# Execute o setup automático
python setup.py
```

Saída esperada:
```
 Setting up Book Recommender API...
 ==================================================
  Creating Python virtual environment...
  Virtual environment created successfully!
  Installing required dependencies...
  Dependencies installed successfully!
  No existing data found, running scraper...
   Running web scraper...
  Scraping completed!
   Setting up database...
  Database setup completed!
 ==================================================
  Setup completed successfully!
```

## Setup Manual (Avançado)

Para maior controle do processo de instalação:

### 1. Preparação do Ambiente

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

### 2. Extração de Dados (Web Scraping)

```bash
# Execute o scraper para obter dados atualizados
python scripts/scrape_books.py

# Verificar dados extraídos
ls -la data/books.csv
```

### 3. Configuração do Banco de Dados

```bash
# Carregue dados CSV para SQLite
python scripts/csv_to_db.py

# Verificar banco criado
ls -la data/books.db
```

### 4. Validação da Instalação

```bash
# Teste rápido da API
python -c "
from api.database import get_db, Book
from sqlalchemy.orm import Session
next(get_db()).query(Book).count()
print(' Database OK!')
"
```

## Instalação com Docker (Opcional)

Para ambiente completamente isolado:

```bash
# Build da imagem
docker build -t book-recommender-api .

# Execução do container
docker run -p 8000:8000 book-recommender-api

# Ou usando docker-compose
docker-compose up --build
```

## Dependências do Projeto

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

## Configuração de Ambiente

### Variáveis de Ambiente Suportadas

```bash
# Porta da aplicação (padrão: 8000)
export PORT=8000

# URL do banco de dados (padrão: sqlite:///./data/books.db)
export DATABASE_URL="sqlite:///./data/books.db"

# Ambiente de execução
export ENVIRONMENT="development"  # ou "production"
```

### Arquivo .env (Opcional)

```bash
# Crie um arquivo .env na raiz do projeto
PORT=8000
DATABASE_URL=sqlite:///./data/books.db
ENVIRONMENT=development
```

## Verificação de Problemas Comuns

### Erro de permissão no Python

```bash
# Use o flag --user se não tiver privilégios admin
pip install --user -r requirements.txt
```

### Erro no web scraping

```bash
# Verifique conectividade
curl -I https://books.toscrape.com/
# Se OK, execute novamente o scraper
python scripts/scrape_books.py
```

### Banco de dados não criado

```bash
# Verifique se o diretório data/ existe
mkdir -p data
# Execute novamente o carregamento
python scripts/csv_to_db.py
```

