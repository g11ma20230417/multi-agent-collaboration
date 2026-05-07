#!/usr/bin/env python3
"""
执行Agent
负责任务的实际执行和结果收集
"""

import asyncio
from typing import Dict, Any, List


class ExecutorAgent:
    """执行Agent，负责具体任务执行"""

    def __init__(self):
        self.execution_history = []

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个任务
        
        Args:
            task: 任务字典
            
        Returns:
            执行结果
        """
        print(f"      ⚙️  执行: {task['description'][:30]}...")
        
        result = {
            'task_id': task['id'],
            'task_type': task['type'],
            'description': task['description'],
            'success': False,
            'output': '',
            'tokens': 0,
            'time': 0,
            'can_improve': False,
            'error': None
        }
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # 根据任务类型执行
            if task['type'] == 'analysis':
                result['output'] = await self._execute_analysis(task)
            elif task['type'] == 'design':
                result['output'] = await self._execute_design(task)
            elif task['type'] == 'backend':
                result['output'] = await self._execute_backend(task)
            elif task['type'] == 'frontend':
                result['output'] = await self._execute_frontend(task)
            elif task['type'] == 'integration':
                result['output'] = await self._execute_integration(task)
            elif task['type'] == 'research':
                result['output'] = await self._execute_research(task)
            elif task['type'] == 'response':
                result['output'] = await self._execute_response(task)
            else:
                result['output'] = await self._execute_implementation(task)
            
            result['success'] = True
            result['can_improve'] = self._check_improvement_needed(result['output'])
            
        except Exception as e:
            result['error'] = str(e)
        
        result['time'] = asyncio.get_event_loop().time() - start_time
        result['tokens'] = self._estimate_tokens(result['output'])
        
        # 记录历史
        self.execution_history.append(result)
        
        print(f"      ✅ 完成 (耗时: {result['time']:.2f}s, Token: {result['tokens']})")
        
        return result

    async def _execute_analysis(self, task: Dict) -> str:
        """执行分析任务"""
        await asyncio.sleep(0.3)
        return """
需求分析报告：
1. 用户需求理解
2. 技术可行性评估
3. 资源需求分析
4. 风险评估
        """.strip()

    async def _execute_design(self, task: Dict) -> str:
        """执行设计任务"""
        await asyncio.sleep(0.3)
        return """
系统设计文档：
1. 架构设计
2. 模块划分
3. 接口定义
4. 数据流程
        """.strip()

    async def _execute_backend(self, task: Dict) -> str:
        """执行后端任务"""
        await asyncio.sleep(0.3)
        return """
后端代码实现：
- API接口
- 数据处理逻辑
- 数据库操作
- 业务规则
        """.strip()

    async def _execute_frontend(self, task: Dict) -> str:
        """执行前端任务"""
        await asyncio.sleep(0.3)
        return """
前端代码实现：
- 界面组件
- 用户交互
- 状态管理
- 样式设计
        """.strip()

    async def _execute_integration(self, task: Dict) -> str:
        """执行集成任务"""
        await asyncio.sleep(0.3)
        return """
集成测试报告：
- 单元测试
- 集成测试
- 性能测试
- 优化建议
        """.strip()

    async def _execute_research(self, task: Dict) -> str:
        """执行研究任务"""
        await asyncio.sleep(0.3)
        return """
研究结果：
- 背景调研
- 现状分析
- 最佳实践
- 推荐方案
        """.strip()

    async def _execute_response(self, task: Dict) -> str:
        """执行响应任务"""
        await asyncio.sleep(0.2)
        return f"回答：{task['description']}\n\n这是基于深度思考的详细回答。"

    async def _execute_implementation(self, task: Dict) -> str:
        """执行实现任务"""
        await asyncio.sleep(0.3)
        return f"""
实现：{task['description']}

代码已完成，包含：
- 核心逻辑
- 错误处理
- 性能优化
- 文档注释
        """.strip()

    def _estimate_tokens(self, output: str) -> int:
        """估算Token消耗"""
        # 简单估算：中文约2字符=1Token，英文约4字符=1Token
        chinese_chars = sum(1 for c in output if '\u4e00' <= c <= '\u9fff')
        english_chars = len(output) - chinese_chars
        return int(chinese_chars / 2 + english_chars / 4)

    def _check_improvement_needed(self, output: str) -> bool:
        """检查是否需要优化"""
        # 简单规则：输出太短或包含错误提示
        if len(output) < 50:
            return True
        if '错误' in output or '失败' in output:
            return True
        return False

    async def execute_batch(self, tasks: List[Dict]) -> List[Dict]:
        """
        批量执行任务（支持并行）
        
        Args:
            tasks: 任务列表
            
        Returns:
            结果列表
        """
        # 分离可并行和必须顺序的任务
        parallel_tasks = [t for t in tasks if t.get('execution_type') == 'parallel']
        sequential_tasks = [t for t in tasks if t.get('execution_type') != 'parallel']
        
        results = []
        
        # 先执行顺序任务
        for task in sequential_tasks:
            result = await self.execute(task)
            results.append(result)
        
        # 并行执行独立任务
        if parallel_tasks:
            batch_results = await asyncio.gather(*[
                self.execute(task) for task in parallel_tasks
            ])
            results.extend(batch_results)
        
        return results

    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计"""
        if not self.execution_history:
            return {}
        
        total = len(self.execution_history)
        successful = sum(1 for r in self.execution_history if r['success'])
        total_tokens = sum(r['tokens'] for r in self.execution_history)
        total_time = sum(r['time'] for r in self.execution_history)
        
        return {
            'total_executions': total,
            'successful_executions': successful,
            'success_rate': successful / total if total > 0 else 0,
            'total_tokens': total_tokens,
            'avg_tokens': total_tokens / total if total > 0 else 0,
            'total_time': total_time,
            'avg_time': total_time / total if total > 0 else 0
        }
