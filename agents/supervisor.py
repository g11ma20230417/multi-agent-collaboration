#!/usr/bin/env python3
"""
Supervisor Agent - 任务理解与协调层
基于 LangChain Supervisor 模式
"""

import asyncio
from typing import Dict, Any


class SupervisorAgent:
    """
    Supervisor Agent - 中心协调器
    
    职责:
    1. 理解用户意图
    2. 判断任务类型
    3. 评估复杂度
    4. 制定执行策略
    5. 协调各Agent工作
    """

    def __init__(self):
        self.task_types = {
            'code_generation': ['代码', '写', '程序', '函数', '类', '爬虫', '网站'],
            'analysis': ['分析', '解释', '比较', '评估'],
            'research': ['研究', '调查', '查找', '搜索'],
            'creative': ['创作', '写文章', '写故事', '设计'],
            'problem_solving': ['解决', '修复', '优化', '改进']
        }
        
        self.complexity_markers = {
            'high': ['系统', '完整', '项目', '应用', '多个', '复杂'],
            'medium': ['模块', '功能', '几个', '中等'],
            'low': ['简单', '一个', '单个', '基础']
        }

    async def understand_task(self, task: str) -> Dict[str, Any]:
        """
        理解任务
        
        Args:
            task: 用户任务描述
            
        Returns:
            任务理解结果
        """
        print(f"  🔍 分析任务...")
        
        # 分析任务类型
        task_type = self._classify_task(task)
        
        # 评估复杂度
        complexity = self._assess_complexity(task)
        
        # 估算Token消耗
        estimated_tokens = self._estimate_tokens(task, complexity)
        
        # 制定执行策略
        strategy = self._determine_strategy(task_type, complexity)
        
        return {
            'task_type': task_type,
            'complexity': complexity,
            'estimated_tokens': estimated_tokens,
            'strategy': strategy,
            'requires_supervisor': complexity in ['high', 'medium'],
            'parallel_possible': complexity == 'low'
        }

    def _classify_task(self, task: str) -> str:
        """分类任务类型"""
        scores = {}
        
        for task_type, keywords in self.task_types.items():
            score = sum(1 for kw in keywords if kw in task)
            scores[task_type] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'general'

    def _assess_complexity(self, task: str) -> str:
        """评估任务复杂度"""
        complexity_score = 0
        
        for level, markers in self.complexity_markers.items():
            if any(marker in task for marker in markers):
                if level == 'high':
                    complexity_score = max(complexity_score, 3)
                elif level == 'medium':
                    complexity_score = max(complexity_score, 2)
                else:
                    complexity_score = max(complexity_score, 1)
        
        # 根据任务长度调整
        if len(task) > 100:
            complexity_score = max(complexity_score, 2)
        if len(task) > 200:
            complexity_score = max(complexity_score, 3)
        
        return {3: 'high', 2: 'medium'}.get(complexity_score, 'low')

    def _estimate_tokens(self, task: str, complexity: str) -> int:
        """估算Token消耗"""
        base_tokens = len(task) // 2  # 基础Token
        
        complexity_multiplier = {
            'high': 3.0,
            'medium': 2.0,
            'low': 1.0
        }
        
        return int(base_tokens * complexity_multiplier.get(complexity, 1.0))

    def _determine_strategy(self, task_type: str, complexity: str) -> Dict[str, Any]:
        """制定执行策略"""
        strategies = {
            ('code_generation', 'high'): {
                'mode': 'multi_agent',
                'agents': ['task_decomposer', 'executor', 'optimizer'],
                'parallel': True
            },
            ('code_generation', 'medium'): {
                'mode': 'single_agent',
                'agents': ['executor'],
                'parallel': False
            },
            ('analysis', 'high'): {
                'mode': 'multi_agent',
                'agents': ['task_decomposer', 'executor', 'reflector'],
                'parallel': True
            },
            ('research', 'high'): {
                'mode': 'multi_agent',
                'agents': ['task_decomposer', 'executor', 'learner'],
                'parallel': True
            }
        }
        
        # 返回匹配策略或默认策略
        key = (task_type, complexity)
        if key in strategies:
            return strategies[key]
        
        # 默认策略
        return {
            'mode': 'single_agent',
            'agents': ['executor'],
            'parallel': complexity == 'low'
        }

    async def coordinate(self, task: str, agents: list) -> Dict[str, Any]:
        """协调多个Agent工作"""
        print(f"  🎯 协调 {len(agents)} 个Agent...")
        
        coordination_plan = {
            'sequence': agents,
            'parallel_groups': [],
            'dependencies': {}
        }
        
        return coordination_plan
