#!/usr/bin/env python3
"""
Token优化器
智能压缩和优化Token消耗
"""

from typing import List, Dict, Any


class TokenOptimizer:
    """Token优化器，负责减少Token消耗"""

    def __init__(self):
        self.optimization_strategies = [
            'context_compression',
            'prompt_simplification',
            'result_deduplication',
            'caching',
            'batch_processing'
        ]

    async def optimize_plan(self, subtasks: List[Dict]) -> Dict[str, Any]:
        """
        优化执行计划以减少Token消耗
        
        Args:
            subtasks: 子任务列表
            
        Returns:
            优化计划
        """
        print(f"    🧠 分析Token优化方案...")
        
        # 分析任务
        total_tokens = sum(t.get('estimated_tokens', 0) for t in subtasks)
        
        # 识别可优化点
        optimizations = self._identify_optimizations(subtasks)
        
        # 计算预计节省
        savings = self._calculate_savings(total_tokens, optimizations)
        
        # 生成优化后的计划
        optimized_plan = self._generate_optimized_plan(subtasks, optimizations)
        
        print(f"    💰 预计节省Token: {savings['percentage']:.1f}% ({savings['tokens']} tokens)")
        
        return {
            'original_tokens': total_tokens,
            'optimized_tokens': total_tokens - savings['tokens'],
            'savings': savings,
            'optimizations': optimizations,
            'plan': optimized_plan
        }

    def _identify_optimizations(self, subtasks: List[Dict]) -> List[Dict]:
        """识别可优化的任务"""
        optimizations = []
        
        # 检查重复内容
        descriptions = [t['description'] for t in subtasks]
        if len(descriptions) != len(set(descriptions)):
            optimizations.append({
                'type': 'deduplication',
                'description': '发现重复任务，可合并',
                'savings_factor': 0.2
            })
        
        # 检查可并行任务
        parallel_count = sum(1 for t in subtasks if t.get('execution_type') == 'parallel')
        if parallel_count > 1:
            optimizations.append({
                'type': 'parallel_execution',
                'description': f'{parallel_count}个任务可并行执行',
                'savings_factor': 0.15
            })
        
        # 检查长任务
        long_tasks = [t for t in subtasks if t.get('estimated_tokens', 0) > 500]
        if long_tasks:
            optimizations.append({
                'type': 'task_split',
                'description': f'{len(long_tasks)}个长任务可拆分',
                'savings_factor': 0.1
            })
        
        return optimizations

    def _calculate_savings(self, total_tokens: int, optimizations: List[Dict]) -> Dict[str, Any]:
        """计算节省量"""
        total_factor = sum(opt['savings_factor'] for opt in optimizations)
        savings_tokens = int(total_tokens * min(total_factor, 0.4))  # 最多节省40%
        
        return {
            'tokens': savings_tokens,
            'percentage': (savings_tokens / total_tokens * 100) if total_tokens > 0 else 0
        }

    def _generate_optimized_plan(self, subtasks: List[Dict], 
                                optimizations: List[Dict]) -> List[Dict]:
        """生成优化后的计划"""
        plan = subtasks.copy()
        
        # 应用优化策略
        for opt in optimizations:
            if opt['type'] == 'parallel_execution':
                # 标记并行执行
                for task in plan:
                    if task.get('execution_type') == 'parallel':
                        task['parallel_batch'] = True
            
            elif opt['type'] == 'deduplication':
                # 去重
                seen = set()
                unique_plan = []
                for task in plan:
                    key = task['description']
                    if key not in seen:
                        seen.add(key)
                        unique_plan.append(task)
                plan = unique_plan
        
        return plan

    def compress_context(self, context: str, max_length: int = 4000) -> str:
        """
        压缩上下文
        
        Args:
            context: 原始上下文
            max_length: 最大长度
            
        Returns:
            压缩后的上下文
        """
        if len(context) <= max_length:
            return context
        
        # 简单压缩策略：保留首尾，中间省略
        if len(context) > max_length:
            half = max_length // 2
            return context[:half] + f"\n... [省略 {len(context) - max_length} 字符] ...\n" + context[-half:]
        
        return context

    def simplify_prompt(self, prompt: str) -> str:
        """
        简化Prompt
        
        Args:
            prompt: 原始Prompt
            
        Returns:
            简化后的Prompt
        """
        # 移除冗余的客气话
        simplified = prompt
        
        # 移除"请"、"麻烦"等客气词
        redundant_words = ['请', '麻烦', '能不能', '可以不可以', '非常感谢']
        for word in redundant_words:
            simplified = simplified.replace(word, '')
        
        # 移除多余空格
        simplified = ' '.join(simplified.split())
        
        return simplified

    def deduplicate_results(self, results: List[str]) -> List[str]:
        """
        去重结果
        
        Args:
            results: 结果列表
            
        Returns:
            去重后的结果
        """
        seen = set()
        unique = []
        
        for result in results:
            # 使用前100字符作为key
            key = result[:100]
            if key not in seen:
                seen.add(key)
                unique.append(result)
        
        return unique

    def batch_similar_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        批处理相似任务
        
        Args:
            tasks: 任务列表
            
        Returns:
            批处理后的任务
        """
        # 按类型分组
        type_groups = {}
        for task in tasks:
            task_type = task.get('type', 'unknown')
            if task_type not in type_groups:
                type_groups[task_type] = []
            type_groups[task_type].append(task)
        
        # 创建批处理任务
        batched = []
        for task_type, group in type_groups.items():
            if len(group) > 1:
                # 创建批处理任务
                batch_task = {
                    'id': f'batch_{task_type}',
                    'type': f'batch_{task_type}',
                    'description': f'批量执行{len(group)}个{task_type}任务',
                    'tasks': group,
                    'execution_type': 'parallel',
                    'estimated_tokens': sum(t.get('estimated_tokens', 0) for t in group) * 0.8
                }
                batched.append(batch_task)
            else:
                batched.extend(group)
        
        return batched

    def get_optimization_report(self) -> Dict[str, Any]:
        """获取优化报告"""
        return {
            'strategies_available': self.optimization_strategies,
            'total_optimizations': len(self.optimization_strategies),
            'description': 'Token优化器提供多种策略减少Token消耗'
        }
