# src/alpha_mini_pkg/utils/helpers.py

import asyncio
import logging

# Отримуємо логер для цього модуля
logger = logging.getLogger(__name__)

async def safe_delay(seconds: float, reason: str = ""):
    """
    Виконує асинхронну паузу, логуючи причину.

    :param seconds: Час очікування в секундах.
    :param reason: Причина очікування (для логування).
    """
    if reason:
        logger.debug(f"⏳ Пауза на {seconds:.2f} с. Причина: {reason}")
    else:
        logger.debug(f"⏳ Пауза на {seconds:.2f} с.")
        
    await asyncio.sleep(seconds)

def estimate_tts_duration(text: str, chars_per_second: float = 6.67, base_time: float = 2.0) -> float:
    """
    Оцінює тривалість TTS на основі довжини тексту.
    
    Це кращий підхід, ніж жорстко закодований таймаут.
    (6.67 - приблизно 400 символів на хвилину, типова швидкість мови)

    :param text: Текст, який буде озвучено.
    :param chars_per_second: Приблизна швидкість мови в символах/с.
    :param base_time: Базовий час для початку/кінця TTS.
    :return: Оцінена тривалість у секундах.
    """
    text_length = len(text)
    # Захист від ділення на нуль, хоча швидкість має бути > 0
    if chars_per_second <= 0:
        return base_time
    
    estimated_time = (text_length / chars_per_second) + base_time
    return estimated_time