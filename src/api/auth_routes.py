from fastapi import APIRouter, HTTPException

from src.core.models import ApiResponse, Token, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Realiza autenticação do usuário"""
    # TODO: Implementar autenticação real
    if credentials.username == "admin" and credentials.password == "admin":
        return Token(access_token="fake-token")
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")


@router.get("/status")
async def get_auth_status():
    """Verifica o status da autenticação"""
    return ApiResponse(
        message="Sistema de autenticação ativo", data={"status": "active"}
    )
