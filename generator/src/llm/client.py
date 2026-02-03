"""LLM client for PRD generation."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class LLMResponse:
    """Response from LLM."""

    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> LLMResponse:
        """Generate content from LLM."""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API client."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> LLMResponse:
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=kwargs.get("max_tokens", 4000),
                temperature=kwargs.get("temperature", 0.7),
            )

            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                finish_reason=response.choices[0].finish_reason,
            )
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude API client."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> LLMResponse:
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 4000),
                temperature=kwargs.get("temperature", 0.7),
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            return LLMResponse(
                content=response.content[0].text,
                model=response.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
                finish_reason=response.stop_reason,
            )
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {e}")


class OllamaClient(BaseLLMClient):
    """Ollama local model client."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> LLMResponse:
        import requests

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7),
                    },
                },
                timeout=300,
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data.get("response", ""),
                model=self.model,
                usage={},  # Ollama doesn't provide token counts
                finish_reason="stop",
            )
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {e}")


def create_llm_client(
    provider: str = "openai", api_key: Optional[str] = None, model: Optional[str] = None
) -> BaseLLMClient:
    """Factory function to create LLM client."""
    if provider == "openai":
        return OpenAIClient(api_key=api_key, model=model or "gpt-4")
    elif provider == "anthropic":
        return AnthropicClient(
            api_key=api_key, model=model or "claude-3-sonnet-20240229"
        )
    elif provider == "ollama":
        return OllamaClient(
            base_url=api_key or "http://localhost:11434", model=model or "llama2"
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
