# 🐳 Deploy com Docker - Book Recommender API

**Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering**

Este guia mostra como usar Docker para deployar a Book Recommender API, tanto localmente quanto em plataformas de nuvem como Render, Railway, Fly.io e outras.

## 📋 Índice

1. [Vantagens do Docker](#vantagens-do-docker)
2. [Arquivos Docker Criados](#arquivos-docker-criados)
3. [Deploy Local com Docker](#deploy-local-com-docker)
4. [Deploy no Render com Docker](#deploy-no-render-com-docker)
5. [Deploy em Outras Plataformas](#deploy-em-outras-plataformas)
6. [Otimizações e Best Practices](#otimizações-e-best-practices)

---

## 🎯 Vantagens do Docker

### ✅ **Por que usar Docker em vez de render.yaml?**

| Aspecto | Docker | render.yaml |
|---------|--------|-------------|
| **Portabilidade** | ✅ Funciona em qualquer lugar | ❌ Específico do Render |
| **Reprodutibilidade** | ✅ Ambiente idêntico sempre | ⚠️ Depende da plataforma |
| **Flexibilidade** | ✅ Controle total do ambiente | ❌ Limitado às opções do Render |
| **Debug** | ✅ Execução local idêntica | ❌ Diferenças entre local/prod |
| **Multi-cloud** | ✅ Deploy em qualquer nuvem | ❌ Só funciona no Render |
| **Dependências** | ✅ Isolamento completo | ⚠️ Conflitos possíveis |

---

## 📦 Arquivos Docker Criados

### 🐳 **`Dockerfile`** (Versão Simples)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python setup_production.py
EXPOSE 8000
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]
```

### 🚀 **`Dockerfile.multi-stage`** (Versão Otimizada)
- Build em múltiplas etapas
- Imagem final menor
- Melhor segurança com usuário não-root
- Cache otimizado

### 🔧 **`docker-compose.yml`**
- Orquestração completa
- Volumes para persistência
- Health checks
- Configuração de rede

### 🚫 **`.dockerignore`**
- Exclui arquivos desnecessários
- Reduz tamanho da imagem
- Melhora performance do build

---

## 🏠 Deploy Local com Docker

### **Método 1: Docker simples**

```bash
# 1. Build da imagem
docker build -t book-recommender-api .

# 2. Executar container
docker run -p 8000:8000 book-recommender-api

# 3. Testar
curl http://localhost:8000/api/v1/health
```

### **Método 2: Docker Compose** (Recomendado)

```bash
# 1. Executar com docker-compose
docker-compose up --build

# 2. Executar em background
docker-compose up -d

# 3. Ver logs
docker-compose logs -f

# 4. Parar
docker-compose down
```

### **Verificações**

```bash
# Status dos containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f book-recommender-api

# Entrar no container para debug
docker-compose exec book-recommender-api bash

# Testar endpoints
curl http://localhost:8000/docs
```

---

## ☁️ Deploy no Render com Docker

### **Configuração no Render**

1. **Acesse** [render.com](https://render.com)
2. **New → Web Service**
3. **Connect Repository**
4. **Configurações**:

```yaml
Name: book-recommender-api
Environment: Docker
Dockerfile Path: ./Dockerfile
Build Command: (deixar vazio)
Start Command: (deixar vazio)
```

5. **Environment Variables**:
```
PORT=8000
DATABASE_URL=sqlite:///./data/books.db
ENVIRONMENT=production
```

### **Vantagens no Render com Docker**

- ✅ Build mais rápido
- ✅ Mesmo ambiente local/produção
- ✅ Menos configuração manual
- ✅ Health checks automáticos
- ✅ Rollbacks mais fáceis

---

## 🌐 Deploy em Outras Plataformas

### **🚂 Railway**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
railway deploy
```

Configuração Railway:
```
Type: Docker
Dockerfile: ./Dockerfile
Port: 8000
```

### **🪰 Fly.io**

```bash
# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Launch app
fly launch --dockerfile Dockerfile

# 4. Deploy
fly deploy
```

### **☁️ Google Cloud Run**

```bash
# 1. Build e push para GCR
docker build -t gcr.io/PROJECT_ID/book-recommender-api .
docker push gcr.io/PROJECT_ID/book-recommender-api

# 2. Deploy
gcloud run deploy book-recommender-api \
  --image gcr.io/PROJECT_ID/book-recommender-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### **🔷 Azure Container Instances**

```bash
# 1. Create resource group
az group create --name book-recommender --location eastus

# 2. Deploy container
az container create \
  --resource-group book-recommender \
  --name book-recommender-api \
  --image book-recommender-api \
  --ports 8000 \
  --environment-variables PORT=8000
```

---

## ⚡ Otimizações e Best Practices

### **🔧 Dockerfile Otimizado**

```dockerfile
# Use multi-stage build
FROM python:3.11-slim as builder
# ... build stage

FROM python:3.11-slim
# ... runtime stage
```

### **📦 Redução do Tamanho da Imagem**

```bash
# Ver tamanho das imagens
docker images book-recommender-api

# Análise detalhada
docker run --rm -it wagoodman/dive book-recommender-api
```

**Técnicas de otimização**:
- ✅ Multi-stage builds
- ✅ Alpine Linux (imagem menor)
- ✅ .dockerignore bem configurado
- ✅ Combinar comandos RUN
- ✅ Remover cache de pacotes

### **🚀 Performance**

```dockerfile
# Cache de layers
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # Isso só executa se código mudar

# Health checks
HEALTHCHECK --interval=30s --timeout=30s \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1
```

### **🔒 Segurança**

```dockerfile
# Usuário não-root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Variáveis de ambiente seguras
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

---

## 🐛 Troubleshooting Docker

### **Problemas Comuns**

#### 1. **Build lento**
```bash
# Usar cache
docker build --cache-from book-recommender-api .

# Build paralelo
docker build --parallel .
```

#### 2. **Container não inicia**
```bash
# Ver logs
docker logs container_name

# Debug interativo
docker run -it book-recommender-api bash
```

#### 3. **Problemas de permissão**
```bash
# Verificar usuário
docker run book-recommender-api whoami

# Ajustar permissões
USER 1000:1000
```

#### 4. **Health check falha**
```bash
# Testar health check manualmente
docker exec container_name curl http://localhost:8000/api/v1/health
```

### **Debug Commands**

```bash
# Entrar no container em execução
docker exec -it container_name bash

# Ver processos
docker exec container_name ps aux

# Ver espaço em disco
docker exec container_name df -h

# Ver logs específicos
docker logs --tail 100 container_name
```

---

## 📊 Comparação: Docker vs render.yaml

| Critério | Docker | render.yaml |
|----------|--------|-------------|
| **Setup inicial** | ⚠️ Mais complexo | ✅ Mais simples |
| **Portabilidade** | ✅ Total | ❌ Limitada |
| **Performance** | ✅ Otimizada | ⚠️ Dependente |
| **Debug** | ✅ Fácil local | ❌ Só em produção |
| **Flexibilidade** | ✅ Total controle | ❌ Limitada |
| **Manutenção** | ⚠️ Mais trabalho | ✅ Automática |
| **Custo** | ✅ Mesma | ✅ Mesma |

---

## 🎯 Recomendação

### **Use Docker quando:**
- ✅ Quer portabilidade entre clouds
- ✅ Precisa de ambiente idêntico local/prod
- ✅ Tem dependências complexas
- ✅ Quer controle total do ambiente
- ✅ Planeja crescer para microserviços

### **Use render.yaml quando:**
- ✅ Quer simplicidade máxima
- ✅ Está começando no Render
- ✅ Não precisa de portabilidade
- ✅ Quer menos configuração

---

## 🚀 Quick Start com Docker

```bash
# 1. Clone o repositório
git clone your-repo
cd book-recommender-api-pipeline

# 2. Build e execute
docker-compose up --build

# 3. Teste
curl http://localhost:8000/docs

# 4. Deploy no Render
# Conecte repositório e selecione "Docker" como ambiente
```

---

**🐳 Docker está pronto para uso!**

Agora você pode deployar sua API em qualquer plataforma que suporte Docker, mantendo total controle sobre o ambiente e garantindo reprodutibilidade perfeita entre desenvolvimento e produção.