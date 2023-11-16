import random
import math
from scipy.stats import geom
import collections
import math
import operator
import env
import player
import calculate

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
    player_1 = player.Player()
    player_2 = player.Player()
    game = env.Game(player_1,player_2)
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


# ハンドのスコア計算
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



# 空のレーンの期待値を計算
# 27枚引いてストレートフラッシュをカウント
def hand_27_build():
    hand = []
    deck = env.Deck()
    first_hand = deck.build_hands()
    hand = first_hand
    n = 1
    while n < 24:
        card = deck.draw_card()
        hand.append(card)
        n += 1
    return hand

def straight_flash_count_exp(hand):
    hand = sorted(hand, key=operator.itemgetter('color', 'number'))
    arr_straight_flashs = []
    straight_flash = []
    pre_card = {}
    used_cards = []
    card_count = 0
    for card in hand[:]:
        if card_count != 0:
            if card['color'] == pre_card['color'] and card['number'] == pre_card['number'] + 1:
                straight_flash.append(card)
            else:
                straight_flash = []
                straight_flash.append(card)
        if len(straight_flash) == 3:
            arr_straight_flashs.append(straight_flash)
            straight_flash = []
            used_cards.extend([card_count - 2, card_count - 1, card_count])
        pre_card = card
        card_count += 1
    n = 0
    straight_flash_count = len(arr_straight_flashs)
    straight_flash_max_list = []
    while n < straight_flash_count:
        # 各sfの最大値を取得
        sf_max_number = arr_straight_flashs[n][2]['number']
        straight_flash_max_list.append(sf_max_number)
        n+=1
    # straight_flash_count = len(straight_flash_max_list)
    # straight_flash_av = sum(straight_flash_max_list) / straight_flash_count if straight_flash_count != 0 else 0
    # 使用したカードを取り除く
    for i in sorted(used_cards, reverse=True):
        hand.pop(i)
    return sorted(straight_flash_max_list, reverse=True), hand

def three_card_count_exp(hand):
    hand = sorted(hand, key=lambda x: x['number'])
    pre_card_number = 0
    pre_three_card = []
    three_card = []
    three_card_number_list = []
    used_cards = []
    card_count = 0
    for card in hand:
        if pre_card_number == card['number']:
            pre_three_card.append(card)
        else:
            pre_three_card = []
            pre_three_card.append(card)
        pre_card_number = card['number']

        if len(pre_three_card) == 3:
            three_card.append(pre_three_card)
            pre_card_number = 0
            used_cards.extend([card_count - 2, card_count - 1, card_count])
        card_count += 1
    three_card_count = len(three_card)
    n = 0
    while n < three_card_count:
        three_card_number_list.append(three_card[n][2]['number'])
        n+=1
    # three_card_av = sum(three_card_number_list) / three_card_count if three_card_count != 0 else 0

    for i in sorted(used_cards, reverse=True):
        hand.pop(i)
    return sorted(three_card_number_list, reverse=True), hand

def flash_count_exp(hand):
    hand = sorted(hand, key=lambda x: x['number'],reverse=True)
    hand = sorted(hand, key=lambda x: x['color'])
    pre_card = None
    card_count = 0
    pre_flash = []
    flash = []
    used_cards = []
    while card_count < len(hand):
        card = hand[card_count]
        if pre_card != None:
            if card['color'] != pre_card['color']:
                pre_flash = []
            pre_flash.append(card)
        pre_card = card
        if len(pre_flash) == 3:
            flash.append(pre_flash)
            used_cards.extend([card_count - 2, card_count - 1, card_count])
            pre_flash = []
            pre_card = None
        card_count += 1
    sum_flash = []
    for comb in flash:
        sum = 0
        for card in comb:
            sum += card['number']
        sum_flash.append(sum / 3)
    sum_flash = sorted(sum_flash,reverse=True)

    for i in sorted(used_cards, reverse=True):
        hand.pop(i)
    return sorted(sum_flash, reverse=True), hand
