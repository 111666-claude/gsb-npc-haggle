"""NPC 砍价：按次数给折扣阶梯，低于底价就翻脸。"""


class Shop:
    """砍价台账：阶梯折扣、次数上限、底价与 req_id 幂等。"""

    def __init__(self, base_price, floor_price, tiers, max_attempts=10):
        self.base_price = base_price
        self.floor_price = floor_price
        self.tiers = list(tiers)
        self.max_attempts = max_attempts
        self.offers = []
        self.seen = {}
        self.scanned = 0

    def price_for(self, attempts):
        """第 attempts 次砍价（1-based）对应的报价，超出阶梯长度固定最后一档。"""
        index = min(max(attempts, 1) - 1, len(self.tiers) - 1)
        return self.base_price * (100 - self.tiers[index]) // 100

    def haggle(self, req_id, times):
        """第 times 次砍价：同一 req_id 只生效一次，超上限或破底价返回失败且不改报价台账。"""
        self.scanned += 1
        if req_id in self.seen:
            return self.seen[req_id]
        price = self.price_for(times)
        if self.offers and price > self.offers[-1]:
            price = self.offers[-1]
        ok = times <= self.max_attempts and price >= self.floor_price
        self.seen[req_id] = (price, ok)
        if ok:
            self.offers.append(price)
        return price, ok

    def accepted(self):
        return [price for price in self.offers if price <= self.base_price]
