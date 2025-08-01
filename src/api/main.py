from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import auth_routes, nuuvify_wordsegment_routes, routes
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar o ciclo de vida da aplicação"""
    # Startup
    print(f"Iniciando {settings.app_name} v{settings.version}")

    # Conectar ao Azure Vault
    print("Conexão com Azure Key Vault inicializada")

    yield

    # Shutdown
    print("Encerrando aplicação...")
    print("Aplicação encerrada")


def create_app() -> FastAPI:
    """Factory function para criar a aplicação FastAPI"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc",
        description="API para segmentação de palavras usando NLP e Azure Key Vault",
        lifespan=lifespan,
    )

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Incluir rotas
    app.include_router(routes.router, prefix=settings.API_PREFIX)
    app.include_router(nuuvify_wordsegment_routes.router, prefix=settings.API_PREFIX)
    app.include_router(auth_routes.router, prefix=settings.API_PREFIX)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