def straight_count_exp(hand):
    hand = sorted(hand, key=lambda x: x['number'],reverse=True)
    straights = []
    numbers = [0,0,0,0,0,0,0,0,0,0]
    card_count = 0
    while card_count < len(hand):
        card_number = hand[card_count]['number']
        if card_number == 10:
            numbers[0] += 1
        elif card_number == 9:
            numbers[1] += 1
        elif card_number == 8:
            numbers[2] += 1
        elif card_number == 7:
            numbers[3] += 1
        elif card_number == 6:
            numbers[4] += 1
        elif card_number == 5:
            numbers[5] += 1
        elif card_number == 4:
            numbers[6] += 1
        elif card_number == 3:
            numbers[7] += 1
        elif card_number == 2:
            numbers[8] += 1
        elif card_number == 1:
            numbers[9] += 1
        card_count += 1

    n = 0
    while n < 8:
        straight = 10 - n
        if numbers[n] == numbers[n + 1] == numbers[n + 2] == 2:
            straights.extend([straight,straight])
            numbers[n] -= 2
            numbers[n + 1] -= 2
            numbers[n + 2] -= 2
        elif numbers[n] > 0 and numbers[n + 1] > 0 and numbers[n + 2] > 0:
            straights.append(straight)
            numbers[n] -= 1
            numbers[n + 1] -= 1
            numbers[n + 2] -= 1
        n += 1
    buta = buta_count_exp(numbers)
    return sorted(straights, reverse=True), buta
def buta_count_exp(numbers):
    butas = []
    buta = []
    count = 0
    for i in numbers:
        if i != 0:
            n = 0
            while n < i:
                buta.append(10 - count)
                n += 1
                if len(buta) == 3:
                    butas.append(sum(buta) / len(buta))
                    buta = []
        count += 1
    return sorted(butas, reverse=True)

def calculate_hand_list_exp():
   hand = hand_27_build()
   hand_rank = []
   sf_list, hand =  straight_flash_count_exp(hand)
   three_card_list, hand = three_card_count_exp(hand)
   flash_list, hand = flash_count_exp(hand)
   straight_list, buta = straight_count_exp(hand)
   pre_hand_rank = [sf_list, three_card_list,flash_list,straight_list,buta]
   hand_rank = []
   hand_count = 0
   n = 0
   while n < 5:
       hand = pre_hand_rank[n]
       hand_count = len(hand)
       num = 0
       while num < hand_count:
           hand_rank.append({'hand': 5 - n, 'score': hand[num]})
           num+=1
       n+=1
   return hand_rank

def build_hand_ranks_exp():
    hand_ranks = []
    prob_hand_ranks = []
    num = 0
    while num < 10:
        hand_ranks.append([])
        
        num_2 = 0
        while num_2 < 5:
            hand_ranks[num].append([])
            num_3 = 0
            while num_3 < 10:
                hand_ranks[num][num_2].append(0)
                num_3 += 1
            num_2 += 1
        num += 1

    c = 0
    n = 1000
    while c < n:
        hand_rank = calculate_hand_list_exp()
        count = 0
        while count < 10:
            hand_index = 5 - hand_rank[count]['hand']
            score_index = 10 - round(hand_rank[count]['score'])
            hand_ranks[count][hand_index][score_index] += 1
            count += 1
        c += 1
    return hand_ranks

def build_rane_rank(hand_ranks, start, end):
    arr = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    n = start
    while n < end:
        hand_rank = hand_ranks[n]
        c = 0
        while c < 5 :
            i = 0
            while i < 10:
                arr[c][i] += hand_rank[c][i]
                i += 1
            c += 1
        n+=1 
    i = 0
    while i < 5:
        t = 0
        while t < 10:
            arr[i][t] /= (end - start) * 1000
            t += 1
        i += 1
    return arr

# レーンの役ごとの確率
def test_calculate_hand_list_exp():
    # 50パターンのどれかをカウントしたい×10=500
    # 順位→役→スコア
    # 10,5,10
    hand_ranks = build_hand_ranks_exp()
    semi_middle_rane = []
    wing_rane = []
    n = 0
    five_middle_rane = build_rane_rank(hand_ranks, 0, 5)
    semi_middle_rane = build_rane_rank(hand_ranks, 6, 7)
    wing_rane = build_rane_rank(hand_ranks, 8, 9)
    print('five_middle_rane',five_middle_rane)
    print('semi_middle_rane',semi_middle_rane)
    print('wing_rane',wing_rane)
    return five_middle_rane, semi_middle_rane, wing_rane

# レーンごとの期待値
def cal_rane_rank_exp(arr):
    sum_prob = 0
    hand = 6
    number = 11
    for i in arr:
        number = 11
        hand -= 1
        for e in i:
            sum_prob += e
            number -= 1
            if sum_prob > 0.5:
                break
        else:
            continue
        break
    return {'hand': hand, 'number': number}

def get_rane_rank_exp():
    five_middle_rane, semi_middle_rane, wing_rane = test_calculate_hand_list_exp()
    five_middle_exp = cal_rane_rank_exp(five_middle_rane)
    semi_middle_exp = cal_rane_rank_exp(semi_middle_rane)
    wing_exp = cal_rane_rank_exp(wing_rane)

    print(five_middle_exp)
    print(semi_middle_exp)
    print(wing_exp)
    return five_middle_exp, semi_middle_exp, wing_exp