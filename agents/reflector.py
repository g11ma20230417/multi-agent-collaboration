#!/usr/bin/env python3
"""
Reflector Agent - 自我反思机制
基于 AutoGPT 的反思模式
"""

import asyncio
from typing import Dict, Any, List


class ReflectorAgent:
    """
    Reflector Agent - 自我反思器
    
    职责:
    1. 评估执行结果质量
    2. 识别潜在问题
    3. 提出改进建议
    4. 决定是否需要重试
    5. 总结经验教训
    """

    def __init__(self):
        self.quality_thresholds = {
            'min_output_length': 50,
            'min_success_rate': 0.7,
            'max_error_rate': 0.3
        }

    async def reflect(self, task: str, subtasks: List[Dict], 
                    results: List[Dict]) -> Dict[str, Any]:
        """
        反思执行过程和结果
        
        Args:
            task: 原始任务
            subtasks: 子任务列表
            results: 执行结果
            
        Returns:
            反思结果
        """
        print(f"  🧠 进行自我反思...")
        
        # 评估质量
        quality_assessment = self._assess_quality(task, subtasks, results)
        
        # 识别问题
        issues = self._identify_issues(results)
        
        # 生成建议
        suggestions = self._generate_suggestions(quality_assessment, issues)
        
        # 判断是否需要重试
        needs_retry = self._check_retry_needed(quality_assessment, issues)
        
        # 总结
        summary = self._generate_summary(quality_assessment, issues)
        
        return {
            'quality': quality_assessment,
            'issues': issues,
            'suggestions': suggestions,
            'needs_retry': needs_retry,
            'retry_reason': issues[0] if needs_retry and issues else None,
            'summary': summary
        }

    def _assess_quality(self, task: str, subtasks: List[Dict], 
                       results: List[Dict]) -> Dict[str, Any]:
        """评估结果质量"""
        # 计算成功率
        total = len(results)
        successful = sum(1 for r in results if r.get('success'))
        success_rate = successful / total if total > 0 else 0
        
        # 计算平均Token效率
        avg_tokens = sum(r.get('tokens', 0) for r in results) / total if total > 0 else 0
        
        # 检查输出质量
        output_lengths = [len(r.get('output', '')) for r in results if r.get('success')]
        avg_output_length = sum(output_lengths) / len(output_lengths) if output_lengths else 0
        
        # 识别问题
        issues = self._identify_issues(results)
        
        # 综合评分
        quality_score = 0
        if success_rate >= 0.8:
            quality_score += 40
        elif success_rate >= 0.6:
            quality_score += 25
        
        if avg_output_length >= self.quality_thresholds['min_output_length']:
            quality_score += 30
        
        if len(issues) == 0:
            quality_score += 30
        
        return {
            'success_rate': success_rate,
            'avg_tokens': avg_tokens,
            'avg_output_length': avg_output_length,
            'quality_score': quality_score,
            'quality_level': self._get_quality_level(quality_score)
        }

    def _identify_issues(self, results: List[Dict]) -> List[str]:
        """识别问题"""
        issues = []
        
        # 检查失败的任务
        failed = [r for r in results if not r.get('success')]
        if failed:
            issues.append(f"有 {len(failed)} 个子任务失败")
        
        # 检查Token消耗
        high_token_tasks = [r for r in results if r.get('tokens', 0) > 1000]
        if high_token_tasks:
            issues.append(f"{len(high_token_tasks)} 个任务Token消耗过高")
        
        # 检查输出长度
        short_outputs = [r for r in results if len(r.get('output', '')) < 50]
        if short_outputs:
            issues.append(f"{len(short_outputs)} 个输出内容过少")
        
        # 检查错误信息
        errors = [r.get('error') for r in results if r.get('error')]
        if errors:
            unique_errors = set(errors)
            issues.append(f"发现 {len(unique_errors)} 种不同错误")
        
        return issues

    def _generate_suggestions(self, quality: Dict, issues: List[str]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if quality['success_rate'] < 0.8:
            suggestions.append("增加错误处理和重试机制")
        
        if quality['avg_tokens'] > 800:
            suggestions.append("优化Prompt，减少Token消耗")
        
        if quality['avg_output_length'] < 100:
            suggestions.append("增加输出详细程度")
        
        if '有子任务失败' in issues:
            suggestions.append("改进任务分解策略")
        
        if 'Token消耗过高' in issues:
            suggestions.append("使用上下文压缩技术")
        
        return suggestions

    def _check_retry_needed(self, quality: Dict, issues: List[str]) -> bool:
        """判断是否需要重试"""
        # 成功率低于阈值
        if quality['success_rate'] < self.quality_thresholds['min_success_rate']:
            return True
        
        # 有严重问题
        if any('失败' in issue for issue in issues):
            return True
        
        return False

    def _generate_summary(self, quality: Dict, issues: List[str]) -> str:
        """生成反思总结"""
        level = quality['quality_level']
        
        summaries = {
            'excellent': '执行质量优秀，结果完全满足预期',
            'good': '执行质量良好，有小幅改进空间',
            'fair': '执行质量一般，需要优化',
            'poor': '执行质量较差，建议重试'
        }
        
        summary = summaries.get(level, '执行完成')
        
        if issues:
            summary += f'。发现 {len(issues)} 个问题'
        
        return summary

    def _get_quality_level(self, score: int) -> str:
        """获取质量等级"""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'fair'
        else:
            return 'poor'
