from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.security import verify_token
from app.services.ai_moderation.moderator import ContentModerator
from app.services.blockchain.manager import BlockchainManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    return username


def get_moderator() -> ContentModerator:
    return ContentModerator(settings.MODEL_PATH, settings.CONFIDENCE_THRESHOLD)


def get_blockchain_manager() -> BlockchainManager:
    return BlockchainManager(
        settings.BLOCKCHAIN_PROVIDER_URL,
        settings.SMART_CONTRACT_ADDRESS,
        "contract_abi.json",
    )
