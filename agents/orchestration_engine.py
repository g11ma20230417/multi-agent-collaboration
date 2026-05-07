#!/usr/bin/env python3
"""
Orchestration Engine - 自动协作引擎
负责任务的自动分配、调度和协调
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict

from agents.agent_factory import AgentFactory
from agents.task_decomposer import TaskDecomposer
from agents.executor import ExecutorAgent


class OrchestrationEngine:
    """
    协作引擎 - 自动协调多Agent工作
    
    功能:
    1. 分析任务需求
    2. 自动创建/分配Agent
    3. 动态任务分配
    4. 监控执行进度
    5. 结果整合
    """

    def __init__(self):
        self.agent_factory = AgentFactory()
        self.task_decomposer = TaskDecomposer()
        self.executor = ExecutorAgent()
        
        # 任务队列
        self.task_queue = []
        
        # 执行中的任务
        self.active_tasks = {}
        
        # 完成的任务
        self.completed_tasks = []
        
        # Agent工作负载
        self.agent_workload = defaultdict(int)
        
        # 配置
        self.config = {
            'max_concurrent_tasks': 5,
            'agent_idle_timeout': 300,  # 秒
            'task_priority_levels': ['high', 'medium', 'low']
        }

    async def orchestrate(self, task: str) -> Dict[str, Any]:
        """
        编排任务执行
        
        Args:
            task: 用户任务
            
        Returns:
            执行结果
        """
        print(f"\n🎭 协作引擎启动...")
        
        result = {
            'success': False,
            'task': task,
            'subtasks': [],
            'agents_created': [],
            'assignments': [],
            'results': {},
            'error': None
        }
        
        try:
            # 步骤1: 任务分解
            print(f"  📋 分解任务...")
            subtasks = await self.task_decomposer.decompose(task)
            result['subtasks'] = subtasks
            
            # 步骤2: 分析需要的Agent类型
            print(f"  🤖 分析所需Agent...")
            required_agents = self._analyze_required_agents(subtasks)
            result['agents_needed'] = required_agents
            
            # 步骤3: 创建/分配Agent
            print(f"  🔧 创建/分配Agent...")
            agent_assignments = await self._allocate_agents(subtasks, required_agents)
            result['assignments'] = agent_assignments
            result['agents_created'] = list(set(a['agent_id'] for a in agent_assignments.values()))
            
            # 步骤4: 执行任务
            print(f"  ⚡ 开始执行...")
            execution_results = await self._execute_with_agents(subtasks, agent_assignments)
            result['results'] = execution_results
            
            # 步骤5: 整合结果
            print(f"  🔗 整合结果...")
            final_result = self._integrate_results(execution_results)
            result['final_output'] = final_result
            
            result['success'] = True
            
            # 清理Agent
            self._cleanup_agents()
            
            print(f"  ✅ 编排完成!")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ 编排失败: {e}")
        
        return result

    def _analyze_required_agents(self, subtasks: List[Dict]) -> Dict[str, int]:
        """
        分析任务需要的Agent类型和数量
        
        Returns:
            {agent_type: count}
        """
        required = defaultdict(int)
        
        for subtask in subtasks:
            task_type = subtask.get('type', 'implementation')
            
            # 根据任务类型映射到Agent类型
            agent_mapping = {
                'analysis': 'analyst',
                'design': 'designer',
                'backend': 'coder',
                'frontend': 'coder',
                'testing': 'tester',
                'research': 'researcher',
                'integration': 'devops',
                'planning': 'planner',
                'response': 'writer',
                'implementation': 'coder'
            }
            
            agent_type = agent_mapping.get(task_type, 'coder')
            required[agent_type] += 1
        
        return dict(required)

    async def _allocate_agents(self, subtasks: List[Dict], 
                              required: Dict[str, int]) -> Dict[int, Dict]:
        """
        为每个子任务分配Agent
        
        Returns:
            {subtask_id: {agent_id, agent_type, agent_name}}
        """
        assignments = {}
        
        for subtask in subtasks:
            task_type = subtask.get('type', 'implementation')
            
            # 根据任务类型确定Agent类型
            agent_mapping = {
                'analysis': 'analyst',
                'design': 'designer',
                'backend': 'coder',
                'frontend': 'coder',
                'testing': 'tester',
                'research': 'researcher',
                'integration': 'devops',
                'planning': 'planner',
                'response': 'writer',
                'implementation': 'coder'
            }
            
            agent_type = agent_mapping.get(task_type, 'coder')
            
            # 创建Agent
            agent = self.agent_factory.create_agent(agent_type)
            agent_id = agent['id']
            
            # 分配任务
            assignments[subtask['id']] = {
                'agent_id': agent_id,
                'agent_type': agent_type,
                'agent_name': agent['name'],
                'subtask': subtask
            }
            
            # 更新工作负载
            self.agent_workload[agent_id] += 1
            
            print(f"    📌 子任务{subtask['id']} → {agent['name']}")
        
        return assignments

    async def _execute_with_agents(self, subtasks: List[Dict], 
                                  assignments: Dict) -> Dict[int, Any]:
        """
        使用分配的Agent执行任务
        
        Returns:
            {subtask_id: result}
        """
        results = {}
        
        # 分离并行和顺序任务
        parallel_tasks = [t for t in subtasks if t.get('execution_type') == 'parallel']
        sequential_tasks = [t for t in subtasks if t.get('execution_type') != 'parallel']
        
        # 执行顺序任务
        for subtask in sequential_tasks:
            assignment = assignments.get(subtask['id'])
            if assignment:
                agent_id = assignment['agent_id']
                result = await self.executor.execute(subtask)
                results[subtask['id']] = result
                
                # 更新Agent统计
                self.agent_factory.update_agent_stats(agent_id, result.get('success', False))
        
        # 并行执行独立任务
        if parallel_tasks:
            tasks_to_run = []
            for subtask in parallel_tasks:
                assignment = assignments.get(subtask['id'])
                if assignment:
                    tasks_to_run.append(
                        self._execute_single_task(subtask, assignment)
                    )
            
            if tasks_to_run:
                batch_results = await asyncio.gather(*tasks_to_run)
                for i, result in enumerate(batch_results):
                    if i < len(parallel_tasks):
                        results[parallel_tasks[i]['id']] = result
        
        return results

    async def _execute_single_task(self, subtask: Dict, assignment: Dict) -> Dict:
        """执行单个任务"""
        agent_id = assignment['agent_id']
        
        # 获取Agent信息
        agent = self.agent_factory.get_agent(agent_id)
        
        print(f"    🤖 {agent['name']} 执行子任务{subtask['id']}...")
        
        # 执行任务
        result = await self.executor.execute(subtask)
        
        # 更新统计
        self.agent_factory.update_agent_stats(agent_id, result.get('success', False))
        
        return result

    def _integrate_results(self, results: Dict[int, Any]) -> str:
        """整合所有结果"""
        outputs = []
        
        for subtask_id in sorted(results.keys()):
            result = results[subtask_id]
            if result.get('success'):
                outputs.append(f"[任务{subtask_id}] {result.get('output', '')}")
            else:
                outputs.append(f"[任务{subtask_id}] ❌ {result.get('error', 'Unknown')}")
        
        return "\n\n".join(outputs)

    def _cleanup_agents(self):
        """清理不需要的Agent"""
        # 移除工作负载为0的Agent
        agents_to_remove = [
            agent_id for agent_id, workload in self.agent_workload.items()
            if workload == 0
        ]
        
        for agent_id in agents_to_remove:
            self.agent_factory.remove_agent(agent_id)
            self.agent_workload.pop(agent_id, None)
        
        if agents_to_remove:
            print(f"  🧹 清理了 {len(agents_to_remove)} 个Agent")

    def get_orchestration_stats(self) -> Dict[str, Any]:
        """获取编排统计"""
        return {
            'total_agents_created': len(self.agent_factory.created_agents),
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'agent_workload': dict(self.agent_workload),
            'factory_stats': self.agent_factory.get_factory_stats()
        }

    async def run_demo(self):
        """运行演示"""
        print("\n" + "="*60)
        print("🎭 协作引擎演示")
        print("="*60)
        
        demo_tasks = [
            "创建一个完整的博客系统",
            "分析竞争对手的市场策略",
            "开发一个数据可视化仪表板"
        ]
        
        for i, task in enumerate(demo_tasks, 1):
            print(f"\n{'='*60}")
            print(f"演示 {i}/3: {task}")
            print('='*60)
            
            result = await self.orchestrate(task)
            
            print(f"\n📊 统计:")
            print(f"  创建的Agent: {result['agents_created']}")
            print(f"  任务分配: {len(result['assignments'])} 个")
            print(f"  成功率: {sum(1 for r in result['results'].values() if r.get('success'))}/{len(result['results'])}")
        
        print(f"\n{'='*60}")
        print("🎉 演示完成!")
        print('='*60)
