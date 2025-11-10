import asyncio
import logging
from mini import mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice
from alpha_mini_pkg.config.settings import (
    ROBOT_IP, 
    ROBOT_PORT, 
    ROBOT_TYPE, 
    LOG_LEVEL, 
    PROGRAM_MODE_WAIT_TIME
)

logger = logging.getLogger(__name__)

def initialize_sdk():
    logger.info(f"Налаштування SDK: Тип Робота={ROBOT_TYPE.name}, Рівень логування={logging.getLevelName(LOG_LEVEL)}")
    
    MiniSdk.set_log_level(LOG_LEVEL)
    MiniSdk.set_robot_type(ROBOT_TYPE)


async def connect_robot() -> WiFiDevice | None:
    device = WiFiDevice(address=ROBOT_IP, port=ROBOT_PORT, name="AlphaMini_Manual") 
    logger.info(f"Спроба прямого підключення до робота за IP: {ROBOT_IP}:{ROBOT_PORT}")
    
    connected: bool = await MiniSdk.connect(device)

    if connected:
        logger.info("Підключення успішне!")
        
        logger.info("Вхід у режим програмування...")
        await MiniSdk.enter_program()

        logger.info(f"Очікування {PROGRAM_MODE_WAIT_TIME} с. на готовність робота...")
        await asyncio.sleep(PROGRAM_MODE_WAIT_TIME) 
        
        logger.info("У режимі програмування. Робот готовий до команд.")
        return device
    else:
        logger.error(f"Не вдалося підключитися до робота за IP {ROBOT_IP}.")
        return None


async def shutdown():
    logger.info("Вихід із режиму програмування...")
    try:
        await MiniSdk.quit_program()
    except Exception as e:
        logger.warning(f"Помилка при виході з режиму програмування: {e}")
        
    logger.info("Відключення та звільнення ресурсів SDK...")
    await MiniSdk.release()
    logger.info("Робот відключено. Ресурси звільнено.")