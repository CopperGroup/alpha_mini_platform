# src/alpha_mini_pkg/launcher.py

import asyncio
import sys 
import logging
# Всі імпорти тепер працюють як внутрішні імпорти пакету
from alpha_mini_pkg.services import connection_manager 
from alpha_mini_pkg.config.settings import LOG_LEVEL 
from listeners import start_listening 

# --- Налаштування Глобального Логування ---
logging.basicConfig(level=LOG_LEVEL, 
                    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# 1. АСИНХРОННА ФУНКЦІЯ (Містить логіку програми)
# ----------------------------------------------------------------------

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
        loop = asyncio.get_running_loop()
        listener = start_listening(loop) 

        logger.info("\n✅ Платформа активована. Скажіть 'start' або 'hello'. Натисніть Ctrl+C, щоб зупинити.")
        
        try:
            # Чекаємо нескінченно
            await asyncio.Future() 

        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("\n👋 Програма перервана.")
        finally:
            # Чисте завершення роботи
            listener.stop()
            await connection_manager.shutdown()
    else:
        logger.error("🛑 Не вдалося підключитися. Робоча логіка не запущена.")


# ----------------------------------------------------------------------
# 2. СИНХРОННА ОБГОРТКА (Нова точка входу для setup.py)
# ----------------------------------------------------------------------

def run():
    """
    Синхронна функція, яка є консольною точкою входу.
    Вона викликає asyncio.run() для безпечного запуску асинхронного коду.
    """
    try:
        # Запуск асинхронної функції main()
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nProgram exited via Keyboard Interrupt.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled error during execution: {e}", exc_info=True)
        sys.exit(1)