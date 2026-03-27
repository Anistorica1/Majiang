from collections import Counter
import os
import random

class MahjongAI:

    def __init__(self, hand_paths):
        self.hand_paths = hand_paths
        self.hand = [self.parse_tile(p) for p in hand_paths]

    def parse_tile(self, tile_path):
        filename = os.path.basename(tile_path)
        return filename.replace(".png", "")

    # ==============================
    # 全牌集合
    # ==============================
    def all_tiles(self):
        tiles = []
        for suit in ['w','p','t']:
            for i in range(1,10):
                tiles += [f"{i}{suit}"] * 4
        tiles += ['E','S','W','N','R','G','D'] * 4
        return tiles

    # ==============================
    # 向听数（DFS完整版）
    # ==============================
    def shanten(self, hand):
        counter = Counter(hand)
        self.min_shanten = 8

        def dfs(counter, melds, pairs, taatsu):
            tiles_left = sum(counter.values())

            # 上限剪枝
            current = 8 - melds * 2 - taatsu - pairs
            self.min_shanten = min(self.min_shanten, current)

            if tiles_left == 0:
                return

            tile = min([t for t in counter if counter[t] > 0])

            # 刻子
            if counter[tile] >= 3:
                counter[tile] -= 3
                dfs(counter, melds + 1, pairs, taatsu)
                counter[tile] += 3

            # 顺子
            if tile[0].isdigit():
                num = int(tile[0])
                suit = tile[1]
                t2 = str(num + 1) + suit
                t3 = str(num + 2) + suit
                if counter.get(t2, 0) > 0 and counter.get(t3, 0) > 0:
                    counter[tile] -= 1
                    counter[t2] -= 1
                    counter[t3] -= 1
                    dfs(counter, melds + 1, pairs, taatsu)
                    counter[tile] += 1
                    counter[t2] += 1
                    counter[t3] += 1

            # 对子
            if counter[tile] >= 2:
                counter[tile] -= 2
                dfs(counter, melds, pairs + 1, taatsu)
                counter[tile] += 2

            # 搭子
            if tile[0].isdigit():
                num = int(tile[0])
                suit = tile[1]

                # 连搭
                t2 = str(num + 1) + suit
                if counter.get(t2, 0) > 0:
                    counter[tile] -= 1
                    counter[t2] -= 1
                    dfs(counter, melds, pairs, taatsu + 1)
                    counter[tile] += 1
                    counter[t2] += 1

                # 跳搭
                t3 = str(num + 2) + suit
                if counter.get(t3, 0) > 0:
                    counter[tile] -= 1
                    counter[t3] -= 1
                    dfs(counter, melds, pairs, taatsu + 1)
                    counter[tile] += 1
                    counter[t3] += 1

            # 单张
            counter[tile] -= 1
            dfs(counter, melds, pairs, taatsu)
            counter[tile] += 1

        dfs(counter, 0, 0, 0)
        return max(self.min_shanten, 0)

    # ==============================
    # 进张数（真实剩余牌）
    # ==============================
    def ukeire(self, hand):
        base = self.shanten(hand)
        full = Counter(self.all_tiles())
        current = Counter(hand)

        remain = full - current

        total = 0
        for t in remain:
            new_hand = hand + [t]
            if self.shanten(new_hand) < base:
                total += remain[t]

        return total

    # ==============================
    # Monte Carlo（核心强化）
    # ==============================
    def monte_carlo_score(self, hand, simulations=50):
        tiles = self.all_tiles()
        current = Counter(hand)
        remain = list((Counter(tiles) - current).elements())

        score = 0

        for _ in range(simulations):
            sim_hand = hand.copy()
            random.shuffle(remain)

            for draw in remain[:10]:  # 模拟摸10张
                sim_hand.append(draw)
                if self.shanten(sim_hand) == 0:
                    score += 1
                    break
                sim_hand.pop()

        return score

    # ==============================
    # 是否胡
    # ==============================
    def is_win(self):
        return self.shanten(self.hand) == 0

    # ==============================
    # 决策（终极版）
    # ==============================
    def choose_discard(self):
        best_tile = None
        best_tuple = (-999, -999, -999)

        for tile in set(self.hand):
            new_hand = self.hand.copy()
            new_hand.remove(tile)

            s = self.shanten(new_hand)
            u = self.ukeire(new_hand)
            m = self.monte_carlo_score(new_hand, simulations=30)

            # 综合评分
            score = (-s, u, m)

            if score > best_tuple:
                best_tuple = score
                best_tile = tile

        return best_tile, best_tuple

    # ==============================
    # 决策输出
    # ==============================
    def decide(self):
        if self.is_win():
            return "胡"

        discard, score = self.choose_discard()

        return {
            "打牌": discard,
            "评分": score,
            "向听数": -score[0],
            "进张数": score[1],
            "胡率估计": score[2]
        }
