# src/alpha_mini_pkg/core/actions_wrapper.py

import logging
from mini.apis.api_action import MoveRobotDirection 
from alpha_mini_pkg.services import api_client 
from alpha_mini_pkg.utils.helpers import estimate_tts_duration, safe_delay

logger = logging.getLogger(__name__)

# --- Атомарні Універсальні Обгортки (Wrappers) ---

async def action_walk(steps: int, direction: MoveRobotDirection = MoveRobotDirection.FORWARD) -> bool:
    """
    Високорівнева обгортка для руху робота.
    """
    logger.info(f"WRAPPER: Запуск руху: {direction.name}, {steps} кроків.")
    return await api_client.move_robot(steps=steps, direction=direction)


async def action_speak(text: str) -> bool:
    """
    Високорівнева обгортка для TTS (мови).
    Запускає TTS і автоматично очікує завершення.
    """
    logger.info(f'WRAPPER: Запуск мови: "{text[:30]}..."')
    
    success = await api_client.start_tts(text=text)

    if success:
        tts_duration = estimate_tts_duration(text)
        await safe_delay(tts_duration, f"Очікування завершення TTS ({tts_duration:.2f} с.)")
        logger.info("WRAPPER: Мова (TTS) завершена.")
        return True
    
    logger.warning("WRAPPER: Мова не вдалася.")
    return False


async def action_play_named(action_name: str) -> bool:
    """
    Високорівнева обгортка для виконання попередньо заданої дії (Action).
    """
    logger.info(f"WRAPPER: Запуск дії: '{action_name}'.")
    return await api_client.play_named_action(action_name)


def get_speech_listener_observer():
    """
    Обгортка, що надає об'єкт для прослуховування голосових команд.
    """
    logger.debug("WRAPPER: Надання об'єкта для прослуховування мови.")
    return api_client.create_speech_observer()