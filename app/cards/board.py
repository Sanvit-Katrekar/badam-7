from constants import *
from utils import print_matrix
from cards_logic import *

class Board:
    def __init__(self) -> None:
        self.matrix = [
            [EMPTY_SYM.center(BOARD_ELEMENT_WIDTH) for _ in range(BOARD_DIMENSIONS[1])] 
            for _ in range(BOARD_DIMENSIONS[0])
        ]
    def add_card(self, row: int, col: int, card: Card, hand: Hand) -> bool:
        display_name = card.sym + card.suit.value
        card = hand.pick_card(card)
        if card is None:
            return False
        self.matrix[row][col] = display_name.center(BOARD_ELEMENT_WIDTH)

        return True

    def display(self):
        print_matrix(self.matrix)

board = Board()

deck = Deck()
hands = [Hand() for _ in range(4)]
deck.distribute_cards(hands)

my_hand = hands[0]
while True:
    print(my_hand)
    print('Enter row and col: ', end='')
    row, col = [int(val) for val in input().split()]
    card_sym = input('Enter card symbol: ')
    card_suit = input('Enter card suit: ')
    card_name = None
    for CardClass in Card.__subclasses__():
        print(f'{CardClass(CardSuit.BADAM).sym } == {card_sym}')
        if CardClass(CardSuit.BADAM).sym == card_sym:
            card_name = CardClass.__name__
            break
    else:
        print("Bruh help", card_name)

    for suit in CardSuit:
        if card_suit == str(suit).split('.')[-1][0]:
            card_suit = suit
            break

    card = eval(
        f'{card_name}({card_suit})',
    )

    print("Card is:", card)
    board.add_card(row, col, card, my_hand)
    board.display()