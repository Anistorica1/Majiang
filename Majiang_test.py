from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

class RiichiAI:
    def __init__(self, hand_tiles):
        self.hand_tiles = hand_tiles
        self.shanten = Shanten()

    # ----------------------------
    # 🔄 转换
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
    # 🎯 进张
    # ----------------------------
    def _calculate_ukeire(self, tiles_34):
        base = self.shanten.calculate_shanten(tiles_34)
        ukeire = 0

        for i in range(34):
            if tiles_34[i] >= 4:
                continue

            tiles_34[i] += 1
            if self.shanten.calculate_shanten(tiles_34) < base:
                ukeire += (4 - tiles_34[i])
            tiles_34[i] -= 1

        return ukeire

    # ----------------------------
    # 🧠 牌型评分
    # ----------------------------
    def _shape_score(self, tiles_34):
        score = 0
        for i in range(34):
            if tiles_34[i] > 0:
                if i < 27:
                    if i % 9 <= 6:
                        score += min(tiles_34[i], tiles_34[i+1])
                        score += min(tiles_34[i], tiles_34[i+2])
                if tiles_34[i] >= 2:
                    score += 1
        return score

    # ----------------------------
    # 🔥 七对子倾向
    # ----------------------------
    def _chiitoi_score(self, tiles_34):
        pairs = sum(1 for x in tiles_34 if x >= 2)
        return pairs * 2

    # ----------------------------
    # 🔥 断幺九倾向
    # ----------------------------
    def _tanyao_score(self, tiles_34):
        score = 0
        for i in range(34):
            if tiles_34[i] > 0:
                # 字牌 or 1/9
                if i >= 27 or i % 9 == 0 or i % 9 == 8:
                    score -= 2
                else:
                    score += 1
        return score

    # ----------------------------
    # 🔥 清一色倾向
    # ----------------------------
    def _flush_score(self, tiles_34):
        man = sum(tiles_34[0:9])
        pin = sum(tiles_34[9:18])
        sou = sum(tiles_34[18:27])

        max_suit = max(man, pin, sou)

        # 偏向最多的花色
        return max_suit * 2

    # ----------------------------
    # 🏆 主函数
    # ----------------------------
    def recommend_discard(self):
        best_tile = None
        best_score = None

        base_34 = self._convert_to_34(self.hand_tiles)

        for tile in set(self.hand_tiles):
            tiles_copy = base_34.copy()

            tile_34 = self._convert_to_34([tile])
            idx = tile_34.index(1)

            tiles_copy[idx] -= 1

            shanten = self.shanten.calculate_shanten(tiles_copy)
            ukeire = self._calculate_ukeire(tiles_copy)
            shape = self._shape_score(tiles_copy)

            # 新增策略
            chiitoi = self._chiitoi_score(tiles_copy)
            tanyao = self._tanyao_score(tiles_copy)
            flush = self._flush_score(tiles_copy)

            # 🔥 综合评分（关键！）
            score = (
                shanten,               # 最重要
                -ukeire,               # 越多越好
                -shape,                # 好形
                -chiitoi * 0.5,        # 七对子
                -tanyao * 0.3,         # 断幺九
                -flush * 0.2           # 清一色
            )

            if best_score is None or score < best_score:
                best_score = score
                best_tile = tile

        return best_tile