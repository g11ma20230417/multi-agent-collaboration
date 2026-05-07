#!/usr/bin/env python3
"""
知识库
存储和管理学习到的模式与优化策略
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class KnowledgeBase:
    """知识库Agent，负责存储和管理知识"""

    def __init__(self):
        self.base_dir = Path("./data/knowledge_base")
        self.base_dir.mkdir(exist_ok=True, parents=True)
        
        self.patterns_file = self.base_dir / "patterns.json"
        self.workflows_file = self.base_dir / "workflows.json"
        self.metrics_file = self.base_dir / "metrics.json"
        
        self.load_data()

    def load_data(self):
        """加载知识库数据"""
        self.patterns = self._load_json(self.patterns_file, [])
        self.workflows = self._load_json(self.workflows_file, [])
        self.metrics = self._load_json(self.metrics_file, {
            'total_tasks': 0,
            'successful_tasks': 0,
            'total_tokens': 0,
            'avg_task_time': 0,
            'last_updated': None
        })

    def _load_json(self, file_path: Path, default):
        """加载JSON文件"""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default

    def _save_json(self, file_path: Path, data):
        """保存JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_pattern(self, pattern: Dict[str, Any]):
        """
        添加学习到的模式
        
        Args:
            pattern: 模式字典
        """
        # 检查是否已存在
        for i, existing in enumerate(self.patterns):
            if existing.get('name') == pattern.get('name'):
                # 更新现有模式
                self.patterns[i] = {**existing, **pattern, 'updated': datetime.now().isoformat()}
                self._save_json(self.patterns_file, self.patterns)
                return
        
        # 添加新模式
        pattern['created'] = datetime.now().isoformat()
        pattern['updated'] = datetime.now().isoformat()
        self.patterns.append(pattern)
        self._save_json(self.patterns_file, self.patterns)

    def get_patterns(self) -> List[Dict[str, Any]]:
        """获取所有模式"""
        return self.patterns

    def get_pattern_by_name(self, name: str) -> Dict[str, Any]:
        """按名称获取模式"""
        for pattern in self.patterns:
            if pattern.get('name') == name:
                return pattern
        return None

    def get_patterns_by_type(self, pattern_type: str) -> List[Dict[str, Any]]:
        """按类型获取模式"""
        return [p for p in self.patterns if p.get('type') == pattern_type]

    def add_workflow(self, workflow: Dict[str, Any]):
        """
        添加工作流
        
        Args:
            workflow: 工作流字典
        """
        workflow['created'] = datetime.now().isoformat()
        workflow['times_used'] = 0
        workflow['success_rate'] = 0
        
        self.workflows.append(workflow)
        self._save_json(self.workflows_file, self.workflows)

    def get_workflows(self) -> List[Dict[str, Any]]:
        """获取所有工作流"""
        return self.workflows

    def get_best_workflow(self, task_type: str) -> Dict[str, Any]:
        """获取最佳工作流"""
        best = None
        best_score = 0
        
        for workflow in self.workflows:
            if workflow.get('task_type') == task_type:
                score = workflow.get('success_rate', 0) * workflow.get('times_used', 0)
                if score > best_score:
                    best_score = score
                    best = workflow
        
        return best

    def update_workflow_stats(self, workflow_name: str, success: bool):
        """更新工作流统计"""
        for workflow in self.workflows:
            if workflow.get('name') == workflow_name:
                workflow['times_used'] = workflow.get('times_used', 0) + 1
                
                # 更新成功率
                total = workflow['times_used']
                prev_success = workflow.get('success_rate', 0) * (total - 1)
                workflow['success_rate'] = (prev_success + (1 if success else 0)) / total
                
                self._save_json(self.workflows_file, self.workflows)
                return

    def update_metrics(self, tokens: int, time_taken: float, success: bool):
        """更新系统指标"""
        self.metrics['total_tasks'] += 1
        if success:
            self.metrics['successful_tasks'] += 1
        self.metrics['total_tokens'] += tokens
        
        # 更新平均时间
        total = self.metrics['total_tasks']
        prev_time = self.metrics.get('avg_task_time', 0)
        self.metrics['avg_task_time'] = (prev_time * (total - 1) + time_taken) / total
        self.metrics['last_updated'] = datetime.now().isoformat()
        
        self._save_json(self.metrics_file, self.metrics)

    def get_metrics(self) -> Dict[str, Any]:
        """获取系统指标"""
        metrics = self.metrics.copy()
        if metrics['total_tasks'] > 0:
            metrics['success_rate'] = metrics['successful_tasks'] / metrics['total_tasks']
        return metrics

    def search_knowledge(self, query: str) -> Dict[str, Any]:
        """
        搜索知识库
        
        Args:
            query: 搜索关键词
            
        Returns:
            搜索结果
        """
        results = {
            'patterns': [],
            'workflows': [],
            'metrics': None
        }
        
        # 搜索模式
        query_lower = query.lower()
        for pattern in self.patterns:
            if (query_lower in pattern.get('name', '').lower() or
                query_lower in pattern.get('description', '').lower()):
                results['patterns'].append(pattern)
        
        # 搜索工作流
        for workflow in self.workflows:
            if (query_lower in workflow.get('name', '').lower() or
                query_lower in workflow.get('description', '').lower()):
                results['workflows'].append(workflow)
        
        # 返回指标摘要
        results['metrics'] = self.get_metrics()
        
        return results

    def export_knowledge(self) -> Dict[str, Any]:
        """导出知识库"""
        return {
            'patterns': self.patterns,
            'workflows': self.workflows,
            'metrics': self.metrics,
            'export_time': datetime.now().isoformat()
        }

    def import_knowledge(self, data: Dict[str, Any]):
        """导入知识库"""
        if 'patterns' in data:
            self.patterns.extend(data['patterns'])
            self._save_json(self.patterns_file, self.patterns)
        
        if 'workflows' in data:
            self.workflows.extend(data['workflows'])
            self._save_json(self.workflows_file, self.workflows)

    def clear_old_data(self, days: int = 30):
        """清理旧数据"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        # 清理旧模式
        self.patterns = [
            p for p in self.patterns 
            if datetime.fromisoformat(p.get('updated', '2000-01-01')).timestamp() > cutoff
        ]
        self._save_json(self.patterns_file, self.patterns)
        
        # 清理旧工作流
        self.workflows = [
            w for w in self.workflows 
            if datetime.fromisoformat(w.get('created', '2000-01-01')).timestamp() > cutoff
        ]
        self._save_json(self.workflows_file, self.workflows)
