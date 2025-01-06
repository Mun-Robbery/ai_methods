import numpy as np
import torch

np.random.seed(42)
torch.manual_seed(42)

from transformers import GPT2LMHeadModel, GPT2Tokenizer

class GptApi:
  '''
  Класс для работы с GPT-3 API.
  '''
  def __init__(self, model_name: str = "sberbank-ai/rugpt3small_based_on_gpt2", query: str = None) -> None:
    '''
    Инициализация класса.
    
    :param model_name: Название модели GPT-3 (по умолчанию "sberbank-ai/rugpt3small_based_on_gpt2")
    :param query: Входной запрос (по умолчанию None)
    '''
    self.mode_name = model_name
    self.query = query

  def load_tokenizer_and_model(self):
    '''
    Загрузка токенизатора и модели GPT-3.
    
    :return: Токенизатор и модель GPT-3
    '''
    return GPT2Tokenizer.from_pretrained(self.mode_name), GPT2LMHeadModel.from_pretrained(self.mode_name).cuda()
  
  def generate(self,
    model, tok, text,
    do_sample=True, 
    max_length=50, 
    repetition_penalty=5.0,
    top_k=5, 
    top_p=0.95, 
    temperature=1,
    num_beams=10,
    no_repeat_ngram_size=3
    ) -> list:
    '''
    Генерация текста с помощью модели GPT-3.
    
    :param model: Модель GPT-3
    :param tok: Токенизатор
    :param text: Входной текст
    :param do_sample: Флаг для использования сэмплинга (по умолчанию True)
    :param max_length: Максимальная длина генерируемого текста (по умолчанию 50)
    :param repetition_penalty: Штраф за повторение (по умолчанию 5.0)
    :param top_k: Количество лучших вариантов для сэмплинга (по умолчанию 5)
    :param top_p: Вероятность для сэмплинга (по умолчанию 0.95)
    :param temperature: Температура для сэмплинга (по умолчанию 1)
    :param num_beams: Количество лучших вариантов для бим-сэмплинга (по умолчанию 10)
    :param no_repeat_ngram_size: Размер n-граммы для повторения (по умолчанию 3)
    :return: Список генерируемых текстов
    '''
    input_ids = tok.encode(text, return_tensors="pt").cuda()
    out = model.generate(
      input_ids.cuda(),
      max_length=max_length,
      repetition_penalty=repetition_penalty,
      do_sample=do_sample,
      top_k=top_k, 
      top_p=top_p, 
      temperature=temperature,
      num_beams=num_beams, 
      no_repeat_ngram_size=no_repeat_ngram_size
      )
    return list(map(tok.decode, out))
  
  def get_answer(self, params: dict) -> str:
    '''
    Получение ответа на входной запрос.
    
    :param params: Словарь параметров для генерации текста
    :return: Генерируемый текст
    '''
    kwargs = {}
    for k, v in params.items():
      if v != '':
        if k in ['top_p', 'temperature', 'repetition_penalty']:
          kwargs[k] = float(v)
        elif k == 'do_sample':
          kwargs[k] = bool(v)
        else:
          kwargs[k] = int(v)
    tok, model = self.load_tokenizer_and_model()
    generated = self.generate(model, tok, self.query, **kwargs)

    return generated[0]


