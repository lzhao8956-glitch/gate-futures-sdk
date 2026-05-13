# -*- coding: utf-8 -*-
"""
异步多合约交易示例
同时监控多个合约，支持并行下单
"""
import asyncio
from gate_futures import GateFutures

CONTRACTS = ['BTC_USDT', 'ETH_USDT', 'SOL_USDT']

async def get_all_prices(client):
    """并行获取所有合约行情"""
    tasks = [client.get_ticker(c) for c in CONTRACTS]
    return dict(zip(CONTRACTS, await asyncio.gather(*tasks)))

async def main():
    client = GateFutures('YOUR_KEY', 'YOUR_SECRET', network='testnet')
    
    while True:
        prices = await get_all_prices(client)
        for contract, ticker in prices.items():
            print(f"{contract}: ${ticker['last']} ({ticker['change_percentage']}%)")
        await asyncio.sleep(10)  # 每10秒刷新

if __name__ == '__main__':
    asyncio.run(main())
