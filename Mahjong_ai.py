from mahjong.hand_calculating.shanten import Shanten

class MahjongAI:
    TILE_MAP = {
        # 万
        **{f"{i}w": i-1 for i in range(1, 10)},
        # 筒
        **{f"{i}p": 9 + i-1 for i in range(1, 10)},
        # 条
        **{f"{i}t": 18 + i-1 for i in range(1, 10)},
        # 字牌
        "dong": 27, "nan": 28, "xi": 29, "bei": 30,
        "bai": 31, "fa": 32, "zhong": 33
    }

    INDEX_TO_TILE = {v: k for k, v in TILE_MAP.items()}

    def __init__(self, hand_tiles: list):
        """
        hand_tiles: ["1w","2w","3w","dong",...]
        """
        self.tiles = [0] * 34
        for t in hand_tiles:
            self.tiles[self.TILE_MAP[t]] += 1

        self.shanten = Shanten()
        self.cache = {}

    def _tiles_to_key(self, tiles):
        return tuple(tiles)

    def calculate_shanten(self, tiles):
        key = self._tiles_to_key(tiles)
        if key in self.cache:
            return self.cache[key]

        val = self.shanten.calculate_shanten(tiles)
        self.cache[key] = val
        return val

    def calculate_ukeire(self, tiles, current_shanten):
        ukeire = 0

        for i in range(34):
            if tiles[i] >= 4:
                continue

            tiles[i] += 1
            new_shanten = self.calculate_shanten(tiles)
            tiles[i] -= 1

            if new_shanten < current_shanten:
                ukeire += (4 - tiles[i])

        return ukeire

    def recommend_discard(self):
        best = []
        min_shanten = 8
        max_ukeire = -1

        for i in range(34):
            if self.tiles[i] == 0:
                continue

            self.tiles[i] -= 1

            shanten = self.calculate_shanten(self.tiles)
            ukeire = self.calculate_ukeire(self.tiles, shanten)

            self.tiles[i] += 1

            # 决策逻辑（核心）
            if shanten < min_shanten or (shanten == min_shanten and ukeire > max_ukeire):
                min_shanten = shanten
                max_ukeire = ukeire
                best = [i]
            elif shanten == min_shanten and ukeire == max_ukeire:
                best.append(i)

        return [self.INDEX_TO_TILE[i] for i in best], min_shanten, max_ukeire


# ================= 测试 =================
if __name__ == "__main__":
    hand = [
        "1w","2w","3w",
        "4p","5p","6p",
        "7t","8t","9t",
        "dong","dong","nan","zhong"
    ]

    ai = MahjongAI(hand)
    best_discards, shanten, ukeire = ai.recommend_discard()

    print("推荐打出:", best_discards)
    print("向听数:", shanten)
    print("进张数:", ukeire)