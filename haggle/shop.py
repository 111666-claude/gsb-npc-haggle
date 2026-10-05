"""NPC 砍价：按次数给折扣阶梯，低于底价就翻脸。

缺陷：砍价次数不封顶、折扣阶梯差一档、低于底价也成交、同一个 req 重复砍价、
每次查询全扫历史报价。
"""


class Shop:
    """砍价台账。"""

    def __init__(self, base_price, floor_price, tiers):
        self.base_price = base_price
        self.floor_price = floor_price
        self.tiers = list(tiers)
        self.offers = []
        self.seen = set()
        self.scanned = 0

    def price_for(self, attempts):
        """第 attempts 次砍价后的报价。缺陷：阶梯差一档（从 0 开始算）。"""
        index = min(attempts, len(self.tiers) - 1)
        return self.base_price * (100 - self.tiers[index]) // 100

    def haggle(self, req_id, times):
        """砍 times 次，返回最终报价与是否成交。缺陷：不封顶次数、低于底价也成交、不查 req、全扫历史。"""
        self.scanned += len(self.offers)
        price = self.price_for(times)
        self.offers.append(price)
        return price, True

    def accepted(self):
        return [price for price in self.offers if price <= self.base_price]
