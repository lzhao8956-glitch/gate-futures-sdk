# -*- coding: utf-8 -*-
"""
WebSocket实时行情订阅
推送而非轮询，延迟最低
"""
import asyncio
from gate_futures import GateWebSocket

async def on_price(msg):
    print(f"[实时] {msg.get('currency_pair')} = ${msg.get('last')}")

async def main():
    ws = GateWebSocket(network='testnet')
    await ws.subscribe(['BTC_USDT', 'ETH_USDT'], on_price)
    await asyncio.Event().wait()  # 永远运行

if __name__ == '__main__':
    asyncio.run(main())
