# -*- coding: utf-8 -*-
"""
Gate.io 永续合约 WebSocket 实时行情
"""

import asyncio
import json
import hashlib
import hmac
import time
import websockets
from typing import Callable, List


class GateWebSocket:
    """
    Gate.io WebSocket 客户端（永续合约）
    
    Usage:
        async def on_tick(msg):
            print(msg)
        
        ws = GateWebSocket('api_key', 'secret_key', network='testnet')
        await ws.subscribe(['BTC_USDT', 'ETH_USDT'], on_tick)
    """
    
    def __init__(self, api_key: str, secret_key: str, network: str = 'testnet'):
        self.api_key = api_key
        self.secret_key = secret_key
        self.network = network
        self.ws = None
        self.running = False
    
    async def connect(self):
        """建立WebSocket连接"""
        url = 'wss://fx-ws-testnet.gateio.xyz/v4/ws' if self.network == 'testnet' \
              else 'wss://api.gateio.xyz/v4/ws'
        self.ws = await websockets.connect(url)
        self.running = True
        asyncio.create_task(self._read_loop())
    
    async def _read_loop(self):
        """持续读取消息"""
        while self.running and self.ws:
            try:
                msg = await self.ws.recv()
                data = json.loads(msg)
                if callback := getattr(self, '_callback', None):
                    callback(data)
            except Exception as e:
                print(f"[GateWS] read error: {e}")
                break
    
    async def subscribe(self, contracts: List[str], callback: Callable):
        """
        订阅实时tick（ticker频道）
        订阅多个合约: ['BTC_USDT', 'ETH_USDT']
        """
        if not self.ws:
            await self.connect()
        
        self._callback = callback
        
        for contract in contracts:
            sub_msg = {
                'id': int(time.time()),
                'method': 'ticker.subscribe',
                'params': [contract],
            }
            await self.ws.send(json.dumps(sub_msg))
        
        return {'subscribed': contracts}
    
    async def subscribe_trades(self, contracts: List[str], callback: Callable):
        """订阅逐笔成交"""
        if not self.ws:
            await self.connect()
        self._callback = callback
        for contract in contracts:
            await self.ws.send(json.dumps({
                'id': int(time.time()),
                'method': 'trades.subscribe',
                'params': [contract],
            }))
    
    async def close(self):
        self.running = False
        if self.ws:
            await self.ws.close()
