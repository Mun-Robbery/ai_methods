import asyncio
import logging
from typing import Dict, Optional

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import load_config
from models import ModelManager
from keyboards import get_model_selection_keyboard, get_after_response_keyboard
# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global state storage
user_states: Dict[int, Dict[str, str]] = {}

class TelegramBot:
    """Main bot class handling all Telegram interactions."""
    
    def __init__(self):
        """Initialize bot with configuration and model manager."""
        self.config = load_config()
        self.model_manager = ModelManager(self.config)

    async def start_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /start command.
        
        Args:
            update: Incoming update
            context: Callback context
        """
        await update.message.reply_text(
            "Welcome! Please select a model to use:",
            reply_markup=get_model_selection_keyboard()
        )

    async def handle_model_selection(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle model selection callback.
        
        Args:
            update: Incoming update
            context: Callback context
        """
        query = update.callback_query
        await query.answer()
        
        model_name = query.data.replace("model_", "")
        user_states[query.from_user.id] = {"model": model_name}
        
        await query.edit_message_text(
            f"Selected model: {model_name}\nPlease enter your prompt:"
        )

    async def handle_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle user messages and generate responses.
        
        Args:
            update: Incoming update
            context: Callback context
        """
        user_id = update.message.from_user.id
        if user_id not in user_states:
            await update.message.reply_text(
                "Please select a model first:",
                reply_markup=get_model_selection_keyboard()
            )
            return

        #prompt = f'Find rhymes for the following word or phrase: {update.message.text}. Rhymes:'
        prompt = f'The five words that rhyme with the word {update.message.text} are:'

        model = user_states[user_id]["model"]
        
        response = await self.model_manager.generate_response(model, prompt)
        if response:
            await update.message.reply_text(
                f"Response:\n{response}",
                reply_markup=get_after_response_keyboard()
            )
        else:
            await update.message.reply_text(
                "Error generating response. Please try again.",
                reply_markup=get_model_selection_keyboard()
            )

    async def handle_after_response(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle actions after response generation.
        
        Args:
            update: Incoming update
            context: Callback context
        """
        query = update.callback_query
        await query.answer()
        
        if query.data == "new_request":
            await query.edit_message_text(
                "Please enter your new prompt:"
            )
        else:  # change_model
            await query.edit_message_text(
                "Please select a new model:",
                reply_markup=get_model_selection_keyboard()
            )

    def run(self) -> None:
        """Start the bot."""
        application = Application.builder().token(self.config.tg_token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CallbackQueryHandler(
            self.handle_model_selection,
            pattern="^model_"
        ))
        application.add_handler(CallbackQueryHandler(
            self.handle_after_response,
            pattern="^(new_request|change_model)$"
        ))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))

        # Start the bot
        application.run_polling()

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()