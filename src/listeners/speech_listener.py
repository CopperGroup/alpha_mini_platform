import asyncio
import logging
from mini.apis.api_observe import ObserveSpeechRecognise, SpeechRecogniseResponse
from alpha_mini_pkg.core import robot_command_handler
from alpha_mini_pkg.core.actions_wrapper import get_speech_listener_observer 

logger = logging.getLogger(__name__)

class SpeechCommandListener:
    def __init__(self, main_loop: asyncio.AbstractEventLoop):
        self._observer: ObserveSpeechRecognise = get_speech_listener_observer()
        self._loop = main_loop
        logger.info("LISTENER: Ініціалізовано SpeechCommandListener.")

    def _handle_speech_sdk_response(self, msg: SpeechRecogniseResponse):
        if msg.isSuccess and msg.text:
            recognized_text = msg.text
            logger.info(f"LISTENER: SDK розпізнано голос: '{recognized_text}'")

            self._loop.create_task(
                robot_command_handler.handle_speech_command(recognized_text)
            )
            
        else:
            logger.warning(f"LISTENER: Розпізнавання не вдалося. Код: {msg.resultCode}")

    def start(self):
        logger.info("LISTENER: Починаю прослуховування голосових команд...")
        
        self._observer.set_handler(self._handle_speech_sdk_response)
        self._observer.start()
        
        logger.info("Прослуховування активне. Готово до розпізнавання.")

    def stop(self):
        self._observer.stop()
        logger.info("Прослуховування голосових команд зупинено.")

def start_listening(main_loop: asyncio.AbstractEventLoop) -> SpeechCommandListener:
    listener = SpeechCommandListener(main_loop)
    listener.start()
    return listener