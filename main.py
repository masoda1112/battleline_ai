import random
import math
from scipy.stats import geom
import collections
import math
import operator
import env
import player
import calculate

# 各役の確率で勝率判断
# 期待値の計算
# プレイアルゴリズム残タスク
# ハンドを含めた勝率計算
# ドロー枚数を含めた期待値計算
# 
calculate.test_calculate_hand_list_exp()

# def cal_win_rate():


def calculate_exp_lane(lane,lane_number):
    # 空の場合とそうでない場合の条件分岐 len(lane) == 0
    # 空の場合lane_numberで分岐 0or8,1or7,else
    # 空の場合
    if len(lane) == 0:
        five_middle_rane, semi_middle_rane, wing_rane = calculate.test_calculate_hand_list_exp()
        win_rate = 0
        if lane_number == 0 or lane_number == 8:
            win_rate = cal_win_rate(lane, wing_rane)
        elif lane_number == 1 or lane_number == 7:
            win_rate = cal_win_rate(lane, semi_middle_rane)
        else:
            win_rate = cal_win_rate(lane, five_middle_rane)

    n = random.randrange(0, 3)
    return n

def decision_option(table, hand):
    # tableをコピー
    test_table = table
    exp_table = []
    n = 0
    c = 0
    while c < 7:
        # handをそれぞれ抜き、tableにつけて算出
        while n < 9:
            game_exp = calculate_exp_lane(test_table[n][1],hand, n)
            exp_table.append(game_exp)
            n+=1
        c += 1
    print(exp_table)

def test_decision_option():
    table_o = env.Table()
    table = table_o.check_table()
    deck = env.Deck()
    hand = deck.build_hands()
    decision_option(table, hand)

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




# 学習時変数
#

# 残タスク
# playerの選択評価アルゴリズムを作成
# レーンごと勝率計算
# 全体勝率判断

# 勝敗決定アルゴリズム作成
# UI作成


# 残りタスク
# レーンごとの勝率の推定
# 判断アルゴリズムの作成
# UIの作成　https://qiita.com/Bashi50/items/01c961f8f969e1b1696d