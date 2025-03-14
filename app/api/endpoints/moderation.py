from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
import hashlib
import tempfile
import os
from typing import List

from app.models.schemas import (
    ModerationRequest,
    ModerationResponse,
    ModerationHistory,
    ModerationResult,
)
from app.api.deps import get_current_user, get_moderator, get_blockchain_manager
from app.services.ai_moderation.moderator import ContentModerator
from app.services.blockchain.manager import BlockchainManager

router = APIRouter()


@router.post("/text", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest,
    current_user: str = Depends(get_current_user),
    moderator: ContentModerator = Depends(get_moderator),
    blockchain: BlockchainManager = Depends(get_blockchain_manager),
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


@router.post("/image", response_model=ModerationResponse)
async def moderate_image(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    moderator: ContentModerator = Depends(get_moderator),
    blockchain: BlockchainManager = Depends(get_blockchain_manager),
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


@router.get("/history/{content_hash}", response_model=ModerationHistory)
async def get_moderation_history(
    content_hash: str,
    current_user: str = Depends(get_current_user),
    blockchain: BlockchainManager = Depends(get_blockchain_manager),
):
    try:
        history = blockchain.get_moderation_history(content_hash)
        return ModerationHistory(content_hash=content_hash, history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=List[ModerationResponse])
async def batch_moderate(
    requests: List[ModerationRequest],
    current_user: str = Depends(get_current_user),
    moderator: ContentModerator = Depends(get_moderator),
    blockchain: BlockchainManager = Depends(get_blockchain_manager),
):
    responses = []
    for request in requests:
        try:
            content_hash = hashlib.sha256(request.content.encode()).hexdigest()

            if request.content_type == "text":
                moderation_result = moderator.moderate_text(request.content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported content type in batch processing",
                )

            tx_hash = blockchain.store_moderation_result(
                content_hash,
                moderation_result,
                "0x0",  # Replace with actual moderator address
            )

            responses.append(
                ModerationResponse(
                    content_hash=content_hash,
                    moderation_result=moderation_result,
                    blockchain_transaction=tx_hash,
                )
            )
        except Exception as e:
            responses.append({"error": str(e)})

    return responses
