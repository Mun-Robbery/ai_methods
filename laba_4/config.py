# config.py
from environs import Env

env = Env()
env.read_env()

HF_API_KEY = env.str("HUGGINGFACE_TOKEN")
TG_TOKEN = env.str("TELEGRAM_TOKEN")

MODELS = {
    "Llama 2": {
        "model_name": "meta-llama/Llama-3.2-1B",
        "parameters": {
            "temperature": 0.7,
            "top_k": 50,
            "repetition_penalty": 1.8
        }
    },
    "Rugpt3": {
        "model_name": "ai-forever/rugpt3medium_based_on_gpt2",
        "parameters": {
            "temperature": 0.5,
            "top_k": 30,
            "repetition_penalty": 1.9
        }
    }
}

DEFAULT_PARAMS = {
    "temperature": 0.7,
    "top_k": 50,
    "repetition_penalty": 1.1,
    "max_new_tokens": 500
}
