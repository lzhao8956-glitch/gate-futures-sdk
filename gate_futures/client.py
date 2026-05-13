# -*- coding: utf-8 -*-
"""
Gate.io API v4 异步客户端 - 永续合约
"""

import asyncio
import hashlib
import hmac
import time
from typing import Optional, Dict, Any, List
import json

BASE_URL = 'https://api.gateio.xyz'
TESTNET_URL = 'https://fx-api-testnet.gateio.xyz'


class GateFutures:
    """Gate.io 永续合约异步客户端"""
    
    def __init__(self, api_key: str, secret_key: str, network: str = 'testnet'):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base = TESTNET_URL if network == 'testnet' else BASE_URL
        self.network = network
    
    # ─── 签名 ──────────────────────────────────────────────────────────
    
    def _sign(self, method: str, path: str, query_string: str = '', body: str = '') -> str:
        """生成HMAC-SHA512签名"""
        timestamp = str(int(time.time()))
        host = 'api.gateio.xyz' if self.network != 'testnet' else 'fx-api-testnet.gateio.xyz'
        hashed_payload = hashlib.sha512(body.encode()).hexdigest() if body else ''
        signed_str = f"{method}\n{host}\n{path}\n{timestamp}{query_string}{hashed_payload}"
        return hmac.new(
            self.secret_key.encode(),
            signed_str.encode(),
            hashlib.sha512
        ).hexdigest()
    
    async def _request(self, method: str, path: str, params: Optional[Dict] = None) -> Dict:
        """发请求"""
        query_parts = []
        if params:
            for k, v in params.items():
                if v is not None and v != '':
                    query_parts.append(f"{k}={v}")
        query_string = '?' + '&'.join(query_parts) if query_parts else ''
        body = json.dumps(params) if method in ('POST', 'DELETE') and params else ''
        
        headers = {
            'KEY': self.api_key,
            'SIGN': self._sign(method, path, query_string, body),
            'Timestamp': str(int(time.time())),
            'Content-Type': 'application/json',
        }
        
        url = self.base + path + query_string
        async with asyncio.Lock():
            resp = await asyncio.to_thread(__import__('urllib.request').request, url, method=method, data=body.encode() if body else None, headers=headers)
        
        import urllib.request
        req = urllib.request.Request(url, data=body.encode() if body else None, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            return {'error': True, 'code': e.code, 'message': e.read().decode()}
    
    # ─── 行情 ──────────────────────────────────────────────────────────
    
    async def get_ticker(self, contract: str) -> Dict:
        """获取指定合约行情"""
        return await self._request('GET', f'/api/v4/futures/usdt/contracts/{contract}')
    
    async def list_contracts(self) -> List[Dict]:
        """列出所有永续合约"""
        return await self._request('GET', '/api/v4/futures/usdt/contracts')
    
    async def get_positions(self) -> List[Dict]:
        """获取所有合约持仓"""
        return await self._request('GET', '/api/v4/futures/usdt/positions')
    
    async def get_position(self, contract: str) -> Dict:
        """获取指定合约持仓"""
        return await self._request('GET', f'/api/v4/futures/usdt/positions/{contract}')
    
    # ─── 交易 ──────────────────────────────────────────────────────────
    
    async def place_order(self, contract: str, side: str, size: float, 
                         price: Optional[float] = None, 
                         order_type: str = 'market') -> Dict:
        """
        下单
        :param contract: 合约如 'BTC_USDT'
        :param side: 'buy' 或 'sell'
        :param size: 数量（正数）
        :param price: 市价单填None，限价单填价格
        :param order_type: 'market' 或 'limit'
        """
        params = {
            'contract': contract,
            'side': side,
            'size': str(int(size)) if size > 0 else str(int(size)),
            'type': order_type,
        }
        if price:
            params['price'] = str(price)
        return await self._request('POST', '/api/v4/futures/usdt/orders', params)
    
    async def close_position(self, contract: str) -> Dict:
        """市价全平指定合约仓位"""
        return await self.place_order(contract, 'sell', 0)  # size=0 = 平仓
    
    async def get_orders(self, contract: str) -> List[Dict]:
        """获取指定合约活跃订单"""
        return await self._request('GET', f'/api/v4/futures/usdt/orders', {'contract': contract})
    
    # ─── 余额 ──────────────────────────────────────────────────────────
    
    async def get_balance(self) -> Dict:
        """获取合约账户余额"""
        return await self._request('GET', '/api/v4/futures/usdt/accounts')
    
    # ─── WebSocket实时行情（简单封装）───────────────────────────────
    
    async def ws_subscribe(self, channel: str, contracts: List[str]):
        """
        WebSocket订阅演示（需要gateway库支持）
        channel: 'tickers' | 'trades' | 'book_ticker' | 'futures'
        """
        # 完整WS实现见 gate_futures/ws_client.py
        print(f"[GateFutures] WS subscribe: {channel} for {contracts}")
        return {'status': 'subscribed', 'channel': channel, 'contracts': contracts}
