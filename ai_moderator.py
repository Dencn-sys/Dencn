from transformers import pipeline
from PIL import Image
import pytesseract
import cv2
import numpy as np
from typing import Dict, Union, List
import logging


class ContentModerator:
    def __init__(self, model_path: str, confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold
        self.text_classifier = pipeline("text-classification", model=model_path)
        self.image_classifier = pipeline("image-classification", model=model_path)
        self.categories = ["safe", "hate_speech", "violence", "adult", "harassment"]

    def moderate_text(self, text: str) -> Dict[str, Union[str, float]]:
        try:
            result = self.text_classifier(text)
            prediction = {
                "content_type": "text",
                "category": result[0]["label"],
                "confidence": result[0]["score"],
                "is_flagged": result[0]["score"] > self.confidence_threshold,
            }
            return prediction
        except Exception as e:
            logging.error(f"Error in text moderation: {str(e)}")
            return {"error": str(e)}

    def moderate_image(self, image_path: str) -> Dict[str, Union[str, float]]:
        try:
            image = Image.open(image_path)
            result = self.image_classifier(image)

            # Extract text from image for additional analysis
            img_array = cv2.imread(image_path)
            extracted_text = pytesseract.image_to_string(img_array)

            text_results = (
                self.moderate_text(extracted_text) if extracted_text.strip() else None
            )

            prediction = {
                "content_type": "image",
                "category": result[0]["label"],
                "confidence": result[0]["score"],
                "is_flagged": result[0]["score"] > self.confidence_threshold,
                "text_analysis": text_results,
            }
            return prediction
        except Exception as e:
            logging.error(f"Error in image moderation: {str(e)}")
            return {"error": str(e)}

    def batch_moderate(
        self, contents: List[Dict[str, str]]
    ) -> List[Dict[str, Union[str, float]]]:
        results = []
        for content in contents:
            if content["type"] == "text":
                result = self.moderate_text(content["content"])
            elif content["type"] == "image":
                result = self.moderate_image(content["content"])
            else:
                result = {"error": "Unsupported content type"}
            results.append(result)
        return results
