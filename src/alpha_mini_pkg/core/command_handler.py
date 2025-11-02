# src/alpha_mini_pkg/core/command_handler.py

import logging
from typing import Callable, Coroutine
from alpha_mini_pkg.core import actions_wrapper
from alpha_mini_pkg.algorithms import execute_main_algorithm # Імпорт універсального алгоритму

logger = logging.getLogger(__name__)

CommandHandlerBlock = Callable[[str], Coroutine]

class CommandHandler:
    """
    Мінімалістичний диспетчер, що відповідає лише за запуск основної логіки.
    """

    def __init__(self):
        # Ми реєструємо лише одну-дві команди
        self._command_map: dict[str, CommandHandlerBlock] = {}
        self.register_handler("start", self._handle_main_algorithm_trigger)
        self.register_handler("hello", lambda t: actions_wrapper.action_speak("Hello, I am ready."))
        
    def register_handler(self, key_phrase: str, handler_func: CommandHandlerBlock):
        """ Реєструє новий обробник. """
        key = key_phrase.strip().lower()
        self._command_map[key] = handler_func
    
    async def _handle_main_algorithm_trigger(self, text: str):
        """ Обробник для команди 'start'. """
        logger.info("HANDLER: Розпізнано команду 'start'. Запуск Main Algorithm.")
        await execute_main_algorithm(text)
        
    async def handle_speech_command(self, text: str):
        """
        Основний метод: знаходить відповідний обробник для тексту та виконує його.
        """
        normalized_text = text.strip().lower()
        logger.info(f"HANDLER: Отримано команду: '{normalized_text}'")

        # 1. Пошук
        matched_handler = None
        for key_phrase, handler_func in self._command_map.items():
            if key_phrase in normalized_text:
                matched_handler = handler_func
                break

        # 2. Виконання
        if matched_handler:
            logger.info("HANDLER: Виконання команди...")
            try:
                await matched_handler(text) 
                logger.info("HANDLER: Виконання завершено.")
            except Exception as e:
                logger.error(f"HANDLER: Помилка виконання: {e}")
                await actions_wrapper.action_speak("Error during algorithm execution.")
        else:
            logger.debug(f"HANDLER: Невідома команда: '{normalized_text}'.")
            await actions_wrapper.action_speak(f"I heard {text}, but I'll only respond to 'start' or 'hello'.")

# Створюємо глобальний або синглтон екземпляр обробника
robot_command_handler = CommandHandler()