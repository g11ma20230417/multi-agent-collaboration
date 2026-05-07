#!/usr/bin/env python3
"""
使用OrchestrationEngine优化代码示例
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.orchestration_engine import OrchestrationEngine


async def optimize_codebase():
    """优化代码库"""
    print("\n" + "🎭"*30)
    print("🚀 多Agent系统 - 代码优化任务")
    print("🎭"*30)
    
    # 创建编排引擎
    engine = OrchestrationEngine()
    
    # 定义优化任务
    task = """
    优化多Agent系统的代码：
    1. 分析现有代码结构
    2. 识别可以改进的地方
    3. 优化代码组织和注释
    4. 增加错误处理
    5. 提升代码可读性
    """
    
    print(f"\n📋 任务描述: {task.strip()}")
    print("\n" + "="*60)
    
    # 执行编排
    result = await engine.orchestrate(task)
    
    print("\n" + "="*60)
    print("📊 编排结果:")
    print("="*60)
    print(f"  状态: {'✅ 成功' if result['success'] else '❌ 失败'}")
    print(f"  创建的Agent: {result.get('agents_created', [])}")
    print(f"  任务分配: {len(result.get('assignments', {}))} 个")
    print(f"  执行结果: {len(result.get('results', {}))} 个")
    
    # 显示编排统计
    stats = engine.get_orchestration_stats()
    print(f"\n📊 系统统计:")
    print(f"  - 总Agent数: {stats['total_agents_created']}")
    print(f"  - Agent类型: {list(set(a['agent_type'] for a in stats['factory_stats'].get('agents', [])))}")
    
    return result


async def demo_multi_agent():
    """演示多Agent协作"""
    print("\n" + "🎭"*30)
    print("🎭 多Agent系统 - 协作演示")
    print("🎭"*30)
    
    # 创建多个任务进行演示
    tasks = [
        "分析代码库结构",
        "识别性能瓶颈",
        "生成优化建议"
    ]
    
    engine = OrchestrationEngine()
    
    for i, task in enumerate(tasks, 1):
        print(f"\n📋 任务 {i}/{len(tasks)}: {task}")
        
        # 使用编排引擎处理
        result = await engine.orchestrate(task)
        
        print(f"  ✅ 完成: {'成功' if result['success'] else '失败'}")
        print(f"  🤖 使用了 {len(result.get('agents_created', []))} 个Agent")


async def main():
    """主函数"""
    try:
        # 运行优化任务
        await optimize_codebase()
        
        # 演示多Agent协作
        await demo_multi_agent()
        
        print("\n" + "🎉"*30)
        print("🎉 多Agent系统演示完成!")
        print("🎉"*30)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
