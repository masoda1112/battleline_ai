import random
import math
from scipy.stats import geom
import collections
import math
import operator

class Game:
    def __init__(self,player_1,player_2):
        deck = Deck()
        table = Table()
        self.deck = deck
        self.table = table
        self.player1 = player_1
        self.player2 = player_2
    def decision_number(self):
        player_1_number = random.randrange(2)
        player_2_number = 1 if player_1_number == 1 else 2
        self.player1.set_player_number(player_1_number)
        self.player2.set_player_number(player_2_number)
    def distribution(self):
        hands1 = self.deck.build_hands()
        self.player1.get_hands(hands1)
        hands2 = self.deck.build_hands()
        self.player2.get_hands(hands2)
    def playing_turn(self):
        player_1_table,player_1_card = self.player1.select_card(self.table.table)
        self.table.set_card(1,player_1_card,player_1_table)
        card_1 = self.deck.draw_card()
        self.player1.get_card(card_1)
        player_2_table,player_2_card = self.player2.select_card(self.table.table)
        self.table.set_card(2,player_2_card,player_2_table)
        card_2 = self.deck.draw_card()
        self.player2.get_card(card_2)
class Deck:
    def __init__(self):
        cards = []
        n = 0
        color_n = 0
        number_n = 1
        while n < 60:
            color = ''
            if color_n == 0:
                color = 'RED'
            elif color_n == 1:
                color = 'ORANGE'
            elif color_n == 2:
                color = 'YELLOW'
            elif color_n == 3:
                color = 'BLUE'
            elif color_n == 4:
                color = 'PURPLE'
            elif color_n == 5:
                color = 'GREEN'
            cards.append({'color': color, 'number': number_n})
            if number_n == 10:
                color_n = color_n + 1 if color_n < 6 else 0
                number_n = 0
            n += 1
            number_n += 1
        self.deck = cards
    def build_hands(self):
        n = 0
        hands = []
        while n < 7:
            card = self.deck.pop(random.randrange(len(self.deck)))
            hands.append(card)
            n += 1
        return hands
    def draw_card(self):
        card = self.deck.pop(random.randrange(len(self.deck)))
        return card
class Table:
    def __init__(self):
        # 9*3*2のテーブルを再現
        self.table = [[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
    def set_card(self,player_number,card,table_number):
        self.table[table_number][player_number - 1].append(card)
    def check_table(self):
        return self.table