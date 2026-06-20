"""Thin wrapper around Hugging Face InferenceClient."""

import logging
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from app.prompts import build_recommendations_messages, build_summary_messages

load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self) -> None:
        self.token: str | None = os.getenv("HF_TOKEN")
        self.model_id: str = os.getenv(
            "HF_MODEL_ID", "Qwen/Qwen2.5-7B-Instruct"
        )
        self.max_new_tokens: int = int(os.getenv("LLM_MAX_NEW_TOKENS", "512"))
        self.debug: bool = os.getenv("DEBUG_PROMPTS", "false").lower() == "true"

        if not self.token:
            raise ValueError("HF_TOKEN environment variable is not set")

        self._client = InferenceClient(token=self.token)

    def _chat(self, messages: list[dict[str, str]]) -> str:
        if self.debug:
            logger.debug("[DEBUG] Messages:\n%s\n---", messages)
        response = self._client.chat_completion(
            messages=messages,
            model=self.model_id,
            max_tokens=self.max_new_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def generate_summary(
        self, category_breakdown: dict, total_tco2e: float, country: str
    ) -> str:
        messages = build_summary_messages(category_breakdown, total_tco2e, country)
        return self._chat(messages)

    def generate_recommendations(
        self, category_breakdown: dict, total_tco2e: float
    ) -> str:
        messages = build_recommendations_messages(category_breakdown, total_tco2e)
        return self._chat(messages)
