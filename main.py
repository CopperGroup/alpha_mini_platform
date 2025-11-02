# main.py

import asyncio
import sys 
import logging
# Імпорти для ініціалізації та запуску
from alpha_mini_pkg.services import connection_manager 
from listeners import start_listening # Ця функція в 'listeners/speech_listener.py' запускає CommandHandler
from alpha_mini_pkg.config.settings import LOG_LEVEL 

# --- Налаштування Глобального Логування ---
logging.basicConfig(level=LOG_LEVEL, 
                    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Основна Програма ---
async def main():
    """
    Основна асинхронна функція: ініціалізація SDK, підключення та запуск 
    слухача, який керується CommandHandler.
    """
    # 1. Ініціалізація SDK
    connection_manager.initialize_sdk()
    
    # 2. Підключення до Робота
    device = await connection_manager.connect_robot() 

    if device:
        # Отримуємо поточний цикл подій
        loop = asyncio.get_running_loop()
        
        # 3. Запускаємо прослуховування команд
        # Слухач постійно працює і передає розпізнаний текст до robot_command_handler.
        listener = start_listening(loop) 

        logger.info("\n✅ Платформа активована. Скажіть 'start' або 'hello'. Натисніть Ctrl+C, щоб зупинити.")
        
        try:
            # 4. Чекаємо нескінченно
            await asyncio.Future() 

        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("\n👋 Програма перервана.")
        finally:
            # 5. Чисте завершення роботи
            listener.stop()
            await connection_manager.shutdown()
    else:
        logger.error("🛑 Не вдалося підключитися. Робоча логіка не запущена.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nProgram exited via Keyboard Interrupt.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled error during execution: {e}", exc_info=True)
        sys.exit(1)