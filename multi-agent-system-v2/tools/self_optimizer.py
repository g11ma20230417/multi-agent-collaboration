#!/usr/bin/env python3
"""
多Agent系统 - 自我分析与优化脚本
使用系统自身的能力来分析和优化代码
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.agent_factory import AgentFactory
from agents.supervisor import SupervisorAgent
from agents.orchestration_engine import OrchestrationEngine


class SelfOptimizer:
    """自我优化器"""

    def __init__(self):
        self.factory = AgentFactory()
        self.supervisor = SupervisorAgent()
        self.orchestration = OrchestrationEngine()
        
    def scan_codebase(self) -> Dict[str, Any]:
        """扫描代码库"""
        print("\n🔍 扫描代码库...")
        
        codebase_info = {
            'total_files': 0,
            'total_lines': 0,
            'languages': {},
            'files': []
        }
        
        project_dir = Path(__file__).parent.parent
        
        for file_path in project_dir.rglob("*.py"):
            if "__pycache__" in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    ext = file_path.suffix
                    
                    codebase_info['total_files'] += 1
                    codebase_info['total_lines'] += lines
                    codebase_info['languages'][ext] = codebase_info['languages'].get(ext, 0) + lines
                    codebase_info['files'].append({
                        'path': str(file_path.relative_to(project_dir)),
                        'lines': lines
                    })
            except:
                pass
        
        # 排序文件
        codebase_info['files'].sort(key=lambda x: x['lines'], reverse=True)
        
        return codebase_info

    def analyze_quality(self, codebase_info: Dict) -> Dict[str, Any]:
        """分析代码质量"""
        print("\n📊 分析代码质量...")
        
        quality_report = {
            'overall_score': 0,
            'issues': [],
            'suggestions': [],
            'strengths': []
        }
        
        # 检查文件数量
        if codebase_info['total_files'] < 5:
            quality_report['issues'].append("文件数量较少，可能功能不完整")
            quality_report['suggestions'].append("考虑增加更多功能模块")
        
        # 检查代码行数
        avg_lines = codebase_info['total_lines'] / max(codebase_info['total_files'], 1)
        if avg_lines < 50:
            quality_report['issues'].append(f"平均文件行数较少 ({avg_lines:.0f}行)")
            quality_report['suggestions'].append("代码可能过于简单，考虑增加复杂性")
        
        # 检查大文件
        large_files = [f for f in codebase_info['files'] if f['lines'] > 500]
        if large_files:
            quality_report['issues'].append(f"有 {len(large_files)} 个大文件(>500行)")
            quality_report['suggestions'].append("考虑拆分大文件以提高可维护性")
        
        # 评分
        score = 70
        score -= len(quality_report['issues']) * 5
        score += len(quality_report['suggestions']) * 2
        quality_report['overall_score'] = max(0, min(100, score))
        
        # 优点
        if codebase_info['total_files'] > 10:
            quality_report['strengths'].append("项目结构完整，文件组织良好")
        if codebase_info['total_lines'] > 1000:
            quality_report['strengths'].append("代码量充足，功能丰富")
        
        return quality_report

    def generate_report(self, codebase_info: Dict, quality_report: Dict) -> str:
        """生成报告"""
        report = []
        report.append("="*60)
        report.append("📋 多Agent系统 - 自我分析报告")
        report.append("="*60)
        report.append("")
        report.append(f"📁 代码库统计:")
        report.append(f"  - 总文件数: {codebase_info['total_files']}")
        report.append(f"  - 总代码行数: {codebase_info['total_lines']}")
        report.append(f"  - 平均文件行数: {codebase_info['total_lines'] / max(codebase_info['total_files'], 1):.0f}")
        report.append("")
        report.append(f"📊 代码质量评分: {quality_report['overall_score']}/100")
        report.append("")
        
        if quality_report['strengths']:
            report.append("✨ 优点:")
            for strength in quality_report['strengths']:
                report.append(f"  ✅ {strength}")
            report.append("")
        
        if quality_report['issues']:
            report.append("⚠️  问题:")
            for issue in quality_report['issues']:
                report.append(f"  ❌ {issue}")
            report.append("")
        
        if quality_report['suggestions']:
            report.append("💡 建议:")
            for suggestion in quality_report['suggestions']:
                report.append(f"  💡 {suggestion}")
            report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)

    async def optimize(self) -> str:
        """执行自我优化"""
        print("\n" + "🎭"*30)
        print("🚀 多Agent系统 - 自我优化开始")
        print("🎭"*30)
        
        # 1. 扫描代码库
        codebase_info = self.scan_codebase()
        
        # 2. 分析质量
        quality_report = self.analyze_quality(codebase_info)
        
        # 3. 生成报告
        report = self.generate_report(codebase_info, quality_report)
        
        print(report)
        
        # 4. 列出主要文件
        print("\n📂 主要文件 (按行数排序):")
        for i, file_info in enumerate(codebase_info['files'][:10], 1):
            print(f"  {i}. {file_info['path']} ({file_info['lines']}行)")
        
        return report


async def main():
    """主函数"""
    optimizer = SelfOptimizer()
    report = await optimizer.optimize()
    
    # 保存报告
    report_file = Path(__file__).parent.parent / "OPTIMIZATION_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 多Agent系统 - 自我分析报告\n\n")
        f.write(report)
        f.write("\n\n---\n*由多Agent系统自我分析生成*\n")
    
    print(f"\n📄 报告已保存到: {report_file}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
