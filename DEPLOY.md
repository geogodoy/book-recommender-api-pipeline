# 🚀 Guia de Deploy - Book Recommender API

**Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering**

Este guia fornece instruções completas para fazer deploy da Book Recommender API no Render, incluindo configuração, deploy e testes em produção.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Preparação do Código](#preparação-do-código)
3. [Deploy no Render](#deploy-no-render)
4. [Configuração Pós-Deploy](#configuração-pós-deploy)
5. [Testes em Produção](#testes-em-produção)
6. [Monitoramento](#monitoramento)
7. [Troubleshooting](#troubleshooting)

---

## 📚 Pré-requisitos

### Contas e Ferramentas
- ✅ Conta no [Render](https://render.com) (gratuita)
- ✅ Conta no [GitHub](https://github.com) 
- ✅ Git instalado localmente
- ✅ Python 3.8+ instalado

### Repositório
- ✅ Código versionado no GitHub
- ✅ Arquivos de configuração criados (já incluídos neste projeto)

---

## 🔧 Preparação do Código

### 1. Arquivos de Configuração Criados

Os seguintes arquivos já foram criados para o deploy:

#### 📄 `render.yaml`
```yaml
services:
  - type: web
    name: book-recommender-api
    env: python
    plan: free
    buildCommand: python setup_production.py
    startCommand: gunicorn main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker --workers 1 --timeout 120
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        value: sqlite:///./data/books.db
      - key: ENVIRONMENT
        value: production
    healthCheckPath: /api/v1/health
```

#### 📄 `setup_production.py`
Script automatizado que:
- Instala dependências
- Executa web scraping
- Configura banco de dados
- Prepara ambiente de produção

#### 📄 `gunicorn.conf.py`
Configuração otimizada do Gunicorn para produção

#### 📄 `requirements.txt` (atualizado)
```
requests==2.32.3
beautifulsoup4==4.12.3
pandas==2.2.2
fastapi==0.116.0
uvicorn[standard]==0.35.0
python-dotenv==1.1.1
sqlalchemy==2.0.36
gunicorn==21.2.0
psutil==5.9.8
```

### 2. Verificar Alterações

```bash
# Verificar se main.py foi atualizado para usar PORT do ambiente
grep "PORT" main.py

# Verificar requirements.txt
cat requirements.txt
```

---

## 🚀 Deploy no Render

### Método 1: Deploy via GitHub (Recomendado)

#### 1. **Preparar Repositório**
```bash
# Adicionar arquivos ao Git
git add .
git commit -m "feat: add Render deployment configuration"
git push origin main
```

#### 2. **Configurar no Render**

1. **Acesse**: [render.com](https://render.com)
2. **Login** com sua conta GitHub
3. **New → Web Service**
4. **Connect Repository**: Selecione seu repositório
5. **Configurações**:
   - **Name**: `book-recommender-api`
   - **Environment**: `Python`
   - **Build Command**: `python setup_production.py`
   - **Start Command**: `gunicorn main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker --workers 1 --timeout 120`

#### 3. **Variáveis de Ambiente**
Adicione as seguintes variáveis:
```
PYTHON_VERSION=3.11.0
DATABASE_URL=sqlite:///./data/books.db
ENVIRONMENT=production
```

#### 4. **Deploy**
- Clique em **"Create Web Service"**
- Aguarde o build (5-10 minutos)

### Método 2: Deploy via render.yaml

Se você tem o arquivo `render.yaml` configurado:

1. **Fork/Clone** o repositório
2. **Connect** no Render
3. Render detectará automaticamente o `render.yaml`
4. **Deploy** será iniciado automaticamente

---

## ⚙️ Configuração Pós-Deploy

### 1. Verificar Deploy

Após o deploy bem-sucedido:

```bash
# Sua URL será algo como:
https://book-recommender-api-xxxx.onrender.com
```

### 2. Verificar Health Check

```bash
curl https://your-app-url.onrender.com/api/v1/health
```

**Resposta esperada**:
```json
{
  "status": "healthy",
  "database_connected": true,
  "total_books": 1
}
```

### 3. Verificar Documentação

- **Swagger**: `https://your-app-url.onrender.com/docs`
- **ReDoc**: `https://your-app-url.onrender.com/redoc`

---

## 🧪 Testes em Produção

### Script de Testes Automatizado

Execute o script criado para validar todos os endpoints:

```bash
# Local
python test_production.py https://your-app-url.onrender.com

# Ou interativo
python test_production.py
# Digite a URL quando solicitado
```

### Testes Manuais

#### 1. **Endpoints Básicos**
```bash
# Root
curl https://your-app-url.onrender.com/

# Health Check
curl https://your-app-url.onrender.com/api/v1/health

# Status rápido
curl https://your-app-url.onrender.com/api/v1/status
```

#### 2. **Funcionalidades Core**
```bash
# Listar livros
curl "https://your-app-url.onrender.com/api/v1/books?limit=5"

# Buscar livro específico
curl "https://your-app-url.onrender.com/api/v1/books/1"

# Buscar por título
curl "https://your-app-url.onrender.com/api/v1/books/search?title=python"

# Categorias
curl "https://your-app-url.onrender.com/api/v1/categories"
```

#### 3. **Endpoints de Insights**
```bash
# Estatísticas gerais
curl "https://your-app-url.onrender.com/api/v1/stats/overview"

# Top livros
curl "https://your-app-url.onrender.com/api/v1/books/top-rated?limit=5"

# Por faixa de preço
curl "https://your-app-url.onrender.com/api/v1/books/price-range?min_price=10&max_price=30"
```

---

## 📊 Monitoramento

### 1. **Logs do Render**
- Acesse o dashboard do Render
- Clique no seu serviço
- Vá para **"Logs"** para ver logs em tempo real

### 2. **Health Check Automático**
O Render verifica automaticamente `/api/v1/health` a cada 30 segundos

### 3. **Métricas de Performance**
- Monitor de CPU/Memory no dashboard
- Response time dos endpoints
- Uptime tracking

---

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. **Build falha**
```bash
# Verificar logs de build
# Comum: dependências em conflito
pip install -r requirements.txt  # Testar localmente
```

#### 2. **Timeout no Start**
```bash
# Verificar se o scraping está demorando muito
# Ajustar timeout no gunicorn.conf.py
timeout = 180  # Aumentar se necessário
```

#### 3. **Banco de dados vazio**
```bash
# Verificar se setup_production.py executou
# Verificar logs para erros no scraping
```

#### 4. **Performance lenta**
```bash
# Primeira requisição pode ser lenta (cold start)
# Subsequentes devem ser rápidas (<2s)
```

### Debug Commands

```bash
# Testar setup localmente
python setup_production.py

# Testar comando start
gunicorn main:app --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker

# Verificar dados
python -c "from api.database import *; print('OK' if os.path.exists('data/books.db') else 'NO DB')"
```

---

## 📝 URLs Importantes

Após o deploy, você terá acesso a:

| Endpoint | URL | Descrição |
|----------|-----|-----------|
| **Root** | `https://your-app.onrender.com/` | Página inicial |
| **Health** | `https://your-app.onrender.com/api/v1/health` | Status da API |
| **Docs** | `https://your-app.onrender.com/docs` | Documentação Swagger |
| **ReDoc** | `https://your-app.onrender.com/redoc` | Documentação ReDoc |
| **Books** | `https://your-app.onrender.com/api/v1/books` | Lista de livros |
| **Search** | `https://your-app.onrender.com/api/v1/books/search` | Busca de livros |

---

## 🎯 Próximos Passos

Após deploy bem-sucedido:

1. ✅ **Compartilhar URL** com stakeholders
2. ✅ **Documentar endpoints** para equipe
3. ✅ **Configurar monitoramento** (opcional)
4. ✅ **Testar load** da aplicação
5. ✅ **Considerar CDN** para imagens (futuro)

---

## 📞 Suporte

**Problemas durante o deploy?**

1. Verifique os logs no dashboard do Render
2. Teste o setup localmente primeiro
3. Confirme que todos os arquivos estão no repositório
4. Verifique se as variáveis de ambiente estão corretas

---

**Deploy realizado com sucesso!** 🎉

Sua API estará disponível em: `https://your-app-name.onrender.com`