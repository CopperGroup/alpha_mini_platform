import logging
from mini.mini_sdk import RobotType

ROBOT_IP: str = "192.168.137.6"
ROBOT_PORT: int = 8800
ROBOT_TYPE: RobotType = RobotType.EDU
LOG_LEVEL: int = logging.INFO

TARGET_COMMAND: str = "good boy"

DEFAULT_STEPS: int = 5

PROGRAM_MODE_WAIT_TIME: int = 6
