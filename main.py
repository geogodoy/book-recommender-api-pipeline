"""
FastAPI application for Book Recommender API
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from api import crud, schemas
from api.auth import create_access_token, create_refresh_token, get_current_admin_user, perform_refresh_token
from api.users import authenticate_user
from api.database import Book
from api.database import get_db, create_tables

# Create tables
create_tables()

# Initialize FastAPI app
app = FastAPI(
    title="Book Recommender API",
    description="API para consulta de livros - Tech Challenge Fase 1",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Book Recommender API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Core Endpoints
@app.get("/api/v1/books", response_model=List[schemas.Book])
def get_books(
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of books to return"),
    db: Session = Depends(get_db)
):
    """Lista todos os livros disponíveis na base de dados"""
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/api/v1/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes completos de um livro específico pelo ID"""
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/api/v1/books/search", response_model=List[schemas.Book])
def search_books(
    title: Optional[str] = Query(None, description="Search by title"),
    category: Optional[str] = Query(None, description="Search by category"),
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of books to return"),
    db: Session = Depends(get_db)
):
    """Busca livros por título e/ou categoria"""
    if not title and not category:
        raise HTTPException(status_code=400, detail="At least one search parameter (title or category) is required")
    
    books = crud.search_books(db, title=title, category=category, skip=skip, limit=limit)
    return books


@app.get("/api/v1/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    """Lista todas as categorias de livros disponíveis"""
    categories = crud.get_categories(db)
    return categories


@app.get("/api/v1/health", response_model=schemas.HealthCheck)
def health_check(db: Session = Depends(get_db)):
    """Verifica status da API e conectividade com os dados - Optimized"""
    try:
        # Use a faster query: just check if any book exists instead of counting all
        has_books = db.query(Book).first() is not None
        
        # Only count if specifically needed - for now just check existence
        total_books = 1 if has_books else 0  # Simplified: 1 means "has data", 0 means "no data"
        
        return schemas.HealthCheck(
            status="healthy",
            database_connected=True,
            total_books=total_books
        )
    except Exception as e:
        return schemas.HealthCheck(
            status="unhealthy",
            database_connected=False,
            total_books=0
        )


@app.get("/api/v1/status")
def quick_status():
    """Endpoint super rápido para verificar se a API está funcionando"""
    return {"status": "ok", "message": "API is running"}


@app.get("/api/v1/data-status")
def data_status(db: Session = Depends(get_db)):
    """Verificação ultra-rápida se há dados no banco"""
    try:
        # Usa LIMIT 1 para ser o mais rápido possível
        has_data = db.query(Book).limit(1).first() is not None
        return {
            "has_data": has_data,
            "status": "data_loaded" if has_data else "no_data"
        }
    except Exception as e:
        return {
            "has_data": False,
            "status": "database_error",
            "error": str(e)
        }


# Optional Insights Endpoints
@app.get("/api/v1/stats/overview", response_model=schemas.StatsOverview)
def get_stats_overview(db: Session = Depends(get_db)):
    """Estatísticas gerais da coleção"""
    stats = crud.get_stats_overview(db)
    return schemas.StatsOverview(**stats)


@app.get("/api/v1/stats/categories", response_model=List[schemas.CategoryStats])
def get_category_stats(db: Session = Depends(get_db)):
    """Estatísticas detalhadas por categoria"""
    stats = crud.get_category_stats(db)
    return [schemas.CategoryStats(**stat) for stat in stats]


@app.get("/api/v1/books/top-rated", response_model=List[schemas.Book])
def get_top_rated_books(
    limit: int = Query(20, ge=1, le=100, description="Number of top books to return"),
    db: Session = Depends(get_db)
):
    """Lista os livros com melhor avaliação"""
    books = crud.get_top_rated_books(db, limit=limit)
    return books


@app.get("/api/v1/books/price-range", response_model=List[schemas.Book])
def get_books_by_price_range(
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of books to return"),
    db: Session = Depends(get_db)
):
    """Filtra livros dentro de uma faixa de preço específica"""
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")
    
    books = crud.get_books_by_price_range(db, min_price=min_price, max_price=max_price, skip=skip, limit=limit)
    return books


@app.post("/api/v1/auth/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60)
    refresh_token_expires = timedelta(days=7)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user["username"]}, expires_delta=refresh_token_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/api/v1/auth/refresh", response_model=schemas.Token)
def refresh_access_token(refresh_token: str = Body(..., embed=True)):
    return perform_refresh_token(refresh_token)


@app.post("/api/v1/scraping/trigger")
def trigger_scraping(current_user: dict = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    # Lógica de scraping aqui
    return {"message": "Scraping triggered successfully"}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)