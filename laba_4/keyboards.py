from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

def get_model_selection_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for model selection."""
    keyboard = [
        [
            InlineKeyboardButton("Llama 3.2", callback_data="model_llama"),
            InlineKeyboardButton("GPT-Neo", callback_data="model_gpt-neo")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_after_response_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for actions after response."""
    keyboard = [
        [
            InlineKeyboardButton("New Request", callback_data="new_request"),
            InlineKeyboardButton("Change Model", callback_data="change_model")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)