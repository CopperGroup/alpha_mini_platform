import logging
from mini.apis.api_action import MoveRobotDirection 
from alpha_mini_pkg.services import api_client 
from alpha_mini_pkg.utils.helpers import estimate_tts_duration, safe_delay

logger = logging.getLogger(__name__)

async def action_walk(steps: int, direction: MoveRobotDirection = MoveRobotDirection.FORWARD) -> bool:
    logger.info(f"WRAPPER: Запуск руху: {direction.name}, {steps} кроків.")
    return await api_client.move_robot(steps=steps, direction=direction)


async def action_speak(text: str) -> bool:
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
    logger.info(f"WRAPPER: Запуск дії: '{action_name}'.")
    return await api_client.play_named_action(action_name)


def get_speech_listener_observer():
    logger.debug("WRAPPER: Надання об'єкта для прослуховування мови.")
    return api_client.create_speech_observer()