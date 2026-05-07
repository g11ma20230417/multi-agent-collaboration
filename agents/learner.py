#!/usr/bin/env python3
"""
学习Agent
从历史任务中学习，自动优化执行策略
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime


class LearnerAgent:
    """学习Agent，负责从历史中学习和进化"""

    def __init__(self):
        self.learned_patterns = []
        self.execution_history = []
        self.load_history()

    def load_history(self):
        """加载历史学习数据"""
        history_file = Path("./data/learning_history.json")
        if history_file.exists():
            try:
                import json
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learned_patterns = data.get('patterns', [])
                    self.execution_history = data.get('history', [])
            except:
                pass

    def save_history(self):
        """保存学习数据"""
        history_file = Path("./data/learning_history.json")
        history_file.parent.mkdir(exist_ok=True)
        
        import json
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'patterns': self.learned_patterns,
                'history': self.execution_history[-100:]  # 只保留最近100条
            }, f, ensure_ascii=False, indent=2)

    async def learn(self, original_task: str, subtasks: List[Dict], 
                   results: List[Dict], final_result: str):
        """
        从任务执行中学习
        
        Args:
            original_task: 原始任务
            subtasks: 子任务列表
            results: 执行结果
            final_result: 最终结果
        """
        print(f"      📚 分析学习点...")
        
        # 分析成功的模式
        successful_patterns = self._extract_patterns(subtasks, results)
        
        # 分析Token使用效率
        token_efficiency = self._analyze_token_efficiency(results)
        
        # 分析执行效率
        execution_efficiency = self._analyze_execution_efficiency(results)
        
        # 更新学习数据
        for pattern in successful_patterns:
            self._update_pattern(pattern)
        
        # 保存历史
        self.execution_history.append({
            'task': original_task,
            'timestamp': datetime.now().isoformat(),
            'subtasks': len(subtasks),
            'successful': sum(1 for r in results if r.get('success')),
            'tokens': sum(r.get('tokens', 0) for r in results),
            'time': sum(r.get('time', 0) for r in results)
        })
        
        # 定期保存
        if len(self.execution_history) % 5 == 0:
            self.save_history()
        
        print(f"      ✅ 学习完成，已掌握 {len(self.learned_patterns)} 个模式")

    def _extract_patterns(self, subtasks: List[Dict], results: List[Dict]) -> List[Dict]:
        """提取成功的执行模式"""
        patterns = []
        
        for task, result in zip(subtasks, results):
            if result.get('success'):
                pattern = {
                    'task_type': task['type'],
                    'strategy': self._determine_strategy(task, result),
                    'success_rate': 1.0,
                    'avg_tokens': result.get('tokens', 0),
                    'avg_time': result.get('time', 0)
                }
                patterns.append(pattern)
        
        return patterns

    def _determine_strategy(self, task: Dict, result: Dict) -> str:
        """确定最佳策略"""
        tokens = result.get('tokens', 0)
        time_taken = result.get('time', 0)
        
        if time_taken > 2 and tokens > 500:
            return "高效完整策略"
        elif tokens > 800:
            return "精简高效策略"
        elif time_taken > 3:
            return "速度优先策略"
        else:
            return "平衡策略"

    def _analyze_token_efficiency(self, results: List[Dict]) -> Dict[str, Any]:
        """分析Token使用效率"""
        total_tokens = sum(r.get('tokens', 0) for r in results)
        total_output = sum(len(r.get('output', '')) for r in results)
        
        return {
            'total_tokens': total_tokens,
            'avg_tokens': total_tokens / len(results) if results else 0,
            'efficiency': total_output / total_tokens if total_tokens > 0 else 0,
            'can_optimize': total_tokens > 1000
        }

    def _analyze_execution_efficiency(self, results: List[Dict]) -> Dict[str, Any]:
        """分析执行效率"""
        total_time = sum(r.get('time', 0) for r in results)
        successful = sum(1 for r in results if r.get('success'))
        
        return {
            'total_time': total_time,
            'avg_time': total_time / len(results) if results else 0,
            'success_rate': successful / len(results) if results else 0,
            'can_optimize': total_time > 10
        }

    def _update_pattern(self, pattern: Dict):
        """更新学习到的模式"""
        # 检查是否已存在类似模式
        for existing in self.learned_patterns:
            if existing['task_type'] == pattern['task_type']:
                # 更新现有模式
                existing['success_rate'] = (existing['success_rate'] + pattern['success_rate']) / 2
                existing['avg_tokens'] = (existing['avg_tokens'] + pattern['avg_tokens']) / 2
                existing['avg_time'] = (existing['avg_time'] + pattern['avg_time']) / 2
                return
        
        # 添加新模式
        self.learned_patterns.append(pattern)

    def find_best_pattern(self, task: Dict) -> Optional[Dict]:
        """查找最佳匹配的模式"""
        task_type = task.get('type', '')
        
        best = None
        best_score = 0
        
        for pattern in self.learned_patterns:
            if pattern['task_type'] == task_type:
                # 计算综合得分
                score = pattern['success_rate'] * 100 - pattern['avg_tokens'] / 10
                if score > best_score:
                    best_score = score
                    best = pattern
        
        return best

    def apply_pattern(self, task: Dict, pattern: Dict) -> Dict:
        """应用学习到的模式优化任务"""
        # 根据模式调整任务参数
        optimized = task.copy()
        
        if pattern['strategy'] == "精简高效策略":
            optimized['priority'] = 'medium'
        elif pattern['strategy'] == "速度优先策略":
            optimized['execution_type'] = 'parallel'
        
        return optimized

    async def analyze_history(self) -> Dict[str, Any]:
        """分析历史数据，寻找优化空间"""
        if len(self.execution_history) < 5:
            return {
                'status': 'insufficient_data',
                'message': '需要更多历史数据才能进行分析'
            }
        
        # 分析任务类型分布
        from collections import Counter
        task_types = Counter(e['task'] for e in self.execution_history[-20:])
        
        # 分析成功率趋势
        recent_success = sum(
            e['successful'] / e['subtasks'] 
            for e in self.execution_history[-10:]
        ) / 10
        
        # 分析Token消耗趋势
        recent_tokens = sum(e['tokens'] for e in self.execution_history[-10:]) / 10
        
        return {
            'status': 'analyzed',
            'total_tasks': len(self.execution_history),
            'common_tasks': task_types.most_common(5),
            'recent_success_rate': recent_success,
            'recent_avg_tokens': recent_tokens,
            'learned_patterns_count': len(self.learned_patterns),
            'recommendations': self._generate_recommendations(recent_success, recent_tokens)
        }

    def _generate_recommendations(self, success_rate: float, avg_tokens: int) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if success_rate < 0.8:
            recommendations.append("任务成功率偏低，考虑增加错误处理")
        
        if avg_tokens > 1000:
            recommendations.append("Token消耗较高，考虑使用更简洁的prompt")
        
        if len(self.learned_patterns) < 5:
            recommendations.append("学习模式较少，建议多样化任务类型")
        
        return recommendations

    def get_learning_stats(self) -> Dict[str, Any]:
        """获取学习统计"""
        return {
            'total_patterns': len(self.learned_patterns),
            'total_history': len(self.execution_history),
            'pattern_types': list(set(p['task_type'] for p in self.learned_patterns))
        }
