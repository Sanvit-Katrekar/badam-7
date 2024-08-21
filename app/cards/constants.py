from enum import Enum, auto

MINIMUM_CARD_POINTS = 1
MAXIMUM_CARD_POINTS = 13

ACE_CARD = {'Ace': 'A'}
NUMBER_CARDS = dict(
    zip(
        tuple(['N' + str(i) for i in range(2, 11)]),
        tuple([str(i) for i in range(2, 11)])
    )
)
FACE_CARDS = {'Jack': 'J', 'Queen': 'Q', 'King': 'K'}
VALID_CARDS = ACE_CARD | NUMBER_CARDS | FACE_CARDS

EMPTY_SYM = 'x'

class CardStatus(Enum):
    CLOSED = 0
    OPEN = auto()

class CardStackDisplay(Enum):
    STACKED = 0
    COVERED = auto()

class CardSuit(Enum):
    BADAM = 'B'
    ESPIK = 'E'
    CHAUKAT = 'C'
    KILVER = 'K'

class SortCriteria(Enum):
    SUIT_THEN_POINTS = 0
    ONLY_POINTS = auto()
    ONLY_SUIT = auto()

DEFAULT_CARD_STATUS = CardStatus.CLOSED
DEFAULT_CARD_STACK_DISPLAY = CardStackDisplay.COVERED
DEFAULT_SORT_CRITERIA = SortCriteria.SUIT_THEN_POINTS

IMAGE_NAME_FORMAT = ('suit', 'points', 'name')
IMAGE_NUM_NAME_FORMAT = ('suit', 'points')

BOARD_DIMENSIONS = (13, 13)

BOARD_ELEMENT_WIDTH = 3
