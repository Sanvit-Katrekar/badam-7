''' All game constants are defined here '''

from enum import Enum, auto
import sys

class Mode:
    PRODUCTION = 0
    DEVELOPMENT = 1

ENV_LOCATION = sys.path[0] + '/.env'
EMPTY_SLOTS = 35

CONFIGURATION_MODE = Mode.PRODUCTION
