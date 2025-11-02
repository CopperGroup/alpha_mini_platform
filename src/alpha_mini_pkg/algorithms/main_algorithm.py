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
    "leftward": MoveRobotDirection.LEFTWARD,
    "rightward": MoveRobotDirection.RIGHTWARD,
}

# --- НОВИЙ/ОНОВЛЕНИЙ КОД ПАРСИНГУ ---

async def parse_and_execute_walk_command(text: str) -> bool:
    """
    Спроба вилучити та виконати команду 'walk [N] steps [DIRECTION]'
    Тепер більш толерантний до зайвих слів та розділових знаків.
    """
    normalized_text = text.strip().lower()
    
    # Регулярний вираз:
    # 1. Починаємо з \bwalk\b (точне слово walk)
    # 2. Далі йде число (\d+)
    # 3. Далі 'steps' або 'step' (необов'язково)
    # 4. Завершується одним із напрямків
    # 5. Використовуємо .*[^\w] для пошуку всього, що є після команди.
    
    # Використовуємо r"(?:steps?)" для необов'язкового 'steps' або 'step'
    pattern = r"\bwalk\s+(\d+)\s*(?:steps?)?\s+(" + "|".join(DIRECTION_MAP.keys()) + r")\b"
    
    match = re.search(pattern, normalized_text)

    if match:
        # match.group(1) - це число кроків
        # match.group(2) - це назва напрямку
        steps_str = match.group(1)
        direction_name = match.group(2)
        
        try:
            steps = int(steps_str)
            direction = DIRECTION_MAP[direction_name]
            
            # Обмеження кроків, щоб уникнути помилок SDK
            if steps > 20:
                steps = 20
                await action_speak("I limited the steps to 20 for safety.")

            logger.info(f"ALGORITHM: Парсинг успішний: {steps} кроків, {direction_name}.")
            await action_speak(f"Executing walk of {steps} steps {direction_name}.")
            
            # Виконання дії
            await action_walk(steps=steps, direction=direction)
            
            await action_speak("Walk command finished.")
            return True
            
        except ValueError:
            # Цей блок, ймовірно, ніколи не спрацює, оскільки regex перевіряє число
            await action_speak("I couldn't process the numbers in your command.")
            return False
    else:
        logger.debug(f"ALGORITHM: Не вдалося розпізнати команду. Шукали патерн: {pattern}")
        return False

# --- execute_main_algorithm залишається незмінним ---

async def execute_main_algorithm(text: str):
    """
    Універсальний алгоритм платформи. 
    Запускає DynamicListener у фоновій задачі, щоб уникнути втрати команд під час TTS.
    """
    logger.info("ALGORITHM: Запуск Main Algorithm. Вхід у динамічний режим прослуховування.")
    
    loop = asyncio.get_running_loop()
    
    # 1. Ініціалізація та налаштування DynamicListener
    listener = create_dynamic_listener(loop)
    
    async def dynamic_callback(speech_text: str):
        """ Викликається при кожному розпізнаванні мови. """
        logger.debug(f"ALGORITHM: Динамічний callback отримав: {speech_text}")
        
        # Використовуємо parse_and_execute_walk_command
        executed = await parse_and_execute_walk_command(speech_text)
        
        if not executed:
            await action_speak(f"I heard {speech_text}. Please specify a walk command or say stop.")
    
    # 2. Налаштування умов
    listener.on_speaking(dynamic_callback).stop_when("stop") 
    
    # 3. ЗАПУСК DynamicListener як фонової задачі
    listener_task = loop.create_task(listener.start()) 
    
    # 4. Мова (TTS): Тепер робот говорить, поки слухач вже активний.
    await action_speak("Entering dynamic command mode. Say 'walk [number] steps [direction]' or say 'stop' to exit.")

    # 5. Очікування: Чекаємо на завершення фонової задачі (коли буде сказано "stop")
    stop_text = await listener_task
    
    # 6. Завершення
    await action_speak(f"Exiting dynamic command mode. You said: {stop_text}")
    logger.info("ALGORITHM: Main Algorithm завершено.")