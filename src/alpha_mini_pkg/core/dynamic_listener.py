# src/alpha_mini_pkg/core/dynamic_listener.py

import asyncio
import logging
from typing import Callable, Coroutine, Any, Optional
from mini.apis.api_observe import SpeechRecogniseResponse
# ВИПРАВЛЕННЯ ЦИКЛІЧНОГО ІМПОРТУ: Імпортуємо необхідні функції напряму
from .actions_wrapper import get_speech_listener_observer, action_speak 

logger = logging.getLogger(__name__)

# Типи для обробників
SpeechCallback = Callable[[str], Coroutine]

class DynamicListener:
    """
    Клас, що обгортає SDK ObserveSpeechRecognise, надаючи динамічний
    інтерфейс для керування прослуховуванням, включаючи:
    - Реєстрацію обробників для кожної розпізнаної фрази (on_speaking).
    - Умову автоматичної зупинки (stop_when).
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        # Отримуємо об'єкт спостерігача через обгортку CORE
        # Тепер імпортовано напряму з actions_wrapper
        self._observer = get_speech_listener_observer() 
        self._is_listening = False
        self._on_speaking_callback: Optional[SpeechCallback] = None
        self._stop_phrase: Optional[str] = None
        self._stop_future: Optional[asyncio.Future] = None
        logger.info("DYNAMIC_LISTENER: Ініціалізовано.")

    # --- Публічний API (Керування станом) ---

    def on_speaking(self, callback: SpeechCallback):
        """ Реєструє асинхронну функцію, яка викликається при розпізнаванні мови. """
        self._on_speaking_callback = callback
        logger.debug("DYNAMIC_LISTENER: Обробник on_speaking зареєстровано.")
        return self # Повертаємо self для ланцюгового виклику

    def stop_when(self, key_phrase: str):
        """ Встановлює ключову фразу, при розпізнаванні якої прослуховування зупиниться. """
        self._stop_phrase = key_phrase.strip().lower()
        logger.debug(f"DYNAMIC_LISTENER: Умова зупинки встановлена: '{self._stop_phrase}'")
        return self

    def _internal_handler(self, msg: SpeechRecogniseResponse):
        """ Обробник, який викликається безпосередньо з SDK. """
        if not self._is_listening:
            return

        if msg.isSuccess and msg.text:
            text = msg.text
            normalized_text = text.strip().lower()
            logger.info(f"DYNAMIC_LISTENER: Розпізнано: '{normalized_text}'")

            # 1. Перевірка умови зупинки
            if self._stop_phrase and self._stop_phrase in normalized_text:
                logger.info(f"DYNAMIC_LISTENER: Умова зупинки '{self._stop_phrase}' виконана.")
                # Завершуємо прослуховування і сигналізуємо про завершення
                self.stop() 
                if self._stop_future and not self._stop_future.done():
                    self._loop.call_soon_threadsafe(self._stop_future.set_result, normalized_text)
                return

            # 2. Виклик користувацького обробника (on_speaking)
            if self._on_speaking_callback:
                # Запускаємо callback як окрему задачу, щоб не блокувати SDK
                self._loop.create_task(self._on_speaking_callback(text))
        else:
            logger.warning(f"DYNAMIC_LISTENER: Помилка розпізнавання: {msg.resultCode}")

    async def start(self) -> str:
        """ 
        Запускає динамічне прослуховування.
        Блокується до тих пір, поки не буде викликано stop() або не спрацює умова stop_when.
        Повертає текст, який викликав зупинку, або порожній рядок.
        """
        if self._is_listening:
            logger.warning("DYNAMIC_LISTENER: Вже прослуховується.")
            return ""

        self._is_listening = True
        self._observer.set_handler(self._internal_handler)
        self._observer.start()
        logger.info("DYNAMIC_LISTENER: Динамічне прослуховування розпочато.")

        # Чекаємо нескінченно, поки не спрацює умова зупинки
        self._stop_future = self._loop.create_future()
        try:
            result = await self._stop_future
            return result # Повертаємо результат, встановлений у _internal_handler
        except asyncio.CancelledError:
            self.stop()
            return ""
        finally:
            # Фінальна чиста зупинка на випадок, якщо future було скасовано ззовні
            self.stop() 

    def stop(self):
        """ Зупиняє прослуховування і очищує стан. """
        if self._is_listening:
            self._observer.stop()
            self._is_listening = False
            logger.info("DYNAMIC_LISTENER: Динамічне прослуховування зупинено.")

# --- Функція для ініціалізації ---
def create_dynamic_listener(loop: asyncio.AbstractEventLoop) -> DynamicListener:
    """ Створює і повертає новий екземпляр DynamicListener. """
    return DynamicListener(loop)