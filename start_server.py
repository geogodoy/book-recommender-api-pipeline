"""
Script simplificado para iniciar o servidor em produção
Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering
"""

import uvicorn
import os

if __name__ == "__main__":
    # Configuração para produção
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print("🚀 Starting Book Recommender API...")
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/api/v1/health")
    
    # Executar com configurações otimizadas
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Desabilitar reload em produção
        access_log=True,
        log_level="info"
    )