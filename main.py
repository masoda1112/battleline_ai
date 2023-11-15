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

# outs計算アルゴリズム
# outsを最後までに獲得できる期待値
def get_exp(card_count, outs):
    exp = 1 - (((card_count + 7) - outs) / (card_count + 7))**(card_count / 2)
    return exp

# アウツを一枚引くまでの期待値
def calculate_draw_exp(outs_n,card_count):
    n = 0
    sum = 0
    while n < card_count:
        sum += outs_n / (card_count - n)
        if sum > 0.5:
            break
        n += 2
    return n

# 役完成に2枚必要（先に1枚目が出る確率を全パターン計算する）
# アウツが被っていないパターン
def two_calculate_draw_exp(outs_1,outs_2,card_count):
    # まず２枚のうちどちらかを引くまでの回数の期待値
    sum_n = calculate_draw_exp(outs_1 + outs_2, card_count)
    # 残った一枚を引くまでの回数の期待値を加重平均、別のoutsを引く確率を加重平均
    sum_1_av = calculate_draw_exp(outs_1, card_count - sum_n) * (outs_2 / (outs_1 + outs_2))
    sum_2_av = calculate_draw_exp(outs_2, card_count - sum_n) * (outs_1 / (outs_1 + outs_2))
    return int(sum_n + sum_1_av + sum_2_av)

# アウツが被っているパターン
def dup_two_calculate_draw_exp(outs_n, card_count):
    # 一枚めを引くまでの回数の期待値
    first_n = calculate_draw_exp(outs_n, card_count)
    # 2枚目を引くまでの回数の期待値
    # 結局1枚目の回数の期待値*2になる？
    second_n = calculate_draw_exp(outs_n - 1, card_count - first_n)
    return first_n + second_n

# テストプレイ
def playing_game():
    player_1 = Player()
    player_2 = Player()
    game = Game(player_1,player_2)
    game.distribution()
    turn_count = 0
    while turn_count < 10:
        game.playing_turn()
        turn_count += 1
    # print('player_1',player_1.hands)
    # print('player_2',player_2.hands)

# outs計算アルゴリズムテスト
def test_outs_prob_calculate():
    card_count = 46
    outs = 2
    exp_draw_count = calculate_draw_exp(outs,card_count)
    exp_draw_count_2 = two_calculate_draw_exp(outs,outs,card_count)
    dup_exp_draw_count_2 = dup_two_calculate_draw_exp(2,card_count)
    print('draw',exp_draw_count)
    print('two_draw',exp_draw_count_2)
    print('dup_two_draw',dup_exp_draw_count_2)
    print('Get_exp', get_exp(card_count, outs))

# 役：ストレートフラッシュ、スリーカード、フラッシュ、ストレート、ブタ
# スコアの評価方法：役→数
def scoring_hand_number(cards):
    colors = []
    numbers = []
    number = 0
    hand = 0
    for i in cards:
        color = i['color']
        number = i['number']
        colors.append(color)
        numbers.append(number)
    
    numbers = sorted(numbers)
    three = 1 if numbers.count(numbers[0]) == 3 else 0
    flash = 1 if colors.count(colors[0]) == 3 else 0
    straight = 1 if numbers[1] == numbers[0] + 1 and numbers[2] == numbers[0] + 2 else 0
 
    if three == 1:
        hand = 4
    elif flash and straight:
        hand = 5
    elif flash:
        hand = 3
    elif straight:
        hand = 2
    else:
        hand = 0
    return {'hand': hand, 'total': sum(numbers)}

# ハンドの強さ判定スコア
def test_hand_scoring():
    score = scoring_hand_number([{'color': 'RED', 'number': 1},{'color': 'RED', 'number': 2},{'color': 'RED', 'number': 3}])
    print(score)

