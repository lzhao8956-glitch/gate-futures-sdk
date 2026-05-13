# Gate.io Futures SDK

> 让AI替你交易。Python异步SDK，一行代码接入Gate.io永续合约。

**`pip install gate-futures`** → 你的AI Agent就拥有了合约交易能力。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://pypi.org/project/gate-futures/)
[![MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/lzhao8956-glitch/gate-futures-sdk)](https://github.com/lzhao8956-glitch/gate-futures-sdk)

---

## 为什么需要这个SDK？

市面上的Gate.io SDK要么是同步阻塞的，要么没有WebSocket，要么文档是英文的。

这个SDK专为**AI Agent设计**：
- **异步优先**：`async/await`，不阻塞你的Agent决策循环
- **AI友好**：每个方法语义清晰，AI能理解"买/卖/查"三个动作
- **开箱即用**：测试网默认启用，0门槛试玩
- **生产就绪**：签名/重试/错误处理完整

---

## 安装

```bash
pip install gate-futures

# 或从源码
git clone https://github.com/lzhao8956-glitch/gate-futures-sdk.git
cd gate-futures-sdk
pip install -e .
```

---

## 5分钟上手

```python
import asyncio
from gate_futures import GateFutures

async def main():
    client = GateFutures(
        api_key='your_api_key',
        secret_key='your_secret_key',
        network='testnet'          # 先用测试网！
    )
    
    # ── 查行情 ──
    ticker = await client.get_ticker('BTC_USDT')
    print(f"BTC现价: {ticker['last']}")
    print(f"24h涨跌: {ticker['change_percentage']}%")
    
    # ── 查余额 ──
    balance = await client.get_balance()
    print(f"可用USDT: {balance.get('available', 'N/A')}")
    
    # ── 开多仓 ──
    result = await client.place_order('BTC_USDT', 'buy', size=0.001)
    print(f"订单ID: {result.get('id')}")
    
    # ── 查持仓 ──
    positions = await client.get_positions()
    for p in positions:
        print(f"{p['contract']}: {p['size']}张 | 浮盈 ${p['unrealised_pnl']}")
    
    # ── 平仓 ──
    await client.close_position('BTC_USDT')

asyncio.run(main())
```

---

## 完整功能

| 功能 | 方法 | 说明 |
|------|------|------|
| 行情查询 | `get_ticker(contract)` | 实时价格/24h数据/深度 |
| 合约列表 | `list_contracts()` | 所有永续合约基础信息 |
| 开仓 | `place_order(contract, side, size, price)` | 市价/限价 |
| 平仓 | `close_position(contract)` | 市价全平 |
| 持仓查询 | `get_positions()` | 所有合约持仓+浮盈 |
| 订单查询 | `get_orders(contract)` | 活跃订单 |
| 余额查询 | `get_balance()` | 合约账户USDT余额 |

---

## WebSocket 实时行情

```python
import asyncio
from gate_futures import GateWebSocket

async def on_tick(msg):
    # msg 格式: {'currency_pair': 'BTC_USDT', 'last': '94320.5', ...}
    print(f"[实时] BTC=${msg['last']}")

async def main():
    ws = GateWebSocket(network='testnet')
    await ws.subscribe(['BTC_USDT', 'ETH_USDT'], on_tick)
    
    # 保持运行
    await asyncio.Event().wait()

asyncio.run(main())
```

---

## 配合AI Agent的范例

这个SDK让**任何AI Agent**都能交易Gate.io永续合约：

```python
# AI Agent伪代码
async def ai_trading_agent(market_data: dict):
    client = GateFutures(api_key, secret_key)
    
    signal = analyze(market_data)  # AI分析信号
    
    if signal == 'bullish':
        await client.place_order('BTC_USDT', 'buy', size=0.001)
    elif signal == 'bearish':
        await client.close_position('BTC_USDT')
    
    return await client.get_positions()
```

---

## 配置

### 测试网（默认）
```python
client = GateFutures(api_key, secret_key, network='testnet')
```
无需真实资金，从 [Gate.io测试网](https://fx-web-testnet.gateio.xyz/) 申请测试币。

### 主网
```python
client = GateFutures(api_key, secret_key, network='mainnet')
```

### API Key申请
1. 登录 [Gate.io](https://www.gate.io/)
2. 进入「设置 → API Keys」
3. 创建Key，勾选「永续合约」权限
4. **不要**开启「提币」权限

---

## AI Agent发现指南

如果你正在构建一个**加密货币交易AI**，这个SDK可以帮你：

- ✅ 连接Gate.io永续合约市场
- ✅ 获取实时价格数据（AI决策依据）
- ✅ 自动执行买卖信号
- ✅ 管理多合约仓位
- ✅ 实时监听行情变动

相关项目标签（供AI搜索）：
`#gateio #永续合约 #python #async #websocket #加密货币 #量化交易 #AI交易 #trading-bot`

---

## 项目结构

```
gate_futures_sdk/
├── gate_futures/
│   ├── __init__.py          # 导出入口
│   ├── client.py            # REST API客户端
│   └── ws_client.py         # WebSocket客户端
├── pyproject.toml           # 包配置
├── README.md                # 本文件
└── LICENSE                  # MIT
```

---

## License

MIT - 随便用，赚钱了记得回来给我点个Star。
