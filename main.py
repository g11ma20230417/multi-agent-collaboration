#!/usr/bin/env python3
"""
多Agent协同工作系统 - 主程序
功能：
1. 多Agent智能分工
2. 自我迭代优化
3. 自我学习进化
4. Token消耗优化
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from agents.task_decomposer import TaskDecomposer
from agents.executor import ExecutorAgent
from agents.optimizer import OptimizerAgent
from agents.learner import LearnerAgent
from core.token_optimizer import TokenOptimizer
from core.knowledge_base import KnowledgeBase


class MultiAgentSystem:
    """多Agent协同系统主类"""

    def __init__(self):
        self.task_decomposer = TaskDecomposer()
        self.executor = ExecutorAgent()
        self.optimizer = OptimizerAgent()
        self.learner = LearnerAgent()
        self.token_optimizer = TokenOptimizer()
        self.knowledge_base = KnowledgeBase()
        
        self.stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'total_tokens': 0,
            'avg_task_time': 0,
            'improvements': 0
        }
        
        self.load_learning_data()

    def load_learning_data(self):
        """加载历史学习数据"""
        self.learned_patterns = self.knowledge_base.get_patterns()
        self.workflow_optimizations = self.knowledge_base.get_workflows()

    async def process_task(self, task: str) -> Dict[str, Any]:
        """
        处理任务的完整流程
        
        Args:
            task: 用户任务描述
            
        Returns:
            处理结果字典
        """
        start_time = time.time()
        self.stats['total_tasks'] += 1
        
        result = {
            'success': False,
            'task': task,
            'subtasks': [],
            'results': [],
            'tokens_used': 0,
            'time_taken': 0,
            'improvements': [],
            'error': None
        }

        try:
            print(f"\n{'='*60}")
            print(f"🎯 收到任务: {task}")
            print(f"{'='*60}")

            # 步骤1: 任务分解
            print("\n[1/6] 📋 任务分解...")
            subtasks = await self.task_decomposer.decompose(task)
            result['subtasks'] = subtasks
            print(f"    分解为 {len(subtasks)} 个子任务")

            # 步骤2: Token优化规划
            print("\n[2/6] 🧠 Token优化规划...")
            optimized_plan = await self.token_optimizer.optimize_plan(subtasks)
            print(f"    预计节省Token: {optimized_plan.get('savings', 0)}%")

            # 步骤3: 智能执行
            print("\n[3/6] ⚡ 智能执行...")
            execution_results = []
            for i, subtask in enumerate(subtasks, 1):
                print(f"    执行子任务 {i}/{len(subtasks)}...")
                
                # 应用学习到的优化
                if self.learned_patterns:
                    best_pattern = self.learner.find_best_pattern(subtask)
                    if best_pattern:
                        print(f"    💡 应用优化策略: {best_pattern['strategy']}")
                        subtask = self.learner.apply_pattern(subtask, best_pattern)
                
                # 执行子任务
                exec_result = await self.executor.execute(subtask)
                execution_results.append(exec_result)
                
                # 记录Token消耗
                result['tokens_used'] += exec_result.get('tokens', 0)
                
                # 自我优化
                if exec_result.get('can_improve'):
                    improvement = await self.optimizer.optimize(subtask, exec_result)
                    if improvement:
                        result['improvements'].append(improvement)
                        self.stats['improvements'] += 1

            result['results'] = execution_results

            # 步骤4: 结果整合
            print("\n[4/6] 🔗 结果整合...")
            final_result = self._integrate_results(execution_results)
            print(f"    整合完成")

            # 步骤5: 学习进化
            print("\n[5/6] 📚 自我学习...")
            await self.learner.learn(task, subtasks, execution_results, final_result)
            print(f"    学习完成，已更新知识库")

            # 步骤6: 统计更新
            time_taken = time.time() - start_time
            result['time_taken'] = time_taken
            result['success'] = True
            self.stats['successful_tasks'] += 1
            self.stats['total_tokens'] += result['tokens_used']
            
            # 计算平均时间
            if self.stats['total_tasks'] > 0:
                self.stats['avg_task_time'] = (
                    (self.stats['avg_task_time'] * (self.stats['total_tasks'] - 1) + time_taken) 
                    / self.stats['total_tasks']
                )

            print(f"\n{'='*60}")
            print(f"✅ 任务完成!")
            print(f"{'='*60}")
            print(f"    ⏱️  耗时: {time_taken:.2f}秒")
            print(f"    💰 Token消耗: {result['tokens_used']}")
            print(f"    📊 子任务: {len(subtasks)}")
            print(f"    🚀 优化次数: {len(result['improvements'])}")
            print(f"{'='*60}\n")

        except Exception as e:
            result['error'] = str(e)
            self.stats['failed_tasks'] += 1
            print(f"\n❌ 任务失败: {e}")

        return result

    def _integrate_results(self, results: List[Dict]) -> str:
        """整合多个子任务的结果"""
        integrated = []
        
        for i, result in enumerate(results, 1):
            if result.get('success'):
                integrated.append(f"[子任务{i}] {result.get('output', '')}")
            else:
                integrated.append(f"[子任务{i}] ❌ {result.get('error', 'Unknown error')}")
        
        return "\n\n".join(integrated)

    async def self_improve(self):
        """自我迭代优化"""
        print("\n🔄 开始自我迭代优化...")
        
        # 分析历史数据
        analysis = await self.learner.analyze_history()
        
        # 寻找优化空间
        improvements = []
        
        # 1. 检查Token使用效率
        if self.stats['total_tokens'] > 0:
            avg_tokens = self.stats['total_tokens'] / self.stats['total_tasks']
            if avg_tokens > 10000:
                improvements.append({
                    'type': 'token_optimization',
                    'suggestion': '考虑使用更简洁的prompt模板'
                })
        
        # 2. 检查执行时间
        if self.stats['avg_task_time'] > 30:
            improvements.append({
                'type': 'performance',
                'suggestion': '考虑并行执行独立的子任务'
            })
        
        # 3. 检查成功率
        if self.stats['total_tasks'] > 5:
            success_rate = self.stats['successful_tasks'] / self.stats['total_tasks']
            if success_rate < 0.8:
                improvements.append({
                    'type': 'reliability',
                    'suggestion': '增加错误处理和重试机制'
                })
        
        print(f"    发现 {len(improvements)} 个优化空间")
        
        for improvement in improvements:
            print(f"    💡 {improvement['suggestion']}")
        
        return improvements

    def get_stats(self) -> Dict:
        """获取系统统计信息"""
        return {
            **self.stats,
            'success_rate': (
                self.stats['successful_tasks'] / self.stats['total_tasks'] 
                if self.stats['total_tasks'] > 0 else 0
            ),
            'learned_patterns_count': len(self.learned_patterns),
            'workflows_count': len(self.workflow_optimizations)
        }

    async def run_interactive(self):
        """交互模式"""
        print("\n" + "="*60)
        print("🤖 多Agent协同工作系统 - 交互模式")
        print("="*60)
        print("\n命令:")
        print("  - 输入任务，系统自动分配Agent处理")
        print("  - 'stats' - 查看统计信息")
        print("  - 'improve' - 触发自我优化")
        print("  - 'patterns' - 查看学习到的模式")
        print("  - 'quit' - 退出")
        print("="*60 + "\n")

        while True:
            try:
                cmd = input("💬 请输入任务: ").strip()
                
                if not cmd:
                    continue
                
                if cmd.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 再见!")
                    break
                
                if cmd.lower() == 'stats':
                    stats = self.get_stats()
                    print("\n📊 系统统计:")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                    continue
                
                if cmd.lower() == 'improve':
                    await self.self_improve()
                    continue
                
                if cmd.lower() == 'patterns':
                    print(f"\n📚 已学习 {len(self.learned_patterns)} 个模式")
                    for pattern in self.learned_patterns[:5]:
                        print(f"  - {pattern['name']}")
                    continue
                
                # 处理任务
                await self.process_task(cmd)
                
            except KeyboardInterrupt:
                print("\n\n👋 退出中...")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")


async def main():
    """主函数"""
    system = MultiAgentSystem()
    
    if len(__import__('sys').argv) > 1:
        # 命令行模式
        task = ' '.join(__import__('sys').argv[1:])
        result = await system.process_task(task)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 交互模式
        await system.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