# 27枚引いてストレートフラッシュをカウント
def test_max_hand():
    hand = []
    deck = Deck()
    first_hand = deck.build_hands()
    hand = first_hand
    n = 1
    while n < 27:
        card = deck.draw_card()
        hand.append(card)
        n += 1

    hand = sorted(hand, key=operator.itemgetter('color', 'number'))
    arr_straight_flashs = []
    arr_three_card = []
    arr_pre_straight_flashs = []
    straight_flash = []
    pre_card = {}
    card_count = 0
    for card in hand:
        if card_count != 0:
            if card['color'] == pre_card['color'] and card['number'] == pre_card['number'] + 1:
                straight_flash.append(card)
            else:
                straight_flash = []
                straight_flash.append(card)
        if len(straight_flash) == 3:
            arr_straight_flashs.append(straight_flash)
            straight_flash = []

        pre_card = card
        card_count += 1

    return len(arr_straight_flashs)

# 4.38くらい
def thousand_straight_flash_count():
    straight_flash_count = 0
    n = 0
    while n < 1000:
        straight_flash = test_max_hand()
        straight_flash_count += straight_flash
        n += 1
    print('straight_flash_count',straight_flash_count)
    print('straight_flash_rate',straight_flash_count / 1000)


# 手番やレーンのからに関係なく選ぶ関数
# 63個ある選択肢を全て選ぶ
# 空のレーンにも期待値あり

# 期待値の計算
def calculate_exp_lane(lane):
    n = random.randrange(0, 3)
    return n

def decision_option(table, hand):
    # tableをコピー
    test_table = table
    exp_table = []
    n = 0
    while n < 9:
        second_player_exp = calculate_exp_lane(test_table[n][0])
        first_player_exp = calculate_exp_lane(test_table[n][1])
        exp_table.append(second_player_exp - first_player_exp)
        n+=1
    print(exp_table)

def test_decision_option():
    table_o = Table()
    table = table_o.check_table()
    deck = Deck()
    hand = deck.build_hands()
    decision_option(table, hand)

test_decision_option()

# 自分だけ空のレーンがあるか
def select_card_table(table, hand):
    competitor_lane = []
    lane_num = 0
    while lane_num < 9:
        if len(table[lane_num][0]) != 0:
            if(len(table[lane_num][1] == 0)):
                competitor_lane.append(lane_num)
        lane_num += 1
    if len(competitor_lane) == 0:
        first_decision(table,hand)
    else:
        second_decision(table,hand,competitor_lane)

#自分だけからのレーンがあった場合 、ロイヤルストレートフラッシュ、ストレートフラッシュ、なし
def first_decision(table,hand):
    # handを色で分類、数字順にソート
    # 同じ色で連番になっていればroyalstraightflashに格納
    # straight_flash = []
    # royal_straight_flash = []
    # decision = {}
    # if len(royal_straight_flash) != 0:
    #     decision = {}
    # elif len(straight_flash) != 0:
    #     decision =  {}
    # else:
    #     decision = {}
    print('first_decision')

def second_decision(table,hand,competitor_lane):
    print('second_decision')


# 考える必要のあるstate数を計算
def caluculate_state_count():
    state_count = math.comb(60,7) * 63 * 53 * 52
    next_state_count = 36 * 8 * 10 * 20
    test = 10 ** 9
    # 67兆~
    print(state_count)
    # 57600
    print(next_state_count)
    # 1億
    print(test)
# select_card_table()

caluculate_state_count()
# 学習時変数
#

# 50%以上はロイヤルストレートフラッシュが出る
# 10,9,8のうち2枚あったら、3枚あったらそれからおく（真ん中5個のランダムに）
# それ以下が揃ってたら、一枚だけ真ん中5個にランダムに置く
# 

# playerの選択評価アルゴリズムを確率
# 場合わけして考える
# 先攻初手（強い組み合わせがある場合、ない場合）
# 既に相手のカードあり
# 既に空のレーンなし
# 既に相手の空のレーンなし

# 初手のハンドの確率を推定？（ストレートフラッシュの確率？）
# 自分のテーブルだけ考える
# 中央５つ、端から二番目、端でスコアを変える
# 空のレーンを優先する

# プレイヤーのプレイログを取得
# 評価関数：これは自分で考えなくてはいけない
# 戦術評価概念
# 引くまでの枚数の期待値
# 自分が引く確率


# 残りタスク
# レーンごとの勝率の推定
# 判断アルゴリズムの作成
# UIの作成　https://qiita.com/Bashi50/items/01c961f8f969e1b1696d