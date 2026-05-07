#!/usr/bin/env python3
"""
升级版系统测试
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import MultiAgentSystemV2


async def test_simple_task():
    """测试简单任务"""
    print("\n" + "="*60)
    print("🧪 测试1: 简单任务")
    print("="*60)
    
    system = MultiAgentSystemV2()
    result = await system.process_task("解释人工智能")
    
    print("\n结果:")
    print(f"  ✅ 成功: {result['success']}")
    print(f"  📊 质量: {result.get('reflection', {}).get('quality', {}).get('quality_level', 'N/A')}")
    print(f"  💰 Token: {result['execution']['tokens_used']}")
    
    return result['success']


async def test_complex_task():
    """测试复杂任务"""
    print("\n" + "="*60)
    print("🧪 测试2: 复杂任务")
    print("="*60)
    
    system = MultiAgentSystemV2()
    result = await system.process_task("创建一个完整的博客系统")
    
    print("\n结果:")
    print(f"  ✅ 成功: {result['success']}")
    print(f"  📋 子任务: {len(result['execution']['subtasks'])}")
    print(f"  💰 Token: {result['execution']['tokens_used']}")
    print(f"  💵 费用: ${result['execution']['cost']:.4f}")
    print(f"  🧠 反思: {len(result.get('reflection', {}).get('suggestions', []))} 条建议")
    
    return result['success']


async def test_cost_tracking():
    """测试成本追踪"""
    print("\n" + "="*60)
    print("🧪 测试3: 成本追踪")
    print("="*60)
    
    system = MultiAgentSystemV2()
    
    # 运行几个任务
    await system.process_task("写一个Python函数")
    await system.process_task("分析数据趋势")
    
    # 查看成本报告
    stats = system.cost_tracker.get_session_stats()
    print("\n成本统计:")
    print(f"  💰 总Token: {stats['total_tokens']}")
    print(f"  💵 总费用: ${stats['total_cost']:.4f}")
    print(f"  📞 API调用: {stats['api_calls']}")
    
    report = system.cost_tracker.get_cost_report()
    print(f"\n优化建议: {len(report['recommendations'])} 条")
    for rec in report['recommendations']:
        print(f"  💡 {rec}")
    
    return True


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 Multi-Agent System v2.0 - 完整测试")
    print("="*60)
    
    tests = [
        ("简单任务", test_simple_task),
        ("复杂任务", test_complex_task),
        ("成本追踪", test_cost_tracking)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = await test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {name}: {status}")
    
    passed = sum(1 for _, s in results if s)
    print(f"\n总计: {passed}/{len(results)} 通过")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
