from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

class RiichiAI:
    def __init__(self, hand_tiles, dora_indicators=None, turn=1):
        """
        hand_tiles: ["1w", ...]
        dora_indicators: ["3w"]  宝牌指示牌（可选）
        turn: 当前巡目（1~18）
        """
        self.hand_tiles = hand_tiles
        self.shanten = Shanten()
        self.turn = turn
        self.dora_tiles = self._calc_dora(dora_indicators or [])

    # ----------------------------
    # 🔄 转换
    # ----------------------------
    def _convert_to_34(self, tiles):
        mapping = {
            "dong": 27, "nan": 28, "xi": 29, "bei": 30,
            "zhong": 31, "fa": 32, "bai": 33
        }

        tiles_34 = [0] * 34

        for t in tiles:
            if t.endswith("w"):
                tiles_34[int(t[0]) - 1] += 1
            elif t.endswith("p"):
                tiles_34[9 + int(t[0]) - 1] += 1
            elif t.endswith("t"):
                tiles_34[18 + int(t[0]) - 1] += 1
            else:
                tiles_34[mapping[t]] += 1

        return tiles_34

    # ----------------------------
    # 🎯 宝牌计算
    # ----------------------------
    def _calc_dora(self, indicators):
        result = set()

        for t in indicators:
            if t.endswith("w"):
                n = int(t[0])
                result.add(f"{(n % 9) + 1}w")
            elif t.endswith("p"):
                n = int(t[0])
                result.add(f"{(n % 9) + 1}p")
            elif t.endswith("t"):
                n = int(t[0])
                result.add(f"{(n % 9) + 1}t")
            else:
                order = ["dong","nan","xi","bei","zhong","fa","bai"]
                idx = order.index(t)
                result.add(order[(idx+1)%7])

        return result

    # ----------------------------
    # 🎯 进张
    # ----------------------------
    def _ukeire(self, tiles):
        base = self.shanten.calculate_shanten(tiles)
        total = 0

        for i in range(34):
            if tiles[i] >= 4:
                continue
            tiles[i] += 1
            if self.shanten.calculate_shanten(tiles) < base:
                total += (4 - tiles[i])
            tiles[i] -= 1

        return total

    # ----------------------------
    # 🧠 听牌质量
    # ----------------------------
    def _wait_quality(self, tiles):
        score = 0
        for i in range(27):
            if tiles[i] > 0:
                if i % 9 <= 6:
                    if tiles[i+1] and tiles[i+2]:
                        score += 3  # 两面
                if i % 9 == 0 or i % 9 == 8:
                    score -= 1  # 边张
        return score

    # ----------------------------
    # 🔥 七对子
    # ----------------------------
    def _chiitoi(self, tiles):
        return sum(1 for x in tiles if x >= 2) * 2

    # ----------------------------
    # 🔥 断幺九
    # ----------------------------
    def _tanyao(self, tiles):
        score = 0
        for i in range(34):
            if tiles[i] > 0:
                if i >= 27 or i % 9 in (0, 8):
                    score -= 2
                else:
                    score += 1
        return score

    # ----------------------------
    # 🔥 清一色
    # ----------------------------
    def _flush(self, tiles):
        suits = [
            sum(tiles[0:9]),
            sum(tiles[9:18]),
            sum(tiles[18:27])
        ]
        return max(suits) * 2

    # ----------------------------
    # 🔥 宝牌权重
    # ----------------------------
    def _dora_score(self, tiles):
        score = 0
        for t in self.hand_tiles:
            if t in self.dora_tiles:
                score += 3
        return score

    # ----------------------------
    # 🏆 主函数
    # ----------------------------
    def recommend_discard(self):
        base = self._convert_to_34(self.hand_tiles)

        best_tile = None
        best_score = None

        for tile in set(self.hand_tiles):
            tiles = base.copy()

            idx = self._convert_to_34([tile]).index(1)
            tiles[idx] -= 1

            shanten = self.shanten.calculate_shanten(tiles)
            ukeire = self._ukeire(tiles)

            # 动态权重（巡目）
            speed_weight = 1.5 if self.turn > 10 else 1.0

            score = (
                shanten,
                -ukeire * speed_weight,
                -self._wait_quality(tiles),
                -self._chiitoi(tiles) * 0.5,
                -self._tanyao(tiles) * 0.3,
                -self._flush(tiles) * 0.2,
                -self._dora_score(tiles)
            )

            if best_score is None or score < best_score:
                best_score = score
                best_tile = tile

        return best_tile