# config.py
from dataclasses import dataclass
from typing import Dict
from environs import Env

@dataclass
class BotConfig:
    """Configuration class for bot tokens and API endpoints."""
    tg_token: str
    hf_token: str
    model_urls: Dict[str, str]

def load_config() -> BotConfig:
    """Load configuration from environment variables."""
    env = Env()
    env.read_env()

    return BotConfig(
        tg_token=env.str("TELEGRAM_TOKEN"),
        hf_token=env.str("HUGGINGFACE_TOKEN"),
        model_urls={
            "llama": "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B",
            "gpt-neo": "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        }
    )