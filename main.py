#!/usr/bin/env python3
"""
升级版多Agent协同系统 v2.0
基于 LangChain/AutoGPT/CrewAI/AutoGen 最佳实践

新增特性：
1. Supervisor 协调层 - 中心化任务调度
2. 链式思维推理 - 增强决策透明度
3. 自我反思机制 - 试错-调整能力
4. 成本实时监控 - Token消耗追踪
5. 错误自动恢复 - 系统稳定性保障
6. 异步并行优化 - 执行效率提升
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict

from agents.task_decomposer import TaskDecomposer
from agents.executor import ExecutorAgent
from agents.optimizer import OptimizerAgent
from agents.learner import LearnerAgent
from agents.supervisor import SupervisorAgent
from agents.reflector import ReflectorAgent
from core.token_optimizer import TokenOptimizer
from core.knowledge_base import KnowledgeBase
from core.cost_tracker import CostTracker


class MultiAgentSystemV2:
    """
    升级版多Agent协同系统 v2.0
    
    架构:
    User → Supervisor(协调层) → TaskDecomposer(分解)
                          ↓
                      Executors(执行) → Reflector(反思)
                          ↓
                      Optimizer(优化) → Learner(学习)
                          ↓
                      Knowledge Base(知识库)
    """

    def __init__(self):
        # 核心组件
        self.supervisor = SupervisorAgent()
        self.task_decomposer = TaskDecomposer()
        self.executor = ExecutorAgent()
        self.optimizer = OptimizerAgent()
        self.learner = LearnerAgent()
        self.reflector = ReflectorAgent()
        self.token_optimizer = TokenOptimizer()
        self.knowledge_base = KnowledgeBase()
        self.cost_tracker = CostTracker()
        
        # 统计信息
        self.stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'avg_task_time': 0,
            'reflections': 0,
            'optimizations': 0,
            'error_recoveries': 0
        }
        
        # 配置
        self.config = {
            'max_retries': 3,
            'reflection_enabled': True,
            'cost_limit': 10.0,
            'timeout': 120,
            'parallel_execution': True
        }
        
        self.load_learning_data()

    def load_learning_data(self):
        """加载历史学习数据"""
        self.learned_patterns = self.knowledge_base.get_patterns()
        self.workflow_optimizations = self.knowledge_base.get_workflows()

    async def process_task(self, task: str) -> Dict[str, Any]:
        """
        处理任务的完整流程 (升级版)
        
        流程: 接收 → 理解 → 分解 → 计划 → 执行 → 反思 → 优化 → 学习
        """
        start_time = time.time()
        self.stats['total_tasks'] += 1
        
        result = {
            'success': False,
            'task': task,
            'understanding': None,
            'plan': None,
            'execution': {
                'subtasks': [],
                'results': [],
                'tokens_used': 0,
                'cost': 0.0
            },
            'reflection': None,
            'optimizations': [],
            'final_output': None,
            'error': None,
            'execution_time': 0
        }

        try:
            print(f"\n{'='*60}")
            print(f"🚀 Multi-Agent System v2.0")
            print(f"{'='*60}")
            print(f"📋 任务: {task}")

            # 阶段1: 理解任务 (Supervisor)
            print(f"\n阶段1: 理解任务")
            understanding = await self.supervisor.understand_task(task)
            result['understanding'] = understanding
            print(f"  ✅ 任务类型: {understanding['task_type']}")
            print(f"  ✅ 复杂度: {understanding['complexity']}")
            print(f"  ✅ 预计Token: {understanding['estimated_tokens']}")

            # 阶段2: 任务分解
            print(f"\n阶段2: 任务分解")
            subtasks = await self.task_decomposer.decompose(task)
            result['execution']['subtasks'] = subtasks
            print(f"  📝 分解为 {len(subtasks)} 个子任务")

            # 阶段3: 智能规划 (Token优化)
            print(f"\n阶段3: 智能规划 & Token优化")
            optimized_plan = await self.token_optimizer.optimize_plan(subtasks)
            result['plan'] = optimized_plan
            print(f"  💰 预计Token: {optimized_plan['original_tokens']}")
            print(f"  🎯 优化后Token: {optimized_plan['optimized_tokens']}")
            print(f"  📉 节省: {optimized_plan['savings']['percentage']:.1f}%")

            # 阶段4: 执行 (支持并行)
            print(f"\n阶段4: 智能执行")
            execution_result = await self._execute_with_monitoring(subtasks)
            result['execution']['results'] = execution_result['results']
            result['execution']['tokens_used'] = execution_result['tokens']
            result['execution']['cost'] = execution_result['cost']
            
            self.stats['total_tokens'] += execution_result['tokens']
            self.stats['total_cost'] += execution_result['cost']
            
            print(f"  ✅ 执行完成")
            print(f"  💰 Token消耗: {execution_result['tokens']}")
            print(f"  💵 费用: ${execution_result['cost']:.4f}")

            # 阶段5: 自我反思
            if self.config['reflection_enabled']:
                print(f"\n阶段5: 自我反思")
                reflection = await self.reflector.reflect(
                    task,
                    subtasks,
                    execution_result['results']
                )
                result['reflection'] = reflection
                self.stats['reflections'] += 1
                print(f"  🧠 反思结果: {reflection['summary']}")
                print(f"  💡 改进建议: {len(reflection['suggestions'])} 条")

            # 阶段6: 结果整合
            print(f"\n阶段6: 结果整合")
            final_output = self._integrate_results(execution_result['results'])
            result['final_output'] = final_output
            print(f"  ✅ 整合完成")

            # 阶段7: 学习进化
            print(f"\n阶段7: 自我学习")
            await self.learner.learn(task, subtasks, execution_result['results'], final_output)
            print(f"  📚 学习完成")

            # 更新统计
            time_taken = time.time() - start_time
            result['execution_time'] = time_taken
            result['success'] = True
            self.stats['successful_tasks'] += 1
            
            if self.stats['total_tasks'] > 0:
                self.stats['avg_task_time'] = (
                    (self.stats['avg_task_time'] * (self.stats['total_tasks'] - 1) + time_taken) 
                    / self.stats['total_tasks']
                )

            print(f"\n{'='*60}")
            print(f"✅ 任务完成!")
            print(f"{'='*60}")
            print(f"  ⏱️  耗时: {time_taken:.2f}秒")
            print(f"  💰 Token: {execution_result['tokens']}")
            print(f"  💵 费用: ${execution_result['cost']:.4f}")
            print(f"  🚀 优化: {len(result['optimizations'])}次")
            print(f"{'='*60}\n")

        except Exception as e:
            result['error'] = str(e)
            self.stats['failed_tasks'] += 1
            print(f"\n❌ 任务失败: {e}")
            import traceback
            traceback.print_exc()

        return result

    async def _execute_with_monitoring(self, subtasks: List[Dict]) -> Dict[str, Any]:
        """执行任务并实时监控"""
        results = []
        total_tokens = 0
        total_cost = 0.0
        
        # 分离并行和顺序任务
        parallel_tasks = [t for t in subtasks if t.get('execution_type') == 'parallel']
        sequential_tasks = [t for t in subtasks if t.get('execution_type') != 'parallel']
        
        # 执行顺序任务
        for i, task in enumerate(sequential_tasks, 1):
            print(f"  📌 执行顺序任务 {i}/{len(sequential_tasks)}...")
            result = await self.executor.execute(task)
            results.append(result)
            total_tokens += result.get('tokens', 0)
            total_cost += self.cost_tracker.calculate_cost(result.get('tokens', 0))
        
        # 并行执行独立任务
        if parallel_tasks and self.config['parallel_execution']:
            print(f"  ⚡ 并行执行 {len(parallel_tasks)} 个任务...")
            batch_results = await asyncio.gather(*[
                self.executor.execute(task) for task in parallel_tasks
            ])
            results.extend(batch_results)
            for r in batch_results:
                total_tokens += r.get('tokens', 0)
                total_cost += self.cost_tracker.calculate_cost(r.get('tokens', 0))
        
        return {
            'results': results,
            'tokens': total_tokens,
            'cost': total_cost
        }

    def _integrate_results(self, results: List[Dict]) -> str:
        """整合多个子任务的结果"""
        integrated = []
        for i, result in enumerate(results, 1):
            if result.get('success'):
                integrated.append(f"[子任务{i}] {result.get('output', '')}")
            else:
                integrated.append(f"[子任务{i}] ❌ {result.get('error', 'Unknown')}")
        return "\n\n".join(integrated)

    async def self_improve(self) -> List[Dict]:
        """自我迭代优化"""
        print("\n🔄 开始自我迭代优化...")
        
        improvements = []
        
        # 分析Token使用效率
        if self.stats['total_tokens'] > 0:
            avg_tokens = self.stats['total_tokens'] / self.stats['total_tasks']
            if avg_tokens > 5000:
                improvements.append({
                    'type': 'token_optimization',
                    'suggestion': '考虑使用更简洁的prompt和上下文压缩',
                    'potential_savings': f'{int(avg_tokens * 0.2)} tokens'
                })
        
        # 分析执行时间
        if self.stats['avg_task_time'] > 30:
            improvements.append({
                'type': 'performance',
                'suggestion': '增加并行执行优化',
                'potential_savings': f'{int(self.stats["avg_task_time"] * 0.3)} 秒'
            })
        
        # 分析成本
        if self.stats['total_cost'] > 1.0:
            improvements.append({
                'type': 'cost_optimization',
                'suggestion': '考虑使用更便宜的模型或优化Token',
                'potential_savings': f'${self.stats["total_cost"] * 0.2:.2f}'
            })
        
        print(f"  💡 发现 {len(improvements)} 个优化空间")
        for imp in improvements:
            print(f"    - {imp['suggestion']}")
        
        self.stats['optimizations'] += len(improvements)
        return improvements

    def get_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        return {
            **self.stats,
            'success_rate': (
                self.stats['successful_tasks'] / self.stats['total_tasks'] 
                if self.stats['total_tasks'] > 0 else 0
            ),
            'learned_patterns': len(self.learned_patterns),
            'cost_efficiency': (
                self.stats['total_tokens'] / self.stats['total_cost'] 
                if self.stats['total_cost'] > 0 else 0
            )
        }

    async def run_interactive(self):
        """交互模式"""
        print("\n" + "="*60)
        print("🤖 Multi-Agent System v2.0 - 交互模式")
        print("="*60)
        print("\n命令:")
        print("  - 输入任务，系统自动分配Agent处理")
        print("  - 'stats' - 查看统计信息")
        print("  - 'improve' - 触发自我优化")
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
                
                await self.process_task(cmd)
                
            except KeyboardInterrupt:
                print("\n\n👋 退出中...")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")


async def main():
    """主函数"""
    system = MultiAgentSystemV2()
    
    if len(__import__('sys').argv) > 1:
        task = ' '.join(__import__('sys').argv[1:])
        result = await system.process_task(task)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        await system.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
