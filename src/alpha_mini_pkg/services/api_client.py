import logging
from mini.apis.api_action import MoveRobot, MoveRobotDirection, PlayAction
from mini.apis.api_sound import StartPlayTTS
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice

logger = logging.getLogger(__name__)

ApiResult = tuple[MiniApiResultType, WiFiDevice | object] 

async def move_robot(steps: int, direction: MoveRobotDirection) -> bool:
    logger.debug(f"API: Виконання руху: {direction.name}, кроків: {steps}")
    
    move_block: MoveRobot = MoveRobot(step=steps, direction=direction)
    (result_type, response) = await move_block.execute()

    if result_type == MiniApiResultType.Success and response.isSuccess:
        logger.debug("API: Рух завершено успішно.")
        return True
    else:
        logger.error(f"API: Помилка руху: {result_type}, Відповідь: {response}")
        return False


async def start_tts(text: str) -> bool:
    logger.debug(f'API: Запуск TTS: "{text[:30]}..."')
    
    tts_block: StartPlayTTS = StartPlayTTS(text=text)
    (result_type, response) = await tts_block.execute()
    if result_type == MiniApiResultType.Success and response.isSuccess:
        logger.debug("API: TTS запущено успішно.")
        return True
    else:
        logger.error(f"API: Помилка запуску TTS: {result_type}, Відповідь: {response}")
        return False


async def play_named_action(action_name: str) -> bool:
    logger.debug(f'API: Запуск дії: "{action_name}"')
    
    play_block: PlayAction = PlayAction(action_name=action_name)
    (result_type, response) = await play_block.execute()

    if result_type == MiniApiResultType.Success and response.isSuccess:
        logger.debug(f"API: Дія '{action_name}' запущена успішно.")
        return True
    else:
        logger.error(f"API: Помилка запуску дії '{action_name}': {result_type}, Відповідь: {response}")
        return False


def create_speech_observer() -> ObserveSpeechRecognise:
    logger.debug("API: Створення об'єкта ObserveSpeechRecognise.")
    return ObserveSpeechRecognise()