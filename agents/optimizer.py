#!/usr/bin/env python3
"""
优化Agent
分析执行结果，自动寻找优化空间
"""

import asyncio
from typing import Dict, Any, List


class OptimizerAgent:
    """优化Agent，负责分析和改进执行效果"""

    def __init__(self):
        self.optimization_rules = self._init_optimization_rules()

    def _init_optimization_rules(self) -> List[Dict]:
        """初始化优化规则"""
        return [
            {
                'name': '减少重复输出',
                'condition': lambda r: len(set(r.get('output', '').split())) < len(r.get('output', '').split()) * 0.5,
                'action': '合并重复内容，使用摘要'
            },
            {
                'name': '精简代码注释',
                'condition': lambda r: '代码' in r.get('description', '') and len(r.get('output', '')) > 2000,
                'action': '删除冗余注释，保留关键说明'
            },
            {
                'name': '优化Prompt长度',
                'condition': lambda r: r.get('tokens', 0) > 1000,
                'action': '使用更简洁的prompt模板'
            },
            {
                'name': '并行执行优化',
                'condition': lambda r: r.get('time', 0) > 5,
                'action': '考虑并行执行独立任务'
            }
        ]

    async def optimize(self, task: Dict, result: Dict) -> Dict[str, Any]:
        """
        分析并优化任务执行结果
        
        Args:
            task: 原始任务
            result: 执行结果
            
        Returns:
            优化建议
        """
        print(f"      🔍 分析优化空间...")
        
        improvements = []
        
        # 应用优化规则
        for rule in self.optimization_rules:
            if rule['condition'](result):
                improvements.append({
                    'type': rule['name'],
                    'suggestion': rule['action'],
                    'potential_savings': self._estimate_savings(result, rule)
                })
        
        # 智能优化建议
        if result.get('tokens', 0) > 800:
            improvements.append({
                'type': 'token_optimization',
                'suggestion': '考虑使用上下文压缩技术',
                'potential_savings': f"可节省 {int(result.get('tokens', 0) * 0.3)} tokens"
            })
        
        if result.get('time', 0) > 3:
            improvements.append({
                'type': 'performance',
                'suggestion': '考虑使用缓存和预加载',
                'potential_savings': f"可节省 {int(result.get('time', 0) * 0.4)} 秒"
            })
        
        print(f"      💡 发现 {len(improvements)} 个优化点")
        
        return {
            'task_id': task['id'],
            'improvements': improvements,
            'can_apply': len(improvements) > 0
        }

    def _estimate_savings(self, result: Dict, rule: Dict) -> str:
        """估算优化节省"""
        tokens = result.get('tokens', 0)
        time_taken = result.get('time', 0)
        
        if rule['name'] == '减少重复输出':
            return f"可节省 {int(tokens * 0.2)} tokens"
        elif rule['name'] == '精简代码注释':
            return f"可节省 {int(tokens * 0.15)} tokens"
        elif rule['name'] == '优化Prompt长度':
            return f"可节省 {int(tokens * 0.3)} tokens"
        elif rule['name'] == '并行执行优化':
            return f"可节省 {int(time_taken * 0.5)} 秒"
        
        return "未知节省量"

    async def optimize_workflow(self, tasks: List[Dict]) -> Dict[str, Any]:
        """
        优化整体工作流程
        
        Args:
            tasks: 任务列表
            
        Returns:
            优化后的工作流程
        """
        print(f"    🔧 优化工作流程...")
        
        # 识别可并行的任务
        parallel_groups = self._identify_parallel_tasks(tasks)
        
        # 识别可复用的组件
        reusable = self._identify_reusable_components(tasks)
        
        # 识别可缓存的结果
        cacheable = self._identify_cacheable_results(tasks)
        
        optimization = {
            'parallel_groups': parallel_groups,
            'reusable_components': reusable,
            'cacheable_results': cacheable,
            'estimated_time_savings': self._estimate_time_savings(parallel_groups),
            'estimated_token_savings': self._estimate_token_savings(reusable, cacheable)
        }
        
        print(f"    ✅ 流程优化完成")
        print(f"      ⏱️  预计节省时间: {optimization['estimated_time_savings']} 秒")
        print(f"      💰 预计节省Token: {optimization['estimated_token_savings']}")
        
        return optimization

    def _identify_parallel_tasks(self, tasks: List[Dict]) -> List[List[int]]:
        """识别可并行执行的任务组"""
        parallel = []
        current_group = []
        
        for task in tasks:
            if task.get('execution_type') == 'parallel':
                current_group.append(task['id'])
            else:
                if current_group:
                    parallel.append(current_group)
                    current_group = []
        
        if current_group:
            parallel.append(current_group)
        
        return parallel

    def _identify_reusable_components(self, tasks: List[Dict]) -> List[Dict]:
        """识别可复用的组件"""
        components = []
        
        # 分析任务类型
        types = [t['type'] for t in tasks]
        
        # 统计重复类型
        from collections import Counter
        type_counts = Counter(types)
        
        for t, count in type_counts.items():
            if count > 1:
                components.append({
                    'type': t,
                    'count': count,
                    'suggestion': f'创建通用{t}组件复用'
                })
        
        return components

    def _identify_cacheable_results(self, tasks: List[Dict]) -> List[str]:
        """识别可缓存的结果"""
        cacheable = []
        
        for task in tasks:
            if task['type'] in ['research', 'analysis']:
                cacheable.append(task['description'][:50])
        
        return cacheable

    def _estimate_time_savings(self, parallel_groups: List[List[int]]) -> int:
        """估算时间节省"""
        # 假设每个并行组节省 (n-1) * 单任务时间
        savings = 0
        for group in parallel_groups:
            if len(group) > 1:
                savings += (len(group) - 1) * 2  # 假设单任务2秒
        return savings

    def _estimate_token_savings(self, reusable: List, cacheable: List) -> int:
        """估算Token节省"""
        # 可复用组件节省 30%，缓存节省 40%
        savings = 0
        for comp in reusable:
            savings += 300 * comp['count']
        for item in cacheable:
            savings += 200
        return savings
