import asyncio
import logging
from typing import Callable, Coroutine, Any, Optional
from mini.apis.api_observe import SpeechRecogniseResponse
from .actions_wrapper import get_speech_listener_observer, action_speak 

logger = logging.getLogger(__name__)
SpeechCallback = Callable[[str], Coroutine]

class DynamicListener:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._observer = get_speech_listener_observer() 
        self._is_listening = False
        self._on_speaking_callback: Optional[SpeechCallback] = None
        self._stop_phrase: Optional[str] = None
        self._stop_future: Optional[asyncio.Future] = None
        logger.info("DYNAMIC_LISTENER: Ініціалізовано.")

    def on_speaking(self, callback: SpeechCallback):
        self._on_speaking_callback = callback
        logger.debug("DYNAMIC_LISTENER: Обробник on_speaking зареєстровано.")
        return self

    def stop_when(self, key_phrase: str):
        self._stop_phrase = key_phrase.strip().lower()
        logger.debug(f"DYNAMIC_LISTENER: Умова зупинки встановлена: '{self._stop_phrase}'")
        return self

    def _internal_handler(self, msg: SpeechRecogniseResponse):
        if not self._is_listening:
            return

        if msg.isSuccess and msg.text:
            text = msg.text
            normalized_text = text.strip().lower()
            logger.info(f"DYNAMIC_LISTENER: Розпізнано: '{normalized_text}'")

            if self._stop_phrase and self._stop_phrase in normalized_text:
                logger.info(f"DYNAMIC_LISTENER: Умова зупинки '{self._stop_phrase}' виконана.")
                self.stop() 
                if self._stop_future and not self._stop_future.done():
                    self._loop.call_soon_threadsafe(self._stop_future.set_result, normalized_text)
                return

            if self._on_speaking_callback:
                self._loop.create_task(self._on_speaking_callback(text))
        else:
            logger.warning(f"DYNAMIC_LISTENER: Помилка розпізнавання: {msg.resultCode}")

    async def start(self) -> str:
        if self._is_listening:
            logger.warning("DYNAMIC_LISTENER: Вже прослуховується.")
            return ""

        self._is_listening = True
        self._observer.set_handler(self._internal_handler)
        self._observer.start()
        logger.info("DYNAMIC_LISTENER: Динамічне прослуховування розпочато.")

        self._stop_future = self._loop.create_future()
        try:
            result = await self._stop_future
            return result
        except asyncio.CancelledError:
            self.stop()
            return ""
        finally:
            self.stop() 

    def stop(self):
        if self._is_listening:
            self._observer.stop()
            self._is_listening = False
            logger.info("DYNAMIC_LISTENER: Динамічне прослуховування зупинено.")

def create_dynamic_listener(loop: asyncio.AbstractEventLoop) -> DynamicListener:
    return DynamicListener(loop)