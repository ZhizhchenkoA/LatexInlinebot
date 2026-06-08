import asyncio


asyncio.set_event_loop(asyncio.new_event_loop())

import logging
from pyrogram import Client, filters
import config
from handlers.inline import process_inline_query

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class LatexInlineBot(Client):
    def __init__(self):
        client_kwargs = {
            "name": "latex_inline_bot",
            "api_id": config.config.API_ID,
            "api_hash": config.config.API_HASH,
            "bot_token": config.config.BOT_TOKEN
        }

        if config.config.PROXY:
            client_kwargs["proxy"] = config.config.PROXY
            print(f"🌐 Использование прокси: {config.config.PROXY['scheme']}://{config.config.PROXY['hostname']}:{config.config.PROXY['port']}")
        
        super().__init__(**client_kwargs)

if __name__ == "__main__":
    app = LatexInlineBot()
    
    # Регистрируем обработчик БЕЗ кастомного фильтра
    @app.on_inline_query()
    async def inline_handler(client, query):
        await process_inline_query(client, query)
    
    # Команда /start
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client, message):
        bot_info = await client.get_me()
        bot_username = bot_info.username
        
        await message.reply_text(
            f"🧮 **Привет! Я LaTeX-to-Unicode бот.**\n\n"
            f"Чтобы использовать меня, начни сообщение в любом чате с `@{bot_username}`, например:\n"
            f"`@{bot_username} \\alpha^2 + \\mathbb{{R}}`\n\n"
            f"Я покажу красивый результат, и ты сможешь отправить его в чат одним нажатием!"
        )

    print("🚀 Запуск Inline LaTeX Bot'а...")
    app.run()