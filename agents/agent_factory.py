#!/usr/bin/env python3
"""
Agent Factory - Agent自动生成工厂
根据任务需求自动创建和注册Agent
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json


class AgentFactory:
    """
    Agent工厂 - 动态创建专用Agent
    
    功能:
    1. 根据任务类型自动创建Agent
    2. 动态注册Agent到系统
    3. 管理Agent生命周期
    4. Agent能力匹配
    """

    def __init__(self):
        # Agent模板库
        self.agent_templates = self._load_templates()
        
        # 已创建的Agent
        self.created_agents = {}
        
        # Agent能力注册表
        self.capability_registry = {}
        
    def _load_templates(self) -> Dict[str, Any]:
        """加载Agent模板"""
        return {
            'coder': {
                'name': '程序员Agent',
                'role': '代码开发',
                'capabilities': ['代码生成', '代码审查', '调试', '重构'],
                'tools': ['代码编辑器', '编译器', '调试器'],
                'system_prompt': '你是一个专业的程序员，擅长编写高质量代码。'
            },
            'researcher': {
                'name': '研究员Agent',
                'role': '信息收集与分析',
                'capabilities': ['搜索', '分析', '总结', '报告撰写'],
                'tools': ['搜索引擎', '数据库', '分析工具'],
                'system_prompt': '你是一个专业的研究员，擅长收集和分析信息。'
            },
            'tester': {
                'name': '测试员Agent',
                'role': '质量保证',
                'capabilities': ['测试设计', '缺陷发现', '性能测试', '自动化测试'],
                'tools': ['测试框架', '性能工具', '监控系统'],
                'system_prompt': '你是一个专业的测试工程师，确保产品质量。'
            },
            'designer': {
                'name': '设计师Agent',
                'role': '界面与架构设计',
                'capabilities': ['UI设计', 'UX设计', '架构设计', '原型制作'],
                'tools': ['设计工具', '原型工具', '文档工具'],
                'system_prompt': '你是一个专业的设计师，创造优秀的用户体验。'
            },
            'planner': {
                'name': '规划师Agent',
                'role': '任务规划与协调',
                'capabilities': ['任务分解', '资源规划', '进度跟踪', '风险评估'],
                'tools': ['项目管理工具', '日历', '提醒系统'],
                'system_prompt': '你是一个专业的项目经理，擅长规划和协调任务。'
            },
            'analyst': {
                'name': '分析师Agent',
                'role': '数据分析与洞察',
                'capabilities': ['数据收集', '统计分析', '可视化', '洞察发现'],
                'tools': ['数据分析工具', '可视化库', '报表工具'],
                'system_prompt': '你是一个专业的数据分析师，擅长从数据中发现洞察。'
            },
            'writer': {
                'name': '写手Agent',
                'role': '内容创作',
                'capabilities': ['文章撰写', '文档编写', '文案创作', '校对编辑'],
                'tools': ['写作工具', '语法检查', '翻译工具'],
                'system_prompt': '你是一个专业的内容创作者，写出清晰、有吸引力的内容。'
            },
            'devops': {
                'name': '运维Agent',
                'role': '部署与运维',
                'capabilities': ['自动化部署', '监控告警', '日志分析', '故障排除'],
                'tools': ['CI/CD工具', '监控平台', '日志系统'],
                'system_prompt': '你是一个专业的DevOps工程师，确保系统稳定运行。'
            }
        }

    def create_agent(self, task_type: str, custom_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        根据任务类型创建Agent
        
        Args:
            task_type: 任务类型 (如 'coder', 'researcher' 等)
            custom_config: 自定义配置
            
        Returns:
            创建的Agent配置
        """
        # 查找匹配的模板
        template = self._find_matching_template(task_type)
        
        if not template:
            # 创建通用Agent
            template = self._create_generic_agent(task_type)
        
        # 生成Agent ID
        agent_id = self._generate_agent_id(template['role'])
        
        # 创建Agent实例
        agent = {
            'id': agent_id,
            'name': template['name'],
            'role': template['role'],
            'capabilities': template['capabilities'],
            'tools': template['tools'],
            'system_prompt': template['system_prompt'],
            'status': 'ready',
            'task_count': 0,
            'success_rate': 0.0
        }
        
        # 应用自定义配置
        if custom_config:
            agent.update(custom_config)
        
        # 注册到系统
        self.created_agents[agent_id] = agent
        self._register_capabilities(agent)
        
        return agent

    def _find_matching_template(self, task_type: str) -> Optional[Dict]:
        """查找匹配的模板"""
        task_lower = task_type.lower()
        
        # 关键词匹配
        matches = {
            'code': 'coder',
            '编程': 'coder',
            '开发': 'coder',
            'research': 'researcher',
            '研究': 'researcher',
            '搜索': 'researcher',
            'test': 'tester',
            '测试': 'tester',
            'design': 'designer',
            '设计': 'designer',
            'plan': 'planner',
            '规划': 'planner',
            '分析': 'analyst',
            'data': 'analyst',
            'write': 'writer',
            '写作': 'writer',
            'deploy': 'devops',
            '运维': 'devops'
        }
        
        template_key = None
        for keyword, template in matches.items():
            if keyword in task_lower:
                template_key = template
                break
        
        if template_key and template_key in self.agent_templates:
            return self.agent_templates[template_key]
        
        return None

    def _create_generic_agent(self, task_type: str) -> Dict:
        """创建通用Agent"""
        return {
            'name': f'通用{task_type}Agent',
            'role': task_type,
            'capabilities': ['任务执行', '问题解决'],
            'tools': ['通用工具'],
            'system_prompt': f'你是一个{task_type}专家，能够处理各种相关任务。'
        }

    def _generate_agent_id(self, role: str) -> str:
        """生成唯一的Agent ID"""
        import hashlib
        from datetime import datetime
        
        timestamp = datetime.now().isoformat()
        hash_input = f"{role}_{timestamp}"
        hash_id = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        
        return f"agent_{role}_{hash_id}"

    def _register_capabilities(self, agent: Dict):
        """注册Agent能力"""
        for capability in agent['capabilities']:
            if capability not in self.capability_registry:
                self.capability_registry[capability] = []
            self.capability_registry[capability].append(agent['id'])

    def find_best_agent(self, required_capabilities: List[str]) -> Optional[str]:
        """
        根据所需能力找到最佳Agent
        
        Args:
            required_capabilities: 所需能力列表
            
        Returns:
            最佳Agent ID
        """
        if not required_capabilities:
            return None
        
        # 统计每个Agent匹配的能力数
        agent_scores = {}
        
        for capability in required_capabilities:
            if capability in self.capability_registry:
                for agent_id in self.capability_registry[capability]:
                    agent_scores[agent_id] = agent_scores.get(agent_id, 0) + 1
        
        if not agent_scores:
            return None
        
        # 返回匹配度最高的Agent
        best_agent = max(agent_scores, key=agent_scores.get)
        
        # 检查是否完全匹配
        if agent_scores[best_agent] == len(required_capabilities):
            return best_agent
        
        # 返回匹配最多的Agent
        return best_agent

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """获取Agent信息"""
        return self.created_agents.get(agent_id)

    def list_agents(self) -> List[Dict]:
        """列出所有Agent"""
        return list(self.created_agents.values())

    def update_agent_stats(self, agent_id: str, success: bool):
        """更新Agent统计"""
        if agent_id in self.created_agents:
            agent = self.created_agents[agent_id]
            agent['task_count'] += 1
            
            # 更新成功率
            if success:
                prev_rate = agent['success_rate']
                prev_count = agent['task_count'] - 1
                agent['success_rate'] = (prev_rate * prev_count + 1) / agent['task_count']

    def remove_agent(self, agent_id: str) -> bool:
        """移除Agent"""
        if agent_id in self.created_agents:
            agent = self.created_agents.pop(agent_id)
            
            # 从能力注册表移除
            for capability, agents in self.capability_registry.items():
                if agent_id in agents:
                    agents.remove(agent_id)
            
            return True
        return False

    def get_factory_stats(self) -> Dict[str, Any]:
        """获取工厂统计"""
        total_agents = len(self.created_agents)
        total_capabilities = len(self.capability_registry)
        
        return {
            'total_agents': total_agents,
            'total_capabilities': total_capabilities,
            'available_templates': len(self.agent_templates),
            'agents': self.list_agents()
        }

    def export_config(self) -> Dict:
        """导出Agent配置"""
        return {
            'templates': self.agent_templates,
            'created_agents': self.created_agents,
            'capability_registry': self.capability_registry
        }

    def import_config(self, config: Dict):
        """导入Agent配置"""
        if 'templates' in config:
            self.agent_templates.update(config['templates'])
        if 'created_agents' in config:
            self.created_agents.update(config['created_agents'])
        if 'capability_registry' in config:
            self.capability_registry.update(config['capability_registry'])
