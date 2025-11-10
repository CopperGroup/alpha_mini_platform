import asyncio
import logging
import re
from alpha_mini_pkg.core import action_walk, action_speak, create_dynamic_listener, MoveRobotDirection
from alpha_mini_pkg.utils.helpers import safe_delay

logger = logging.getLogger(__name__)

DIRECTION_MAP = {
    "forward": MoveRobotDirection.FORWARD,
    "backward": MoveRobotDirection.BACKWARD,
    "leftward": MoveRobotDirection.LEFTWARD,
    "rightward": MoveRobotDirection.RIGHTWARD,
}

async def parse_and_execute_walk_command(text: str) -> bool:
    normalized_text = text.strip().lower()

    pattern = r"\bwalk\s+(\d+)\s*(?:steps?)?\s+(" + "|".join(DIRECTION_MAP.keys()) + r")\b"
    
    match = re.search(pattern, normalized_text)

    if match:
        steps_str = match.group(1)
        direction_name = match.group(2)
        
        try:
            steps = int(steps_str)
            direction = DIRECTION_MAP[direction_name]
            
            if steps > 20:
                steps = 20
                await action_speak("I limited the steps to 20 for safety.")

            logger.info(f"ALGORITHM: Парсинг успішний: {steps} кроків, {direction_name}.")
            await action_speak(f"Executing walk of {steps} steps {direction_name}.")

            await action_walk(steps=steps, direction=direction)
            
            await action_speak("Walk command finished.")
            return True
            
        except ValueError:
            await action_speak("I couldn't process the numbers in your command.")
            return False
    else:
        logger.debug(f"ALGORITHM: Не вдалося розпізнати команду. Шукали патерн: {pattern}")
        return False

async def execute_main_algorithm(text: str):
    logger.info("ALGORITHM: Запуск Main Algorithm. Вхід у динамічний режим прослуховування.")
    
    loop = asyncio.get_running_loop()

    listener = create_dynamic_listener(loop)
    
    async def dynamic_callback(speech_text: str):
        logger.debug(f"ALGORITHM: Динамічний callback отримав: {speech_text}")

        executed = await parse_and_execute_walk_command(speech_text)
        
        if not executed:
            await action_speak(f"I heard {speech_text}. Please specify a walk command or say stop.")

    listener.on_speaking(dynamic_callback).stop_when("stop") 
    listener_task = loop.create_task(listener.start()) 
    await action_speak("Entering dynamic command mode. Say 'walk [number] steps [direction]' or say 'stop' to exit.")
    stop_text = await listener_task
    await action_speak(f"Exiting dynamic command mode. You said: {stop_text}")
    logger.info("ALGORITHM: Main Algorithm завершено.")