from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from collections import Counter

class RiichiAI:
    def __init__(self, hand_tiles):
        """
        hand_tiles: list[str]
        例如：
        ["1w","2w","3w","4w","5w","6w","7p","8p","9p","1t","2t","3t","dong","dong"]
        """
        self.hand_tiles = hand_tiles
        self.shanten = Shanten()

    # ----------------------------
    # 🔄 字符 → 34数组
    # ----------------------------
    def _convert_to_34(self, tiles):
        mapping = {
            "dong": "1z", "nan": "2z", "xi": "3z", "bei": "4z",
            "zhong": "5z", "fa": "6z", "bai": "7z"
        }

        man = ""
        pin = ""
        sou = ""
        honors = ""

        for t in tiles:
            if t.endswith("w"):
                man += t[0]
            elif t.endswith("p"):
                pin += t[0]
            elif t.endswith("t"):
                sou += t[0]
            else:
                honors += mapping[t][0]

        return TilesConverter.string_to_34_array(
            man=man, pin=pin, sou=sou, honors=honors
        )

    # ----------------------------
    # 🎯 计算进张数（ukeire）
    # ----------------------------
    def _calculate_ukeire(self, tiles_34):
        base_shanten = self.shanten.calculate_shanten(tiles_34)
        ukeire = 0

        for i in range(34):
            if tiles_34[i] >= 4:
                continue

            tiles_34[i] += 1
            new_shanten = self.shanten.calculate_shanten(tiles_34)
            tiles_34[i] -= 1

            if new_shanten < base_shanten:
                # 剩余张数（4 - 已有）
                ukeire += (4 - tiles_34[i])

        return ukeire

    # ----------------------------
    # 🧠 牌型评分（简单版）
    # ----------------------------
    def _shape_score(self, tiles_34):
        score = 0

        for i in range(34):
            if tiles_34[i] > 0:
                # 顺子潜力
                if i < 27:  # 数牌
                    if i % 9 <= 6:
                        score += min(tiles_34[i], tiles_34[i+1])
                        score += min(tiles_34[i], tiles_34[i+2])

                # 对子
                if tiles_34[i] >= 2:
                    score += 1

        return score

    # ----------------------------
    # 🏆 主函数：推荐打牌
    # ----------------------------
    def recommend_discard(self):
        best_tile = None
        best_tuple = None

        original_34 = self._convert_to_34(self.hand_tiles)

        for idx, tile in enumerate(self.hand_tiles):
            tiles_copy = original_34.copy()

            tile_34 = self._convert_to_34([tile])
            tile_index = tile_34.index(1)

            tiles_copy[tile_index] -= 1

            shanten = self.shanten.calculate_shanten(tiles_copy)
            ukeire = self._calculate_ukeire(tiles_copy)
            shape = self._shape_score(tiles_copy)

            score = (shanten, -ukeire, -shape)

            if best_tuple is None or score < best_tuple:
                best_tuple = score
                best_tile = tile

        return best_tile