"""NPC 砍价：按次数给折扣阶梯，低于底价就翻脸。"""


class Shop:
    """砍价台账。"""

    def __init__(self, base_price, floor_price, tiers, max_attempts=None):
        self.base_price = base_price
        self.floor_price = floor_price
        self.tiers = list(tiers)
        self.max_attempts = len(self.tiers) if max_attempts is None else max_attempts
        self.offers = []
        self.seen = {}
        self.price = base_price
        self.scanned = 0

    def price_for(self, attempts):
        """第 attempts 次砍价后的报价：第 1 次用 tiers[0]，超出阶梯长度固定最后一档。"""
        index = min(attempts - 1, len(self.tiers) - 1)
        if index < 0:
            index = 0
        return self.base_price * (100 - self.tiers[index]) // 100

    def haggle(self, req_id, times):
        """砍价请求：返回 (报价, 是否成交)。同一 req_id 只生效一次，O(1) 查询。"""
        self.scanned += 1
        if req_id in self.seen:
            return self.seen[req_id]

        if times < 1 or times > self.max_attempts:
            result = (self.price, False)
            self.seen[req_id] = result
            return result

        candidate = self.price_for(times)
        if candidate < self.floor_price or candidate > self.price:
            result = (self.price, False)
            self.seen[req_id] = result
            return result

        self.price = candidate
        self.offers.append(candidate)
        result = (candidate, True)
        self.seen[req_id] = result
        return result

    def accepted(self):
        return [price for price in self.offers if price <= self.base_price]
