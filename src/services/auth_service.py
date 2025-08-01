from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings
from src.core.models import Token, UserLogin, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.SECRET_KEY = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.algorithm)
        return encoded_jwt

    def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        # Placeholder - aqui você implementaria a lógica real de autenticação
        # Por exemplo, consultar um banco de dados
        if username == "admin" and password == "admin123":
            return UserResponse(
                username=username, is_active=True, created_at=datetime.utcnow()
            )
        return None

    def login(self, user_credentials: UserLogin) -> Optional[Token]:
        user = self.authenticate_user(
            user_credentials.username, user_credentials.password
        )
        if not user:
            return None

        access_token = self.create_access_token(data={"sub": user.username})
        return Token(access_token=access_token)


auth_service = AuthService()
