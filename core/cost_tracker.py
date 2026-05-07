#!/usr/bin/env python3
"""
Cost Tracker - 成本实时监控系统
基于 AutoGen 的成本监控功能
"""

from typing import Dict, Any
from datetime import datetime


class CostTracker:
    """
    Cost Tracker - 成本追踪器
    
    职责:
    1. 实时监控Token消耗
    2. 计算API调用费用
    3. 追踪成本趋势
    4. 设置预算提醒
    5. 生成成本报告
    """

    def __init__(self):
        # 模型定价（每1K Token的价格，单位：美元）
        self.model_pricing = {
            'gpt-4': {
                'input': 0.03,
                'output': 0.06
            },
            'gpt-3.5-turbo': {
                'input': 0.0005,
                'output': 0.0015
            },
            'claude-3': {
                'input': 0.015,
                'output': 0.075
            },
            'default': {
                'input': 0.01,
                'output': 0.03
            }
        }
        
        # 当前会话统计
        self.session_stats = {
            'total_tokens': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'total_cost': 0.0,
            'api_calls': 0,
            'start_time': datetime.now().isoformat()
        }
        
        # 历史记录
        self.history = []
        
        # 预算设置
        self.budget = {
            'daily_limit': 10.0,
            'monthly_limit': 100.0,
            'alert_threshold': 0.8  # 80%时提醒
        }

    def calculate_cost(self, tokens: int, model: str = 'default', 
                      is_output: bool = False) -> float:
        """
        计算Token消耗的费用
        
        Args:
            tokens: Token数量
            model: 模型名称
            is_output: 是否为输出Token
            
        Returns:
            费用（美元）
        """
        pricing = self.model_pricing.get(model, self.model_pricing['default'])
        
        if is_output:
            price_per_token = pricing['output']
        else:
            price_per_token = pricing['input']
        
        # 计算费用 (tokens / 1000 * price)
        cost = (tokens / 1000) * price_per_token
        
        # 更新统计
        self.session_stats['total_tokens'] += tokens
        self.session_stats['total_cost'] += cost
        self.session_stats['api_calls'] += 1
        
        if is_output:
            self.session_stats['output_tokens'] += tokens
        else:
            self.session_stats['input_tokens'] += tokens
        
        return cost

    def record_usage(self, tokens: int, cost: float, model: str = 'default'):
        """
        记录一次使用
        
        Args:
            tokens: Token数量
            cost: 费用
            model: 模型名称
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'tokens': tokens,
            'cost': cost,
            'model': model,
            'cumulative_cost': self.session_stats['total_cost']
        }
        
        self.history.append(record)
        
        # 检查预算
        self._check_budget_alert()

    def _check_budget_alert(self):
        """检查预算提醒"""
        daily_spent = self._get_daily_spending()
        
        if daily_spent >= self.budget['daily_limit'] * self.budget['alert_threshold']:
            print(f"  ⚠️  预算提醒: 当日费用 ${daily_spent:.2f} 已超过预算的 {int(self.budget['alert_threshold']*100)}%")

    def _get_daily_spending(self) -> float:
        """获取当日花费"""
        today = datetime.now().date()
        today_records = [
            r for r in self.history
            if datetime.fromisoformat(r['timestamp']).date() == today
        ]
        return sum(r['cost'] for r in today_records)

    def get_session_stats(self) -> Dict[str, Any]:
        """获取会话统计"""
        stats = self.session_stats.copy()
        stats['daily_spending'] = self._get_daily_spending()
        stats['budget_remaining'] = self.budget['daily_limit'] - stats['daily_spending']
        stats['avg_cost_per_call'] = (
            stats['total_cost'] / stats['api_calls'] 
            if stats['api_calls'] > 0 else 0
        )
        return stats

    def get_cost_report(self) -> Dict[str, Any]:
        """生成成本报告"""
        return {
            'session': self.get_session_stats(),
            'budget': self.budget,
            'model_usage': self._get_model_usage(),
            'trend': self._get_cost_trend(),
            'recommendations': self._generate_recommendations()
        }

    def _get_model_usage(self) -> Dict[str, int]:
        """获取各模型使用量"""
        model_usage = {}
        for record in self.history:
            model = record['model']
            model_usage[model] = model_usage.get(model, 0) + record['tokens']
        return model_usage

    def _get_cost_trend(self) -> str:
        """分析成本趋势"""
        if len(self.history) < 2:
            return 'stable'
        
        recent = self.history[-5:]
        if not recent:
            return 'stable'
        
        first_cost = recent[0]['cumulative_cost']
        last_cost = recent[-1]['cumulative_cost']
        
        if last_cost > first_cost * 1.2:
            return 'increasing'
        elif last_cost < first_cost * 0.8:
            return 'decreasing'
        else:
            return 'stable'

    def _generate_recommendations(self) -> list:
        """生成成本优化建议"""
        recommendations = []
        
        # 检查是否使用最贵的模型
        if 'gpt-4' in self._get_model_usage():
            recommendations.append('考虑使用 gpt-3.5-turbo 降低费用')
        
        # 检查Token消耗
        if self.session_stats['total_tokens'] > 100000:
            recommendations.append('使用上下文压缩技术减少Token消耗')
        
        # 检查API调用频率
        if self.session_stats['api_calls'] > 50:
            recommendations.append('考虑批量处理减少API调用次数')
        
        return recommendations

    def reset_session(self):
        """重置会话统计"""
        self.session_stats = {
            'total_tokens': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'total_cost': 0.0,
            'api_calls': 0,
            'start_time': datetime.now().isoformat()
        }

    def export_history(self) -> list:
        """导出使用历史"""
        return self.history
