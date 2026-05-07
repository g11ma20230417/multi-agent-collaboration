#!/usr/bin/env python3
"""
Multi-Agent Collaboration System
多Agent协同工作系统
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"

from .agents.task_decomposer import TaskDecomposer
from .agents.executor import ExecutorAgent
from .agents.optimizer import OptimizerAgent
from .agents.learner import LearnerAgent
from .core.token_optimizer import TokenOptimizer
from .core.knowledge_base import KnowledgeBase

__all__ = [
    'TaskDecomposer',
    'ExecutorAgent',
    'OptimizerAgent',
    'LearnerAgent',
    'TokenOptimizer',
    'KnowledgeBase'
]
