# -*- coding: utf-8 -*-
"""
Gate.io 永续合约 Python SDK
=============================
异步API客户端，支持合约交易、行情订阅、持仓管理。
安装: pip install gate_futures

Usage:
    from gate_futures import GateFutures
    
    client = GateFutures(api_key, secret_key, network='testnet')
    ticker = await client.get_ticker('BTC_USDT')
    await client.place_order('BTC_USDT', 'buy', '0.001')
"""

__version__ = '1.0.0'
__author__ = 'AI Agent'

from .client import GateFutures
from .ws_client import GateWebSocket

__all__ = ['GateFutures', 'GateWebSocket']
