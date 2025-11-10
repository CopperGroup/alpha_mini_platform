import asyncio
import sys 
import logging
from alpha_mini_pkg.services import connection_manager 
from alpha_mini_pkg.config.settings import LOG_LEVEL 
from listeners import start_listening 

logging.basicConfig(level=LOG_LEVEL, 
                    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)

async def main():
    connection_manager.initialize_sdk()
    device = await connection_manager.connect_robot() 

    if device:
        loop = asyncio.get_running_loop()
        listener = start_listening(loop) 

        logger.info("\nПлатформа активована. Скажіть 'start' або 'hello'. Натисніть Ctrl+C, щоб зупинити.")
        
        try:
            await asyncio.Future() 

        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("\nПрограма перервана.")
        finally:
            listener.stop()
            await connection_manager.shutdown()
    else:
        logger.error("Не вдалося підключитися. Робоча логіка не запущена.")

def run():
    """
    Синхронна функція, яка є консольною точкою входу.
    Вона викликає asyncio.run() для безпечного запуску асинхронного коду.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nProgram exited via Keyboard Interrupt.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled error during execution: {e}", exc_info=True)
        sys.exit(1)