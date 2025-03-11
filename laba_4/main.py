from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from config import MODELS, TG_TOKEN
from keyboards import get_model_keyboard, remove_keyboard
from models import generate_response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Выберите модель для диалога:",
        reply_markup=get_model_keyboard()
    )

async def handle_model_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    model_name = update.message.text
    if model_name not in MODELS:
        await update.message.reply_text("Пожалуйста, выберите модель из предложенных вариантов")
        return
    
    # Сохраняем конфигурацию модели
    context.user_data["model_config"] = MODELS[model_name]
    await update.message.reply_text(
        f"✅ Модель {model_name} выбрана!\n"
        f"Параметры генерации:\n"
        f"• Температура: {context.user_data['model_config']['parameters']['temperature']}\n"
        f"• Top-K: {context.user_data['model_config']['parameters']['top_k']}\n"
        f"• Штраф повторов: {context.user_data['model_config']['parameters']['repetition_penalty']}\n\n"
        "Отправьте мне слово для генерации рифм!",
        reply_markup=remove_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "model_config" not in context.user_data:
        await update.message.reply_text("❌ Сначала выберите модель через /start")
        return
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action="typing"
    )
    
    try:
        print(context.user_data["model_config"])
        response = await generate_response(
            model=context.user_data["model_config"],
            message=update.message.text
        )
        await update.message.reply_text(f"🎯 Рифмы для слова '{update.message.text}':\n\n{response}")
        
        await update.message.reply_text(
            "Выберите модель для нового запроса:",
            reply_markup=get_model_keyboard()
        )
        context.user_data.pop("model_config", None)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

def main():
    # Создаем приложение бота
    application = ApplicationBuilder()\
        .token(TG_TOKEN)\
        .concurrent_updates(True)\
        .build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.Regex(f"^({'|'.join(MODELS.keys())})$"), handle_model_selection)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
