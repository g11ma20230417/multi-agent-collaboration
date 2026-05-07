#!/usr/bin/env python3
"""
任务分解Agent
智能分析任务，自动拆分为可并行的子任务
"""

import asyncio
from typing import List, Dict, Any


class TaskDecomposer:
    """任务分解Agent"""

    def __init__(self):
        self.decomposition_strategies = {
            'parallel': '可并行执行',
            'sequential': '必须顺序执行',
            'dependent': '依赖其他任务'
        }

    async def decompose(self, task: str) -> List[Dict[str, Any]]:
        """
        分解任务为子任务
        
        Args:
            task: 原始任务描述
            
        Returns:
            子任务列表
        """
        print(f"    📝 分析任务: {task[:50]}...")
        
        # 模拟AI分析过程
        await asyncio.sleep(0.5)
        
        # 智能分解策略
        subtasks = []
        
        # 分析任务类型
        if self._is_complex_task(task):
            # 复杂任务 - 多步骤分解
            subtasks = self._decompose_complex(task)
        elif self._is_simple_task(task):
            # 简单任务 - 单步执行
            subtasks = self._decompose_simple(task)
        else:
            # 中等任务 - 适度分解
            subtasks = self._decompose_moderate(task)
        
        # 标记依赖关系
        subtasks = self._mark_dependencies(subtasks)
        
        # 优化执行顺序
        subtasks = self._optimize_order(subtasks)
        
        return subtasks

    def _is_complex_task(self, task: str) -> bool:
        """判断是否为复杂任务"""
        complex_indicators = [
            '系统', '项目', '应用', '完整', '全面',
            '多个', '一系列', '包括', '集成'
        ]
        return any(indicator in task for indicator in complex_indicators)

    def _is_simple_task(self, task: str) -> bool:
        """判断是否为简单任务"""
        simple_indicators = [
            '解释', '说明', '什么是', '怎么', '如何',
            '简单', '单个', '一个'
        ]
        return any(indicator in task for indicator in simple_indicators)

    def _decompose_complex(self, task: str) -> List[Dict[str, Any]]:
        """分解复杂任务"""
        return [
            {
                'id': 1,
                'type': 'analysis',
                'description': '分析需求和技术选型',
                'execution_type': 'sequential',
                'priority': 'high',
                'estimated_tokens': 500
            },
            {
                'id': 2,
                'type': 'design',
                'description': '设计系统架构和模块',
                'execution_type': 'sequential',
                'priority': 'high',
                'estimated_tokens': 800
            },
            {
                'id': 3,
                'type': 'backend',
                'description': '实现后端逻辑',
                'execution_type': 'parallel',
                'priority': 'medium',
                'estimated_tokens': 1500
            },
            {
                'id': 4,
                'type': 'frontend',
                'description': '实现前端界面',
                'execution_type': 'parallel',
                'priority': 'medium',
                'estimated_tokens': 1200
            },
            {
                'id': 5,
                'type': 'integration',
                'description': '集成测试和优化',
                'execution_type': 'sequential',
                'priority': 'high',
                'estimated_tokens': 600
            }
        ]

    def _decompose_simple(self, task: str) -> List[Dict[str, Any]]:
        """分解简单任务"""
        return [
            {
                'id': 1,
                'type': 'response',
                'description': task,
                'execution_type': 'sequential',
                'priority': 'high',
                'estimated_tokens': 300
            }
        ]

    def _decompose_moderate(self, task: str) -> List[Dict[str, Any]]:
        """分解中等复杂度任务"""
        return [
            {
                'id': 1,
                'type': 'research',
                'description': '收集相关信息',
                'execution_type': 'sequential',
                'priority': 'medium',
                'estimated_tokens': 400
            },
            {
                'id': 2,
                'type': 'implementation',
                'description': task,
                'execution_type': 'sequential',
                'priority': 'high',
                'estimated_tokens': 800
            }
        ]

    def _mark_dependencies(self, subtasks: List[Dict]) -> List[Dict]:
        """标记任务依赖关系"""
        for i, subtask in enumerate(subtasks):
            if i == 0:
                subtask['depends_on'] = []
            else:
                # 默认依赖前一个任务
                subtask['depends_on'] = [subtasks[i-1]['id']]
        
        return subtasks

    def _optimize_order(self, subtasks: List[Dict]) -> List[Dict]:
        """优化执行顺序"""
        # 分离可并行和必须顺序的任务
        parallel = [t for t in subtasks if t['execution_type'] == 'parallel']
        sequential = [t for t in subtasks if t['execution_type'] == 'sequential']
        
        # 按优先级排序
        parallel.sort(key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x['priority'], 3))
        sequential.sort(key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x['priority'], 3))
        
        # 合并：顺序任务在前，并行任务在后
        return sequential + parallel

    def get_strategy(self, task: str) -> str:
        """获取任务执行策略"""
        if self._is_complex_task(task):
            return 'complex_strategy'
        elif self._is_simple_task(task):
            return 'simple_strategy'
        else:
            return 'moderate_strategy'
