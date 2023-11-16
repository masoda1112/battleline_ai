import random
import math
from scipy.stats import geom
import collections
import math
import operator
import env

class Player:
    def __init__(self):
        self.hands = []
        self.play_log = []
        self.player_number = 0
    def get_hands(self,hands):
        self.hands = hands
    def select_card(self,table):
        # 選択のアルゴリズムを用意
        card = self.hands.pop(random.randrange(7))
        number = random.randrange(9)
        return number, card
    def get_card(self,card):
        self.hands.append(card)
    def set_player_number(self,number):
        self.player_number = number