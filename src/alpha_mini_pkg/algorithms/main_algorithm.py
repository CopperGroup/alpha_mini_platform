# src/alpha_mini_pkg/algorithms/main_algorithm.py

import asyncio
import logging
import re
from alpha_mini_pkg.core import action_walk, action_speak, create_dynamic_listener, MoveRobotDirection
from alpha_mini_pkg.utils.helpers import safe_delay

logger = logging.getLogger(__name__)

# Словник напрямків для парсингу команд
DIRECTION_MAP = {
    "forward": MoveRobotDirection.FORWARD,
    "backward": MoveRobotDirection.BACKWARD,
    "left": MoveRobotDirection.TURN_LEFT,
    "right": MoveRobotDirection.TURN_RIGHT,
}

async def parse_and_execute_walk_command(text: str):
    """
    Спроба вилучити та виконати команду 'walk [N] steps [DIRECTION]'
    Приклад: "walk five steps forward"
    """
    normalized_text = text.strip().lower()
    
    # Патерн: walk <число> steps <напрямок>
    # Регулярний вираз для пошуку "walk [N] steps [direction]"
    match = re.search(r"walk\s+(\d+)\s+steps\s+(" + "|".join(DIRECTION_MAP.keys()) + r")", normalized_text)

    if match:
        steps_str = match.group(1)
        direction_name = match.group(2)
        
        try:
            steps = int(steps_str)
            direction = DIRECTION_MAP[direction_name]

            logger.info(f"ALGORITHM: Парсинг успішний: {steps} кроків, {direction_name}.")
            await action_speak(f"Executing walk of {steps} steps {direction_name}.")
            await action_walk(steps=steps, direction=direction)
            await action_speak("Walk command finished.")
            return True
            
        except ValueError:
            await action_speak("I found numbers, but I couldn't understand the command format.")
            return False
    else:
        logger.debug("ALGORITHM: Не вдалося розпізнати команду 'walk [N] steps [direction]'.")
        return False


async def execute_main_algorithm(text: str):
    """
    Універсальний алгоритм платформи. 
    Він запускає динамічний цикл прослуховування.
    """
    logger.info("ALGORITHM: Запуск Main Algorithm. Вхід у динамічний режим прослуховування.")
    
    await action_speak("Entering dynamic command mode. Say 'walk [number] steps [direction]' or say 'stop' to exit.")

    # Отримуємо цикл подій
    loop = asyncio.get_running_loop()
    
    # 1. Ініціалізація DynamicListener
    listener = create_dynamic_listener(loop)
    
    # 2. Визначення callback для on_speaking
    async def dynamic_callback(speech_text: str):
        """ Викликається при кожному розпізнаванні мови. """
        logger.debug(f"ALGORITHM: Динамічний callback отримав: {speech_text}")
        
        # Спроба виконати складний парсинг
        executed = await parse_and_execute_walk_command(speech_text)
        
        if not executed:
            # Якщо це не команда "walk", даємо просту відповідь
            await action_speak(f"I heard {speech_text}. Please specify a walk command or say stop.")
    
    # 3. Налаштування та запуск прослуховування
    listener.on_speaking(dynamic_callback).stop_when("stop") # Використовуємо 'stop' як custom value

    # 4. Блокування до тих пір, поки не буде сказано "stop"
    stop_text = await listener.start()
    
    await action_speak(f"Exiting dynamic command mode. You said: {stop_text}")
    logger.info("ALGORITHM: Main Algorithm завершено.")