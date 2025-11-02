# src/alpha_mini_pkg/core/command_handler.py

import logging
from typing import Callable, Coroutine
from alpha_mini_pkg.core import actions_wrapper
# Ледачий імпорт для алгоритму залишається
# from alpha_mini_pkg.algorithms import execute_main_algorithm 

logger = logging.getLogger(__name__)

CommandHandlerBlock = Callable[[str], Coroutine]

class CommandHandler:
    
    def __init__(self):
        self._command_map: dict[str, CommandHandlerBlock] = {}
        # НОВИЙ СТАН: Прапор, що вказує, чи активний динамічний режим
        self.is_dynamic_mode_active: bool = False
        self.register_handler("start", self._handle_main_algorithm_trigger)
        self.register_handler("hello", lambda t: actions_wrapper.action_speak("Hello, I am ready."))
        
    def register_handler(self, key_phrase: str, handler_func: CommandHandlerBlock):
        key = key_phrase.strip().lower()
        self._command_map[key] = handler_func
    
    async def _handle_main_algorithm_trigger(self, text: str):
        """ Обробник для команди 'start'. Встановлює прапор активності. """
        
        if self.is_dynamic_mode_active:
             # Запобігаємо повторному запуску, якщо вже активний
            await actions_wrapper.action_speak("Dynamic mode is already running.")
            return

        from alpha_mini_pkg.algorithms import execute_main_algorithm 

        logger.info("HANDLER: Розпізнано команду 'start'. Запуск Main Algorithm.")
        self.is_dynamic_mode_active = True # !!! ВСТАНОВЛЮЄМО ПРАПОР !!!
        
        try:
            await execute_main_algorithm(text)
        except Exception as e:
            logger.error(f"HANDLER: Помилка виконання алгоритму: {e}")
            await actions_wrapper.action_speak("An error occurred in the main algorithm.")
        finally:
            self.is_dynamic_mode_active = False # !!! ЗНИМАЄМО ПРАПОР ПІСЛЯ ЗАВЕРШЕННЯ !!!
            logger.info("HANDLER: Main Algorithm завершено. Динамічний режим вимкнено.")
        
    async def handle_speech_command(self, text: str):
        """
        Основний метод: знаходить відповідний обробник для тексту та виконує його.
        """
        if self.is_dynamic_mode_active:
            # ІГНОРУЄМО: Якщо алгоритм активний, всі команди ігноруються постійним слухачем.
            logger.debug(f"HANDLER: Ігнорую команду '{text}' (Динамічний режим активний).")
            return
        
        # ... (решта логіки CommandHandler залишається незмінною)
        
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
                await actions_wrapper.action_speak("Error during command execution.")
        else:
            logger.debug(f"HANDLER: Не знайдено обробника для '{normalized_text}'.")
            await actions_wrapper.action_speak(f"I heard {text}, but I'll only respond to 'start' or 'hello'.")


# Створюємо глобальний або синглтон екземпляр обробника
robot_command_handler = CommandHandler()