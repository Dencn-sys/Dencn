from web3 import Web3
from typing import Dict, Any, List
import json
import logging
from fastapi import HTTPException
from app.models.schemas import ModerationResult


class BlockchainManager:
    def __init__(
        self, provider_url: str, contract_address: str, contract_abi_path: str
    ):
        try:
            self.web3 = Web3(Web3.HTTPProvider(provider_url))

            with open(contract_abi_path, "r") as f:
                contract_abi = json.load(f)

            self.contract = self.web3.eth.contract(
                address=self.web3.to_checksum_address(contract_address),
                abi=contract_abi,
            )
        except Exception as e:
            logging.error(f"Error initializing blockchain manager: {str(e)}")
            raise HTTPException(status_code=500, detail="Blockchain connection failed")

    def store_moderation_result(
        self,
        content_hash: str,
        moderation_result: ModerationResult,
        moderator_address: str,
    ) -> str:
        try:
            tx = self.contract.functions.storeModeration(
                content_hash,
                moderation_result.category,
                moderation_result.confidence,
                moderation_result.is_flagged,
            ).build_transaction(
                {
                    "from": moderator_address,
                    "nonce": self.web3.eth.get_transaction_count(moderator_address),
                    "gas": 2000000,
                    "gasPrice": self.web3.eth.gas_price,
                }
            )

            return tx["hash"].hex()
        except Exception as e:
            logging.error(f"Error storing moderation result on blockchain: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Failed to store result on blockchain"
            )

    def get_moderation_history(self, content_hash: str) -> List[ModerationResult]:
        try:
            raw_history = self.contract.functions.getModerationHistory(
                content_hash
            ).call()
            return [ModerationResult(**item) for item in raw_history]
        except Exception as e:
            logging.error(f"Error retrieving moderation history: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Failed to retrieve moderation history"
            )

    def verify_moderation(self, content_hash: str, transaction_hash: str) -> bool:
        try:
            tx_receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
            return tx_receipt is not None and tx_receipt["status"] == 1
        except Exception as e:
            logging.error(f"Error verifying moderation: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to verify moderation")
