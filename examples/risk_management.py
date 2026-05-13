# -*- coding: utf-8 -*-
"""
风控模块示例
每笔交易前检查仓位、余额、每日交易次数
"""

class RiskManager:
    def __init__(self, client, max_daily_trades=10, max_position_pct=20):
        self.client = client
        self.max_daily_trades = max_daily_trades
        self.max_position_pct = max_position_pct
        self.daily_trades = 0
    
    async def pre_trade_check(self, contract, size):
        # 检查每日交易次数
        if self.daily_trades >= self.max_daily_trades:
            return False, "每日交易上限已达"
        
        # 检查持仓比例
        positions = await self.client.get_positions()
        balance = await self.client.get_balance()
        total_value = sum(float(p.get('value', 0)) for p in positions)
        if total_value / float(balance.get('available', 1)) > self.max_position_pct / 100:
            return False, "仓位超过上限"
        
        return True, "检查通过"
    
    def after_trade(self):
        self.daily_trades += 1
