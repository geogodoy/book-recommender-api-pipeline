# Book Recommender API Pipeline

Este repositório contém o projeto desenvolvido para o Tech Challenge da Fase 1 da Pós-Tech em Machine Learning Engineering. O objetivo foi construir uma infraestrutura de coleta, processamento e disponibilização de dados sobre livros através de uma API pública e escalável.

---

## Visão Geral do Projeto

O sistema é composto por:
- Web Scraper automatizado para coletar dados do site [Books to Scrape](https://books.toscrape.com/)
- Armazenamento estruturado em CSV
- API RESTful para servir os dados extraídos
- Deploy da API em ambiente público
- Plano arquitetural pensado para expansão futura com modelos de Machine Learning

---

## Arquitetura

```plaintext
           +-------------+        +----------------+        +----------------+
           | Web Scraper | -----> | Base de Dados  | -----> |     API REST   |
           +-------------+        +----------------+        +----------------+
                                           |
                                           v
                                Acesso via endpoints públicos
