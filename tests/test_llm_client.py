"""Mocked LLM integration tests."""

from unittest.mock import MagicMock, patch

import pytest

from app.llm_client import LLMClient


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "hf_test123")
    monkeypatch.setenv("HF_MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")
    monkeypatch.setenv("LLM_MAX_NEW_TOKENS", "128")


@pytest.fixture
def client(mock_env):
    with patch("app.llm_client.InferenceClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_chat = MagicMock()
        mock_chat.choices = [MagicMock()]
        mock_chat.choices[0].message.content = "Mocked LLM response."
        mock_instance.chat_completion.return_value = mock_chat
        yield LLMClient()


def test_generate_summary(client):
    breakdown = {"Household": 2.5, "Travel": 1.2}
    result = client.generate_summary(breakdown, total_tco2e=3.7, country="GB")
    assert "Mocked LLM response." in result


def test_generate_recommendations(client):
    breakdown = {"Household": 2.5, "Travel": 1.2}
    result = client.generate_recommendations(breakdown, total_tco2e=3.7)
    assert "Mocked LLM response." in result


def test_missing_token(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    with pytest.raises(ValueError, match="HF_TOKEN"):
        with patch("app.llm_client.InferenceClient"):
            LLMClient()
