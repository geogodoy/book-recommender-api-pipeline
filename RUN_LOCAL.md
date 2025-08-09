# 🏃‍♂️ Como Executar Localmente - Book Recommender API

**Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering**

Este guia mostra todas as formas de executar a Book Recommender API localmente para desenvolvimento e testes.

## 📋 Métodos Disponíveis

1. [Setup Automático](#1-setup-automático-recomendado)
2. [Setup Manual](#2-setup-manual)
3. [Docker](#3-docker)
4. [Docker Compose](#4-docker-compose-mais-fácil)

---

## 1. 🚀 Setup Automático (Recomendado)

### **Execução em Uma Linha:**
```bash
python setup.py && python main.py
```

### **Passo a Passo:**
```bash
# 1. Setup completo (ambiente + dados + banco)
python setup.py

# 2. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# 3. Executar API
python main.py
```

### **O que o setup.py faz:**
- ✅ Cria ambiente virtual
- ✅ Instala dependências
- ✅ Executa web scraping
- ✅ Configura banco de dados
- ✅ Valida dados

---

## 2. 🔧 Setup Manual

### **Se preferir controle total:**

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar scraping (se não tiver dados)
python scripts/scrape_books.py

# 5. Configurar banco
python scripts/csv_to_db.py

# 6. Executar API
python main.py
```

---

## 3. 🐳 Docker (Simples)

### **Build e Execute:**
```bash
# 1. Build da imagem
docker build -t book-recommender-api .

# 2. Executar container
docker run -p 8000:8000 book-recommender-api
```

### **Com persistência de dados:**
```bash
# Criar volume para dados
docker run -p 8000:8000 -v $(pwd)/data:/app/data book-recommender-api
```

---

## 4. 🐳 Docker Compose (Mais Fácil)

### **Execução One-Click:**
```bash
# Executar (build automático)
docker-compose up

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

---

## 📊 Verificação da Execução

### **URLs para Testar:**

| Endpoint | URL | Descrição |
|----------|-----|-----------|
| 🏠 **Root** | http://localhost:8000/ | Página inicial |
| ❤️ **Health** | http://localhost:8000/api/v1/health | Status da API |
| 📖 **Docs** | http://localhost:8000/docs | Documentação Swagger |
| 📚 **Books** | http://localhost:8000/api/v1/books?limit=5 | Lista de livros |
| 🔍 **Search** | http://localhost:8000/api/v1/books/search?title=python | Busca |

### **Comandos de Teste:**
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Listar livros
curl "http://localhost:8000/api/v1/books?limit=5"

# Buscar livros
curl "http://localhost:8000/api/v1/books/search?title=the"

# Ver categorias
curl http://localhost:8000/api/v1/categories
```

---

## 🔍 Troubleshooting

### **Problema: Porta 8000 ocupada**
```bash
# Ver quem está usando a porta
lsof -i :8000          # Mac/Linux
netstat -ano | find "8000"  # Windows

# Matar processo
kill -9 PID_NUMBER

# Usar porta diferente
python main.py  # Editar main.py para mudar porta
# OU
PORT=8080 python main.py
```

### **Problema: Dependências não instaladas**
```bash
# Verificar Python
python --version  # Deve ser 3.8+

# Instalar pip
python -m ensurepip --upgrade

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### **Problema: Dados não encontrados**
```bash
# Verificar se CSV existe
ls -la data/books.csv

# Se não existir, executar scraping
python scripts/scrape_books.py

# Verificar banco
ls -la data/books.db

# Se não existir, carregar dados
python scripts/csv_to_db.py
```

### **Problema: Import errors**
```bash
# Verificar PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH

# Ou executar do diretório raiz
cd /path/to/book-recommender-api-pipeline
python main.py
```

---

## ⚡ Execução Rápida para Demo

### **Demo One-Liner:**
```bash
python setup.py && python main.py &
sleep 5 && curl http://localhost:8000/api/v1/health && echo "🎉 API rodando!"
```

### **Demo com Docker:**
```bash
docker-compose up -d && sleep 10 && curl http://localhost:8000/api/v1/health
```

---

## 📝 Scripts Auxiliares

### **Criar script de inicialização rápida:**
```bash
# criar arquivo: start.sh (Linux/Mac)
cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Book Recommender API..."
source venv/bin/activate 2>/dev/null || python setup.py
python main.py
EOF
chmod +x start.sh

# Executar
./start.sh
```

### **Para Windows (start.bat):**
```batch
@echo off
echo 🚀 Starting Book Recommender API...
call venv\Scripts\activate 2>nul || python setup.py
python main.py
pause
```

---

## 🧪 Teste Completo Local

### **Script de teste automático:**
```bash
# Executar testes
python test_production.py http://localhost:8000
```

### **Teste manual passo a passo:**
```bash
# 1. Verificar se API subiu
curl http://localhost:8000/

# 2. Health check
curl http://localhost:8000/api/v1/health

# 3. Contar livros
curl http://localhost:8000/api/v1/books | jq length

# 4. Buscar
curl "http://localhost:8000/api/v1/books/search?title=light" | jq .

# 5. Categorias
curl http://localhost:8000/api/v1/categories | jq .
```

---

## 🎯 Resumo dos Comandos

### **Setup + Execução (Método Recomendado):**
```bash
# Setup completo
python setup.py

# Ativar ambiente
source venv/bin/activate

# Executar API
python main.py

# Testar
curl http://localhost:8000/api/v1/health
```

### **Docker (Alternativa):**
```bash
# Método mais simples
docker-compose up

# Testar
curl http://localhost:8000/api/v1/health
```

---

## 🔧 Configurações Úteis

### **Variáveis de ambiente:**
```bash
# .env local (opcional)
PORT=8000
DATABASE_URL=sqlite:///./data/books.db
ENVIRONMENT=development
```

### **Para desenvolvimento:**
```bash
# Executar com reload automático
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Executar com logs detalhados
python main.py --log-level debug
```

---

**🎉 Pronto! Sua API estará rodando em http://localhost:8000**

Escolha o método que preferir - o setup automático é mais fácil, mas Docker oferece maior consistência!