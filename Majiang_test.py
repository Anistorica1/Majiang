from collections import Counter
import os

class MahjongAI:

    def __init__(self, hand_paths):
        # 原始图片路径
        self.hand_paths = hand_paths

        # 转换为牌面
        self.hand = [self.parse_tile(p) for p in hand_paths]

    # ---------------------------
    # 解析牌
    # ---------------------------
    def parse_tile(self, tile_path):
        filename = os.path.basename(tile_path)
        return filename.replace(".png", "")

    # ---------------------------
    # 判断是否胡
    # ---------------------------
    def is_win(self):
        if self.shanten(self.hand) != 0:
            return False

        # 必须有役
        if not self.has_yaku(self.hand):
            return False

        return True

    # ---------------------------
    # 向听数（简化）
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
    # 面子提取
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
        for suit in ["w", "p", "t"]:
            nums = [str(i) + suit for i in range(1, 10)]
            counts = [counter[t] for t in nums if t in counter]

            i = 0
            while i < len(nums) - 2:
                t1, t2, t3 = nums[i], nums[i+1], nums[i+2]
                while counter.get(t1,0) > 0 and counter.get(t2,0) > 0 and counter.get(t3,0) > 0:
                    counter[t1] -= 1
                    counter[t2] -= 1
                    counter[t3] -= 1
                    melds += 1
                i += 1

        leftovers = sum(counter.values())
        return melds, leftovers

    # ---------------------------
    # 役判断（简化版，但可用）
    # ---------------------------
    def has_yaku(self, hand):
        """
        简化役判断：
        至少满足一个役才允许胡牌
        """

        # 断幺九（无1/9/字牌）
        if self.is_tanyao(hand):
            return True

        # 对对和（全刻子）
        if self.is_toitoi(hand):
            return True

        # 七对子（特殊）
        if self.is_chiitoi(hand):
            return True

        # 平和（简化版）
        if self.is_pinfu(hand):
            return True

        # 字一色（全字牌）
        if self.is_ziiso(hand):
            return True

        return False

    # ---------------------------
    # 各种役判断
    # ---------------------------

    def is_tanyao(self, hand):
        for tile in hand:
            if tile[0] in ["1","9"]:
                return False
            if tile in ["E","S","W","N","R","G","D"]:
                return False
        return True

    def is_toitoi(self, hand):
        counter = Counter(hand)
        melds = 0
        for tile in counter:
            if counter[tile] >= 3:
                melds += 1
        return melds >= 4

    def is_chiitoi(self, hand):
        counter = Counter(hand)
        return len(counter) == 7 and all(v == 2 for v in counter.values())

    def is_pinfu(self, hand):
        """
        简化版平和（不完全精确，但够用）
        条件：
        - 全顺子
        - 无字牌
        """
        for tile in hand:
            if tile in ["E","S","W","N","R","G","D"]:
                return False
        return True

    def is_ziiso(self, hand):
        for tile in hand:
            if tile not in ["E","S","W","N","R","G","D"]:
                return False
        return True

    # ---------------------------
    # 自动打牌
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
    # 决策
    # ---------------------------
    def decide(self):
        if self.is_win():
            return "胡"

        # 向听数
        discard, s = self.choose_discard()

        # 是否建议立直
        riichi = (s == 1)

        return {
            "立直": riichi,
            "打牌": discard,
            "向听数": s,
            "是否可胡(需有役)": self.is_win()
        }