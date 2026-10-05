"""砍价命令行入口：python3 cmd_haggle.py --sample <名>，或 h/s/state 子命令配 JSON 状态。"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from haggle.shop import Shop  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(prog="npc-haggle", description="NPC 砍价")
    parser.add_argument("--sample", default=None, help="tiers / floor / cap / dup / work")
    parser.add_argument("--state", default="state.json", help="状态文件")
    parser.add_argument("command", nargs="*", help="haggle <次数> / show")
    return parser


def load(path, base, floor, tiers):
    shop = Shop(base, floor, tiers)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            shop.offers = json.load(handle).get("offers", [])
    return shop


def save(path, shop):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"offers": shop.offers}, handle)


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "tiers":
        shop = Shop(1000, 100, [10, 30])
        print("first=%d second=%d" % (shop.price_for(1), shop.price_for(2)))
    elif args.sample == "floor":
        shop = Shop(100, 95, [50])
        price, ok = shop.haggle("r1", 1)
        print("price=%d ok=%s" % (price, str(ok).lower()))
    elif args.sample == "cap":
        shop = Shop(1000, 100, [10])
        price, ok = shop.haggle("r1", 99)
        print("price=%d ok=%s" % (price, str(ok).lower()))
    elif args.sample == "dup":
        shop = Shop(1000, 100, [10, 20])
        shop.haggle("r1", 1)
        price, _ = shop.haggle("r1", 2)
        print("second=%d" % price)
    elif args.sample == "work":
        shop = Shop(1000, 100, [10])
        for index in range(3000):
            shop.haggle("r-%d" % index, 1)
        for index in range(3000):
            shop.haggle("r-other-%d" % index, 1)
        print("scanned=%d" % shop.scanned)
    elif args.command and args.command[0] == "haggle":
        shop = load(args.state, 1000, 100, [10, 20, 30])
        price, ok = shop.haggle("cmd", int(args.command[1]))
        save(args.state, shop)
        print("price=%d ok=%s" % (price, str(ok).lower()))
    elif args.command and args.command[0] == "show":
        shop = load(args.state, 1000, 100, [10, 20, 30])
        print("offers=%s" % ",".join(str(item) for item in shop.offers))
    else:
        raise SystemExit("需要 --sample tiers|floor|cap|dup|work，或 haggle/show 子命令")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
