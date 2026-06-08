import logging
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.enums import ParseMode

from utils.latex_converter import latex_to_unicode

logger = logging.getLogger(__name__)

async def process_inline_query(client, query: InlineQuery):
    """
    Обрабатывает inline-запросы и предлагает конвертированный текст.
    """
    original_text = query.query.strip()
    
    # Если пользователь ничего не ввёл или ввёл только пробелы, просто выходим
    if not original_text:
        return
    
    try:
        # Конвертируем текст
        converted_text = latex_to_unicode(original_text)
        
        # Определяем, изменился ли текст
        is_changed = converted_text != original_text
        
        # Формируем заголовок и описание (лимит Telegram на title = 64 символа)
        title = (converted_text[:60] + "...") if len(converted_text) > 60 else converted_text
        description = f"Оригинал: {original_text}" if is_changed else "Текст без изменений (команды не найдены)"
        
        # Создаём результат для inline-меню
        result = InlineQueryResultArticle(
            title=title,
            description=description,
            input_message_content=InputTextMessageContent(
                message_text=converted_text,
                parse_mode=ParseMode.DISABLED
            ),
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Mathematics-omega.svg/120px-Mathematics-omega.svg.png"
        )
        
        # Отправляем результат пользователю
        await query.answer(
            results=[result],
            cache_time=1
        )
        
    except Exception as e:
        logger.error(f"Ошибка в inline-обработчике: {e}")
        await query.answer(
            results=[],
            switch_pm_text="❌ Ошибка при конвертации",
            switch_pm_parameter="error"
        )