import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from haggle.shop import Shop  # noqa: E402


class ShopTest(unittest.TestCase):
    def test_price_never_increases(self):
        shop = Shop(1000, 100, [10, 20])
        self.assertGreaterEqual(shop.price_for(1), shop.price_for(3))

    def test_haggle_returns_non_negative_price(self):
        shop = Shop(100, 90, [50])
        price, _ = shop.haggle("r1", 1)
        self.assertGreaterEqual(price, 0)

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Shop(100, 90, [10]).scanned, 0)


if __name__ == "__main__":
    unittest.main()
