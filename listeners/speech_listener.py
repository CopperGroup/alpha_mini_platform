# listeners/speech_listener.py

import asyncio
import logging
from mini.apis.api_observe import ObserveSpeechRecognise, SpeechRecogniseResponse
# Імпорт обробника команд із CORE
from alpha_mini_pkg.core import robot_command_handler
# Імпорт функції-обгортки для отримання об'єкта слухача з CORE
from alpha_mini_pkg.core import get_speech_listener_observer 

logger = logging.getLogger(__name__)

class SpeechCommandListener:
    """
    Клас, що відповідає за запуск та керування фоновим прослуховуванням 
    голосових команд Alpha Mini. 
    Він виступає як міст між SDK та CommandHandler.
    """

    def __init__(self, main_loop: asyncio.AbstractEventLoop):
        # Отримуємо об'єкт спостерігача через обгортку CORE
        self._observer: ObserveSpeechRecognise = get_speech_listener_observer()
        self._loop = main_loop
        logger.info("LISTENER: Ініціалізовано SpeechCommandListener.")

    def _handle_speech_sdk_response(self, msg: SpeechRecogniseResponse):
        """ 
        Приватний обробник, який викликається безпосередньо при надходженні 
        відповіді від Alpha Mini SDK.
        """
        
        if msg.isSuccess and msg.text:
            recognized_text = msg.text
            logger.info(f"LISTENER: SDK розпізнано голос: '{recognized_text}'")
            
            # КЛЮЧОВИЙ МОМЕНТ: Передача команди до CommandHandler
            # Ми запускаємо обробку команди як окрему задачу в основному циклі подій, 
            # щоб не блокувати низькорівневий потік SDK.
            self._loop.create_task(
                robot_command_handler.handle_speech_command(recognized_text)
            )
            
        else:
            logger.warning(f"LISTENER: Розпізнавання не вдалося. Код: {msg.resultCode}")
            # Можна додати логіку для обробки помилок розпізнавання (наприклад, тиша).

    def start(self):
        """ Починає прослуховування голосових команд. """
        logger.info("LISTENER: Починаю прослуховування голосових команд...")
        
        # 1. Встановлюємо наш обробник як callback для об'єкта SDK
        self._observer.set_handler(self._handle_speech_sdk_response)
        
        # 2. Запускаємо спостерігач
        self._observer.start()
        
        logger.info("✅ Прослуховування активне. Готово до розпізнавання.")

    def stop(self):
        """ Зупиняє прослуховування голосових команд. """
        self._observer.stop()
        logger.info("🛑 Прослуховування голосових команд зупинено.")


# --- Функція, яку викликає main.py ---

def start_listening(main_loop: asyncio.AbstractEventLoop) -> SpeechCommandListener:
    """
    Створює та запускає екземпляр слухача.

    :param main_loop: Поточний цикл подій asyncio.
    :return: Активний об'єкт SpeechCommandListener.
    """
    listener = SpeechCommandListener(main_loop)
    listener.start()
    return listener