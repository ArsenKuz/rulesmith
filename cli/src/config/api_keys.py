"""API key configuration management for LLM providers."""

import os
from pathlib import Path
from typing import Optional, Dict
import json
from dataclasses import dataclass, asdict


@dataclass
class APIKeyConfig:
    """Configuration for API keys."""

    # LLM Providers
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None

    # AI Tools (that might need API keys)
    cursor_api_key: Optional[str] = None
    github_token: Optional[str] = None  # For Copilot
    roo_api_key: Optional[str] = None

    # Custom/Local
    ollama_base_url: Optional[str] = "http://localhost:11434"
    localai_base_url: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary (for serialization)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "APIKeyConfig":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class APIKeyManager:
    """Manages API key configuration."""

    def __init__(self):
        self.config_dir = Path.home() / ".rulesmith"
        self.config_file = self.config_dir / "api-keys.json"
        self._config: Optional[APIKeyConfig] = None

    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(exist_ok=True)

    def load(self) -> APIKeyConfig:
        """Load API key configuration."""
        if self._config is not None:
            return self._config

        if not self.config_file.exists():
            self._config = APIKeyConfig()
            return self._config

        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
            self._config = APIKeyConfig.from_dict(data)
        except (json.JSONDecodeError, IOError):
            self._config = APIKeyConfig()

        # Override with environment variables if present
        self._load_from_env()

        return self._config

    def save(self, config: APIKeyConfig) -> None:
        """Save API key configuration."""
        self._ensure_config_dir()
        self._config = config

        with open(self.config_file, "w") as f:
            json.dump(config.to_dict(), f, indent=2)

    def _load_from_env(self) -> None:
        """Override config with environment variables."""
        if self._config is None:
            return

        env_mappings = {
            "openai_api_key": ["OPENAI_API_KEY", "OPENAI_KEY"],
            "anthropic_api_key": [
                "ANTHROPIC_API_KEY",
                "ANTHROPIC_KEY",
                "CLAUDE_API_KEY",
            ],
            "cohere_api_key": ["COHERE_API_KEY", "COHERE_KEY"],
            "openrouter_api_key": ["OPENROUTER_API_KEY", "OPENROUTER_KEY"],
            "github_token": ["GITHUB_TOKEN", "GITHUB_API_TOKEN", "GH_TOKEN"],
            "ollama_base_url": ["OLLAMA_BASE_URL", "OLLAMA_URL"],
            "localai_base_url": ["LOCALAI_BASE_URL", "LOCALAI_URL"],
        }

        for attr, env_vars in env_mappings.items():
            for env_var in env_vars:
                value = os.getenv(env_var)
                if value:
                    setattr(self._config, attr, value)
                    break

    def get_key(self, provider: str) -> Optional[str]:
        """Get API key for a specific provider."""
        config = self.load()
        return getattr(config, f"{provider.lower()}_api_key", None)

    def set_key(self, provider: str, key: str) -> None:
        """Set API key for a specific provider."""
        config = self.load()
        attr_name = f"{provider.lower()}_api_key"
        if hasattr(config, attr_name):
            setattr(config, attr_name, key)
            self.save(config)

    def has_key(self, provider: str) -> bool:
        """Check if API key is configured for a provider."""
        key = self.get_key(provider)
        return key is not None and key.strip() != ""

    def list_configured(self) -> Dict[str, bool]:
        """List all providers and whether they have keys configured."""
        config = self.load()
        providers = [
            "openai",
            "anthropic",
            "cohere",
            "openrouter",
            "cursor",
            "github",
            "roo",
        ]
        return {p: self.has_key(p) for p in providers}

    def remove_key(self, provider: str) -> None:
        """Remove API key for a provider."""
        config = self.load()
        attr_name = f"{provider.lower()}_api_key"
        if hasattr(config, attr_name):
            setattr(config, attr_name, None)
            self.save(config)
