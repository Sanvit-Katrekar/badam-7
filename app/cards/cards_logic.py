from enum import Enum
from abc import ABC, abstractmethod
from .constants import *
import random

#IMAGES_PATH = r"/Users/sanvit/Desktop/Projects To DO/badam-7/app/static/images/"
IMAGES_PATH = r"static/images/"

class Card(ABC):
    @abstractmethod
    def __init__(self, suit: CardSuit, status: CardStatus | None = None):
        self.name = type(self).__name__
        if self.name.lstrip('N').isdigit():
            self.sym = self.name.lstrip('N')
        else:
            self.sym = self.name[0]
        self.points = self.get_card_points(self.name)
        self.suit = suit
        self.status = DEFAULT_CARD_STATUS if status is None else status
        self.image_path = self.get_image_path()

    @staticmethod
    def get_card_points(card_name: str):
        if card_name not in VALID_CARDS:
            print("Heh")
            return
        points = list(VALID_CARDS).index(card_name) + 1
        return points
    
    def set_open(self):
        self.status = CardStatus.OPEN
    
    def set_closed(self):
        self.status = CardStatus.CLOSED
    
    def toggle_status(self):
        self.status = CardStatus.OPEN if self.status == CardStatus.CLOSED else CardStatus.CLOSED
    
    def __str__(self):
        WIDTH = 26
        display_str = f'''
        +----------------------------+
        | ''' + self.name.center(WIDTH + 1) + '|' + \
        f'''
        +----------------------------+
        | sym = {self.sym}{' ' * (WIDTH - len('sym = ') - len(self.sym))} |
        | points = {self.points}{' ' * (WIDTH - len('points = ') - len(str(self.points)))} |
        | suit = {self.suit}{' ' * (WIDTH - len('suit = ') - len(str(self.suit)))} |      
        | status = {self.status}{' ' * (WIDTH - len('status = ') - len(str(self.status)))} |
        +----------------------------+
        {self.image_path}
        '''
        return display_str
    
    def __eq__(self, other):
        return self.name == other.name and \
            self.suit == other.suit and \
            self.status == other.status
    
    def get_image_path(self):
        NAME_FORMAT = IMAGE_NUM_NAME_FORMAT if self.name in NUMBER_CARDS else IMAGE_NAME_FORMAT
        img_name = '-'.join(
            str(eval(f'self.{attr}', {'self': self}))\
                .removeprefix('CardSuit.')\
                .lstrip('N')\
                .upper()
            for attr in NAME_FORMAT
        ) + '.svg'
        return IMAGES_PATH + img_name
    
    @staticmethod
    def from_json(card: dict):
        flag = True
        suit = None
        status = None
        if card['name'].title() in VALID_CARDS:
            CardClass = eval(card['name'].title())
        else:
            flag = False

        for card_suit in CardSuit:
            if card_suit.value == card['suit'][0]:
                suit = card_suit
                break
        else:
            flag = False

        for card_status in CardStatus:
            if str(card_status.value) == card['status']:
                status = card_status
                break
        else:
            flag = False

        if not flag:
            return
        return CardClass(suit, status)
        


        return redirect(url_for('play'))
    
class Ace(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N2(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N3(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N4(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)
    
class N5(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N6(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N7(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N8(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N9(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class N10(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class Jack(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class Queen(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class King(Card):
    def __init__(self, suit: CardSuit, status: CardStatus = None):
        super().__init__(suit, status)

class Hand:
    def __init__(self) -> None:
        self.cards = [] #A stack with top at self.cards[-1]
        self.display_msg = 'Showing Hand:'
    
    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def pick_top(self) -> Card:
        return self.cards.pop()
    
    def pick_card(self, card: Card) -> Card | None:
        try:
            return self.cards.pop(self.cards.index(card))
        except ValueError:
            print("Card not in hand!")
        return

    def shuffle(self):
        random.shuffle(self.cards)
    
    def sort(self, criteria: SortCriteria = DEFAULT_SORT_CRITERIA):
        card_suit_order = list(CardSuit)
        if criteria == SortCriteria.SUIT_THEN_POINTS:
            self.cards.sort(key=lambda card: (card_suit_order.index(card.suit), card.points))
        elif criteria == SortCriteria.ONLY_POINTS:
            self.cards.sort(key=lambda card: card.points)
        elif criteria == SortCriteria.ONLY_SUIT:
            self.cards.sort(key=lambda card: card_suit_order.index(card.suit))

    def __len__(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        if len(self) == 0:
            return f'{type(self).__name__} is empty!'
        display_str = f'''
        {self.display_msg}
        ----------------'''
        for card in self.cards:
            display_str += str(card)
        return display_str

class Deck(Hand):
    def __init__(self) -> None:
        self.display_msg = 'Displaying Deck:'
        self.cards = self.generate_card_deck()
        self.shuffle()

    def distribute_cards(self, hands: list[Hand], max_cards_in_hand: int | None = None):
        if max_cards_in_hand is None:
            max_cards_in_hand = len(self)
        count = 0
        n_hands = len(hands)
        while count < max_cards_in_hand:
            index = count % n_hands
            deck_top_card = self.pick_top()
            hands[index].add_card(deck_top_card)
            count += 1

    @staticmethod
    def generate_card_deck() -> list[Card]:
        cards = []
        for suit in CardSuit:
            for card_name in VALID_CARDS:
                cards.append(eval(f'{card_name}({suit})'))
        return cards
    
if __name__ == '__main__':
    '''
    deck = Deck()
    hands = [Hand() for _ in range(4)]
    deck.distribute_cards(hands)
    hands[0].sort()
    print(hands[0], 'Length:', len(hands[0]))
    print(deck)
    '''
    deck = Deck()
    print(deck)
    hands = [Hand() for _ in range(6)]
    deck.distribute_cards(hands)
    hands = hands[:2]
    print(vars(hands[0])['cards'][0].__dict__)
