from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import hashlib
import tempfile
import os

from config import settings
from ai_moderator import ContentModerator
from blockchain_manager import BlockchainManager

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Initialize components
moderator = ContentModerator(settings.MODEL_PATH, settings.CONFIDENCE_THRESHOLD)
blockchain = BlockchainManager(
    settings.BLOCKCHAIN_PROVIDER_URL,
    settings.SMART_CONTRACT_ADDRESS,
    "contract_abi.json",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ModerationRequest(BaseModel):
    content: str
    content_type: str
    metadata: Optional[Dict[str, Any]] = None


class ModerationResponse(BaseModel):
    content_hash: str
    moderation_result: Dict[str, Any]
    blockchain_transaction: str


@app.post("/api/v1/moderate/text", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest, token: str = Depends(oauth2_scheme)
):
    try:
        # Generate content hash
        content_hash = hashlib.sha256(request.content.encode()).hexdigest()

        # Perform AI moderation
        moderation_result = moderator.moderate_text(request.content)

        # Store result on blockchain
        tx_hash = blockchain.store_moderation_result(
            content_hash,
            moderation_result,
            "0x0",  # Replace with actual moderator address
        )

        return ModerationResponse(
            content_hash=content_hash,
            moderation_result=moderation_result,
            blockchain_transaction=tx_hash,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/moderate/image", response_model=ModerationResponse)
async def moderate_image(
    file: UploadFile = File(...), token: str = Depends(oauth2_scheme)
):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Generate content hash
        content_hash = hashlib.sha256(content).hexdigest()

        # Perform AI moderation
        moderation_result = moderator.moderate_image(temp_file_path)

        # Clean up temporary file
        os.unlink(temp_file_path)

        # Store result on blockchain
        tx_hash = blockchain.store_moderation_result(
            content_hash,
            moderation_result,
            "0x0",  # Replace with actual moderator address
        )

        return ModerationResponse(
            content_hash=content_hash,
            moderation_result=moderation_result,
            blockchain_transaction=tx_hash,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/moderation/{content_hash}")
async def get_moderation_history(
    content_hash: str, token: str = Depends(oauth2_scheme)
):
    try:
        history = blockchain.get_moderation_history(content_hash)
        return {"content_hash": content_hash, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
