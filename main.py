import random
import math
from scipy.stats import geom
import collections
import math
import operator
import env
import player
import calculate


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



# 一旦使用しない関数
# count 3.45  av 6.5
# def thousand_straight_flash_count():
#     straight_flash_count = 0
#     n = 0
#     sf_av = 0
#     while n < 1000:
#         count, av = calculate_hand_list_exp()
#         straight_flash_count += count
#         sf_av += av
#         n += 1
#     print('straight_flash_count',straight_flash_count)
#     print('straight_flash_rate',straight_flash_count / 1000)
#     print('straight_flash_max_number_av', sf_av / 1000)

# 考える必要のあるstate数を計算
# def caluculate_state_count():
#     state_count = math.comb(60,7) * 63 * 53 * 52
#     next_state_count = 36 * 8 * 10 * 20
#     test = 10 ** 9
#     # 67兆~
#     print(state_count)
#     # 57600
#     print(next_state_count)
#     # 1億
#     print(test)

# 学習時変数
#

# 50%以上はロイヤルストレートフラッシュが出る
# 10,9,8のうち2枚あったら、3枚あったらそれからおく（真ん中5個のランダムに）
# それ以下が揃ってたら、一枚だけ真ん中5個にランダムに置く

# playerの選択評価アルゴリズムを確率
# 各テーブルの勝率で考える
# 空のテーブル：1：5つの平均、2：5つを合計した役の強さごとの確率
# 空じゃないテーブル

# プレイヤーのプレイログを取得
# 評価関数：これは自分で考えなくてはいけない
# 戦術評価概念
# 引くまでの枚数の期待値
# 自分が引く確率


# 残りタスク
# レーンごとの勝率の推定
# 判断アルゴリズムの作成
# UIの作成　https://qiita.com/Bashi50/items/01c961f8f969e1b1696d