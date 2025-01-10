from typing import Dict, Optional
import aiohttp
from config import BotConfig

class ModelManager:
    """Manager class for handling interactions with language models."""
    
    def __init__(self, config: BotConfig):
        """
        Initialize ModelManager with configuration.
        
        Args:
            config: Bot configuration containing tokens and URLs
        """
        self.config = config
        self.headers = {"Authorization": f"Bearer {config.hf_token}"}

    async def generate_response(self, model_name: str, prompt: str) -> Optional[str]:
        """
        Generate response from specified model.
        
        Args:
            model_name: Name of the model to use
            prompt: Input prompt for the model
            
        Returns:
            Generated text or None if request failed
        """
        if model_name not in self.config.model_urls:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.config.model_urls[model_name],
                headers=self.headers,
                json={"inputs": prompt}
            ) as response:
                if response.status != 200:
                    return None
                result = await response.json()
                return result[0].get("generated_text", "Error generating response")