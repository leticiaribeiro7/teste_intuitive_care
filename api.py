from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List
import os

from models import DespesaAgregada, Operadora, DespesaConsolidada
from db.db_setup import engine

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi.middleware.cors import CORSMiddleware


# Configuração do ciclo de vida do App
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Inicializa o cache em memória ao ligar o servidor
    FastAPICache.init(InMemoryBackend())
    yield

app = FastAPI(title="ANS Data API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependência para abrir/fechar a sessão do banco em cada requisição
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# --- ROTAS ---

@app.get("/api/operadoras")
def listar_operadoras(
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    operadoras = db.query(Operadora).offset(offset).limit(limit).all()
    return {
        "data": operadoras, "total": db.query(Operadora).count(), "page": page, "limit": limit
    }

@app.get("/api/operadoras/{cnpj}")
def detalhes_operadora(cnpj: str, db: Session = Depends(get_db)):
    operadora = db.query(Operadora).filter(Operadora.cnpj == cnpj).first()
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return operadora

@app.get("/api/operadoras/{cnpj}/despesas")
def historico_despesas(cnpj: str, db: Session = Depends(get_db)):
    despesas = db.query(DespesaConsolidada).filter(DespesaConsolidada.cnpj == cnpj).all()
    if not despesas:
        raise HTTPException(status_code=404, detail="Nenhuma despesa encontrada para este CNPJ")
    return despesas

@app.get("/api/estatisticas")
@cache(expire=3600)
def obter_estatisticas(db: Session = Depends(get_db)):
    stats_geral = db.query(
        func.sum(DespesaAgregada.total_despesas).label("total"),
        func.avg(DespesaAgregada.total_despesas).label("media")
    ).first()

    # 2. Top 5 Operadoras 
    query_top5 = text("""
        SELECT o.razao_social, SUM(d.total_despesas) as total
        FROM despesas_agregadas d
        JOIN operadoras o ON d.registro_ans = o.registro_ans
        GROUP BY o.razao_social
        ORDER BY total DESC
        LIMIT 5
    """)
    
    top5 = db.execute(query_top5).mappings().all()

    return {
        "total_geral": float(stats_geral.total or 0),
        "media_geral": float(stats_geral.media or 0),
        "top_5_operadoras": top5
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)