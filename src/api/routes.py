from datetime import datetime

from fastapi import APIRouter

from src.core.config import settings
from src.core.models import StatusResponse

router = APIRouter()


@router.get("/")
async def read_root():
    """Endpoint de boas-vindas da API"""
    return {
        "message": f"Bem-vindo ao {settings.app_name}",
        "version": settings.version,
        "docs": "/docs",
    }


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Verifica se a API está funcionando"""
    return StatusResponse(
        status="API funcionando",
        timestamp=datetime.utcnow(),
        version=settings.version,
    )


@router.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da aplicação"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "api": "running",
            "azure_vault": (
                "configured" if settings.AzureKeyVault__Dns else "not_configured"
            ),
        },
    }
