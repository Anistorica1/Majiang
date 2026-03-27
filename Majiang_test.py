from collections import Counter
import os
import copy

class MahjongAI:

    def __init__(self, hand_paths):
        self.hand_paths = hand_paths
        self.hand = [self.parse_tile(p) for p in hand_paths]

    def parse_tile(self, tile_path):
        filename = os.path.basename(tile_path)
        return filename.replace(".png", "")

    # ==============================
    # 向听数（递归改进版）
    # ==============================
    def shanten(self, hand):
        tiles = sorted(hand)
        counter = Counter(tiles)

        self.min_shanten = 8

        def dfs(counter, melds, pairs, taatsu):
            tiles_left = sum(counter.values())

            # 剪枝
            current = 8 - melds * 2 - taatsu - pairs
            if current < self.min_shanten:
                self.min_shanten = current

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

            # 搭子（两连）
            if tile[0].isdigit():
                num = int(tile[0])
                suit = tile[1]
                t2 = str(num + 1) + suit
                if counter.get(t2, 0) > 0:
                    counter[tile] -= 1
                    counter[t2] -= 1
                    dfs(counter, melds, pairs, taatsu + 1)
                    counter[tile] += 1
                    counter[t2] += 1

            # 单张
            counter[tile] -= 1
            dfs(counter, melds, pairs, taatsu)
            counter[tile] += 1

        dfs(counter, 0, 0, 0)
        return max(self.min_shanten, 0)

    # ==============================
    # 进张数（核心提升）
    # ==============================
    def ukeire(self, hand):
        base = self.shanten(hand)
        tiles = self.all_tiles()
        count = 0

        for t in tiles:
            new_hand = hand + [t]
            if self.shanten(new_hand) < base:
                count += 1

        return count

    def all_tiles(self):
        tiles = []
        for suit in ['w','p','t']:
            for i in range(1,10):
                tiles.append(f"{i}{suit}")
        tiles += ['E','S','W','N','R','G','D']
        return tiles

    # ==============================
    # 是否胡（简化：允许立直）
    # ==============================
    def is_win(self):
        return self.shanten(self.hand) == 0

    # ==============================
    # 打牌决策（进张优先）
    # ==============================
    def choose_discard(self):
        best_tile = None
        best_score = -1
        best_shanten = 99

        for tile in self.hand:
            new_hand = self.hand.copy()
            new_hand.remove(tile)

            s = self.shanten(new_hand)
            u = self.ukeire(new_hand)

            # 优先：向听数，其次：进张数
            score = (-s, u)

            if score > ( -best_shanten, best_score ):
                best_shanten = s
                best_score = u
                best_tile = tile

        return best_tile, best_shanten, best_score

    # ==============================
    # 决策
    # ==============================
    def decide(self):
        if self.is_win():
            return "胡"

        discard, s, u = self.choose_discard()

        return {
            "打牌": discard,
            "向听数": s,
            "进张数": u,
            "是否听牌": s == 0
        }