# models.py
from huggingface_hub import InferenceClient
import asyncio
from config import HF_API_KEY, DEFAULT_PARAMS

client = InferenceClient(token=HF_API_KEY)

SYSTEM_PROMPT = """Ты профессиональный поэт-рифмоплёт. Сгенерируй 3 креативные рифмы для слова, которое предоставит пользователь. 
Рифмы должны быть творческими и использовать различные стили. Формат ответа:
1. [Рифма 1] - [краткое объяснение]
2. [Рифма 2] - [пояснение]
3. [Рифма 3] - [пояснение]

Слово для рифмовки: """

async def generate_response(model: dict, message: str) -> str:
    """Генерация рифм через Hugging Face API"""
    try:
        full_prompt = SYSTEM_PROMPT + message.strip()
        params = {**DEFAULT_PARAMS, **model.get("parameters", {})}
        
        response = await asyncio.to_thread(
            client.text_generation,
            prompt=full_prompt,
            model=model["model_name"],
            max_new_tokens=params["max_new_tokens"],
            temperature=params["temperature"],
            top_k=params["top_k"],
            repetition_penalty=params["repetition_penalty"],
            do_sample=True
        )
        return response
    except Exception as e:
        raise Exception(f"Ошибка генерации: {str(e)}")
