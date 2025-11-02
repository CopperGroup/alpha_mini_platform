# src/alpha_mini_pkg/__init__.py

# Експортуємо лише ключові компоненти, а не конкретні функції дій
from .services.connection_manager import connect_robot, shutdown
from .core.command_handler import robot_command_handler

__all__ = [
    # Для загального керування підключенням
    'connect_robot',
    'shutdown',
    # Для прямого доступу до диспетчера команд
    'robot_command_handler',
]