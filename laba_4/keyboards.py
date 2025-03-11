from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import MODELS

def get_model_keyboard():
    """Создаёт клавиатуру для выбора модели"""
    keyboard = [[model] for model in MODELS.keys()]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

def remove_keyboard():
    """Удаляет клавиатуру"""
    return ReplyKeyboardRemove()
