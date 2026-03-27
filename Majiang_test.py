from collections import Counter

class MahjongAI:
    def __init__(self, hand):
        self.hand = hand  # 13 or 14 tiles

    # ---------------------------
    # 判断是否胡
    # ---------------------------
    def is_win(self):
        return self.shanten(self.hand) == 0

    # ---------------------------
    # 向听数计算（简化）
    # ---------------------------
    def shanten(self, hand):
        hand = sorted(hand)
        tile_count = Counter(hand)

        min_shanten = 8

        unique_tiles = set(hand)

        for pair_tile in unique_tiles:
            if tile_count[pair_tile] >= 2:
                temp = tile_count.copy()
                temp[pair_tile] -= 2

                melds, leftovers = self.remove_melds(temp)
                shanten_value = 4 - melds

                if leftovers > 0:
                    shanten_value += leftovers // 3

                if shanten_value < min_shanten:
                    min_shanten = shanten_value

        return min_shanten

    # ---------------------------
    # 提取面子
    # ---------------------------
    def remove_melds(self, tile_counter):
        counter = tile_counter.copy()
        melds = 0

        # 刻子
        for tile in list(counter.keys()):
            while counter[tile] >= 3:
                counter[tile] -= 3
                melds += 1

        # 顺子
        for suit in ["m", "p", "s"]:
            nums = [str(i) + suit for i in range(1, 10)]
            counts = [counter[t] for t in nums]

            i = 0
            while i < 7:
                while counts[i] > 0 and counts[i+1] > 0 and counts[i+2] > 0:
                    counts[i] -= 1
                    counts[i+1] -= 1
                    counts[i+2] -= 1
                    melds += 1
                i += 1

            for idx, t in enumerate(nums):
                counter[t] = counts[idx]

        leftovers = sum(counter.values())
        return melds, leftovers

    # ---------------------------
    # 是否立直（简化策略）
    # ---------------------------
    def should_riichi(self):
        """
        简化策略：
        - 向听数 = 1 时建议立直
        """

        s = self.shanten(self.hand)

        if s == 1:
            return True
        return False

    # ---------------------------
    # 是否吃（默认：不吃）
    # ---------------------------
    def should_chi(self):
        return False

    # ---------------------------
    # 是否碰（默认：不碰）
    # ---------------------------
    def should_pon(self):
        return False

    # ---------------------------
    # 选择弃牌
    # ---------------------------
    def choose_discard(self):
        best_tile = None
        best_shanten = float('inf')

        for tile in self.hand:
            new_hand = self.hand.copy()
            new_hand.remove(tile)

            s = self.shanten(new_hand)

            if s < best_shanten:
                best_shanten = s
                best_tile = tile

        return best_tile, best_shanten

    # ---------------------------
    # 综合决策
    # ---------------------------
    def decide(self):
        # 1. 是否胡
        if self.is_win():
            return "胡"

        # 2. 是否立直
        if self.should_riichi():
            riichi = True
        else:
            riichi = False

        # 3. 吃碰（默认不做）
        chi = self.should_chi()
        pon = self.should_pon()

        # 4. 打牌
        discard, s = self.choose_discard()

        return {
            "立直": riichi,
            "吃": chi,
            "碰": pon,
            "打牌": discard,
            "向听数": s
        }


# ---------------------------
# 测试
# ---------------------------
if __name__ == "__main__":
    hand = [
        "1m","2m","3m",
        "4p","5p","6p",
        "7s","8s","9s",
        "E","E","R","R"
    ]

    ai = MahjongAI(hand)

    result = ai.decide()
    print(result)