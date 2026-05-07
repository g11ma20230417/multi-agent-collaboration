#!/usr/bin/env python3
"""
测试用例
验证多Agent协同系统
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import MultiAgentSystem


async def test_simple_task():
    """测试简单任务"""
    print("\n" + "="*60)
    print("🧪 测试1: 简单任务")
    print("="*60)
    
    system = MultiAgentSystem()
    result = await system.process_task("解释什么是人工智能")
    
    print("\n结果:")
    print(f"  ✅ 成功: {result['success']}")
    print(f"  📋 子任务数: {len(result['subtasks'])}")
    print(f"  💰 Token消耗: {result['tokens_used']}")
    
    return result['success']


async def test_complex_task():
    """测试复杂任务"""
    print("\n" + "="*60)
    print("🧪 测试2: 复杂任务")
    print("="*60)
    
    system = MultiAgentSystem()
    result = await system.process_task("帮我创建一个完整的博客系统")
    
    print("\n结果:")
    print(f"  ✅ 成功: {result['success']}")
    print(f"  📋 子任务数: {len(result['subtasks'])}")
    print(f"  💰 Token消耗: {result['tokens_used']}")
    print(f"  🚀 优化次数: {len(result['improvements'])}")
    
    return result['success']


async def test_code_generation():
    """测试代码生成"""
    print("\n" + "="*60)
    print("🧪 测试3: 代码生成任务")
    print("="*60)
    
    system = MultiAgentSystem()
    result = await system.process_task("写一个Python爬虫")
    
    print("\n结果:")
    print(f"  ✅ 成功: {result['success']}")
    print(f"  📋 子任务数: {len(result['subtasks'])}")
    print(f"  💰 Token消耗: {result['tokens_used']}")
    
    return result['success']


async def test_self_improvement():
    """测试自我优化"""
    print("\n" + "="*60)
    print("🧪 测试4: 自我优化")
    print("="*60)
    
    system = MultiAgentSystem()
    
    # 先运行几个任务
    await system.process_task("解释机器学习")
    await system.process_task("写一个排序算法")
    
    # 触发自我优化
    improvements = await system.self_improve()
    
    print("\n结果:")
    print(f"  🚀 发现优化点: {len(improvements)}")
    
    return True


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 多Agent协同系统 - 完整测试")
    print("="*60)
    
    tests = [
        ("简单任务", test_simple_task),
        ("复杂任务", test_complex_task),
        ("代码生成", test_code_generation),
        ("自我优化", test_self_improvement)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = await test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            results.append((name, False))
    
    # 打印总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {name}: {status}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
