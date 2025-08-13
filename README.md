# Book Recommender API Pipeline

**Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering**

**Desenvolvido por:** Cleiton Cardodo, Geovana Godoy Viana
**Instituição:** Fiap  
**Data:** agosto/2025


Uma API RESTful completa para consulta de livros com pipeline de dados automatizado, desenvolvida como parte do Tech Challenge da primeira fase do curso de Machine Learning Engineering.

##  Descrição do Projeto

Este projeto implementa um **pipeline completo de dados** e uma **API RESTful robusta** para servir informações de livros extraídas via web scraping do site [Books to Scrape](https://books.toscrape.com/). 

###  Objetivos
- **Extração automatizada** de dados de livros via web scraping
- **API RESTful** performática com documentação interativa
- **Pipeline ETL** completo (Extração → Transformação → Carregamento)
- **Arquitetura escalável** para integração futura com modelos de ML
- **Containerização** com Docker para deploy simplificado

###  Características Técnicas
- **Framework:** FastAPI com documentação automática (Swagger/ReDoc)
- **Banco de Dados:** SQLite com SQLAlchemy ORM
- **Validação:** Pydantic para schemas de request/response
- **Performance:** Endpoints otimizados com indexação de banco
- **Observabilidade:** Health checks e endpoints de status

##  Arquitetura do Sistema

```
book-recommender-api-pipeline/
  data/                    # Camada de Dados
    books.csv              # Dados extraídos (formato raw)
    books.db               # Base de dados SQLite (formato estruturado)
  scripts/                 # Pipeline ETL
    scrape_books.py        # Extrator: Web scraping automatizado
    csv_to_db.py           # Carregador: CSV → Database
  api/                     # Camada de Aplicação
    database.py            # Configuração do ORM e modelos
    schemas.py             # Schemas de validação (Pydantic)
    crud.py                # Operações de banco (CRUD)
  main.py                  # Aplicação FastAPI principal
  setup.py                 # Automação de setup inicial
  requirements.txt         # Dependências do projeto
  Dockerfile              # Containerização
  docker-compose.yml      # Orquestração de containers
```

###  Fluxo de Dados
```
[Books to Scrape] → [Web Scraper] → [CSV] → [ETL Pipeline] → [SQLite] → [FastAPI] → [Cliente]
```

>  **Documentação Detalhada:** Para uma análise completa do pipeline com diagramas interativos, métricas de performance e arquitetura detalhada, consulte [PIPELINE.md](./PIPELINE.md)

##  Instalação e Configuração

As instruções completas de instalação, setup, configuração de ambiente e solução de problemas podem ser encontradas no guia dedicado a seguir:

- Consulte `INSTALLATION.md` para detalhes: [Instalação e Configuração](./INSTALLATION.md)

##  Executando a API

As instruções completas de execução, URLs de acesso, monitoramento, performance e como parar a API foram movidas para um guia dedicado:

- Consulte `USAGE.md`: [Execução da API (Runbook)](./USAGE.md)

###  Configuração de Ambiente

As variáveis de ambiente e o uso de arquivo `.env` estão documentados em [Instalação e Configuração](./INSTALLATION.md)

###  Monitoramento da Execução

Para exemplos práticos de chamadas (cURL e Python) com respostas, consulte:

- [Exemplos de Chamadas](./API_EXAMPLES.md)

#### **Logs da Aplicação**
```bash
# Para ver logs detalhados durante execução
python main.py --log-level debug

# Ou usando uvicorn
uvicorn main:app --log-level debug
```

###  Performance e Otimização

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

##  Documentação da API

As rotas, schemas, exemplos e códigos de erro foram movidos para um guia dedicado:

- Consulte `API_REFERENCE.md` para detalhes: [Referência da API](./API_REFERENCE.md)


##  Casos de Uso e Aplicações

###  Machine Learning
- **Sistema de Recomendação:** Features categóricas e numéricas prontas
- **Análise de Sentimento:** Dados textuais dos títulos
- **Clustering:** Agrupamento por preço/categoria/rating
- **Previsão de Preços:** Regressão baseada em features

###  Analytics e BI
- **Dashboards:** Distribuição de preços e ratings
- **Relatórios:** Performance por categoria
- **Análise de Mercado:** Tendências de preços
- **KPIs:** Métricas de catálogo

###  E-commerce
- **Catálogo de Produtos:** Base para loja virtual
- **Sistema de Busca:** Filtros avançados
- **Recomendações:** "Livros similares"
- **Gestão de Inventário:** Status de disponibilidade

##  Stack Tecnológico

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

### **Objetivos Acadêmicos Atingidos:**
- [x] Pipeline ETL completo
- [x] API RESTful robusta
- [x] Documentação profissional
- [x] Containerização
- [x] Práticas de desenvolvimento
- [x] Deploy em cloud - Render
- [x] Autenticação JWT

### **Tecnologias Demonstradas:**
- [x] Python avançado
- [x] FastAPI moderno
- [x] Web scraping ético
- [x] Banco de dados relacional
- [x] Docker e containerização

---

###  Links Rápidos
-  [Instalação & Configuração](./INSTALLATION.md)
-  [Execução da API](./USAGE.md)
-  [Referência da API](./API_REFERENCE.md)
-  [Exemplos de Chamadas](./API_EXAMPLES.md)
-  [Arquitetura](./PIPELINE.md#-arquitetura-geral-do-sistema)