# npc-haggle

NPC 砍价：按砍价次数给折扣阶梯，报价不得低于底价，状态可存 JSON，只用 Python 标准库。

```
python3 cmd_haggle.py --sample tiers
python3 cmd_haggle.py --sample floor
python3 cmd_haggle.py --sample cap
python3 cmd_haggle.py --sample dup
python3 cmd_haggle.py --sample work
python3 cmd_haggle.py haggle 2 --state state.json
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **折扣阶梯**：第 1 次砍价用 `tiers[0]`，第 2 次用 `tiers[1]`，次数超过阶梯长度就固定用最后一档。
- **次数上限**：同一玩家对同一件商品的砍价次数不超过 `max_attempts`，超出返回失败且报价不变。
- **底价**：报价不得低于 `floor_price`，砍到低于底价时直接按失败处理（不成交）。
- **幂等**：同一个 `req_id` 只砍一次，重复调用返回上一次的报价且不改状态。
- **不变量**：报价单调不增；报价不低于底价；同一串砍价重复执行结果相同。
- **代价**：查询不许全扫历史报价，`scanned` 不随报价数乘调用次数增长；10 万次砍价每秒 10 万次查询。

## 输出契约（不改格式）

```
first=.. second=..
price=.. ok=..
second=..
offers=..
scanned=..
```

## 目录

```
haggle/shop.py       阶梯、上限、底价与幂等
cmd_haggle.py        命令行入口（--sample 与子命令）
tests/test_shop.py   unittest 用例
```
