# 🚀 TRAE SOLO 多Agent协作Skill安装指南

> 让你的TRAE SOLO拥有多Agent协同能力

## 📋 目录

- [功能介绍](#功能介绍)
- [安装步骤](#安装步骤)
- [使用方法](#使用方法)
- [示例](#示例)
- [配置选项](#配置选项)

---

## 功能介绍

这个Skill让你的TRAE SOLO可以：

✅ **自动创建Agent** - 根据任务需求自动创建专用Agent  
✅ **智能任务分解** - 复杂任务自动拆分为子任务  
✅ **并行执行** - 多任务并发处理，效率提升  
✅ **自我学习** - 从执行中学习，持续优化  
✅ **成本控制** - 实时监控Token消耗  

---

## 安装步骤

### 方法一：从GitHub安装（推荐）

#### 步骤1：下载Skill文件

1. 访问 GitHub 仓库：
   ```
   https://github.com/g11ma20230417/multi-agent-collaboration
   ```

2. 点击 **Code** → **Download ZIP**

3. 解压文件，找到 `SKILL.md`

#### 步骤2：在TRAE中安装

1. 打开 TRAE SOLO
2. 进入设置（⚙️）
3. 找到 **Skills** 或 **技能** 选项
4. 点击 **添加技能**
5. 选择 **从文件导入**
6. 选择下载的 `SKILL.md` 文件

#### 步骤3：验证安装

在SOLO中输入：
```
测试多Agent技能
```

如果系统回复说技能已激活，说明安装成功！

---

### 方法二：手动创建

#### 步骤1：找到Skill目录

在项目根目录创建：
```
.trae/skills/multi-agent/
```

#### 步骤2：创建SKILL.md

将以下内容复制到 `SKILL.md` 文件：

```markdown
# Multi-Agent Collaboration Skill

> 一句话调用多Agent协同系统

## 触发条件

- "多Agent"
- "协同工作"
- "创建完整系统"
- "复杂任务"

## 功能

- 自动创建Agent
- 智能任务分解
- 并行执行
- 自我学习

## 使用

直接说出你的需求，例如：
"多Agent处理：帮我创建一个博客系统"
```

#### 步骤3：在TRAE中启用

1. 打开项目设置
2. 启用项目级Skills
3. 确认Skill已加载

---

## 使用方法

### 基本语法

在SOLO中这样使用：

```
@multi-agent <任务描述>
```

或者直接说：

```
帮我用多Agent处理：<任务描述>
```

---

## 示例

### 示例1：创建完整系统

```
输入：
@multi-agent 帮我创建一个完整的博客系统，包含用户登录、文章发布、评论功能

输出：
🎭 多Agent系统启动...

✅ 完成！
- 创建了3个Agent
- 处理了5个子任务
- Token消耗：减少25%
```

### 示例2：复杂项目开发

```
输入：
用多Agent处理这个项目，需要：
1. 后端API开发
2. 前端界面
3. 数据库设计
4. 测试验证

输出：
🎭 多Agent系统启动...

🤖 创建的Agent：
- CoderAgent × 2（后端+前端）
- DesignerAgent × 1
- TesterAgent × 1

✅ 完成！
- 所有任务并行执行
- 总耗时：减少40%
```

### 示例3：数据分析任务

```
输入：
@multi-agent 分析这个销售数据集，找出趋势和洞察

输出：
🎭 多Agent系统启动...

✅ 完成！
- 创建了AnalystAgent
- 识别了5个关键洞察
- 生成了可视化建议
```

---

## 配置选项

### 速度模式

```
@multi-agent speed=fast     # 快速模式
@multi-agent speed=balanced  # 平衡模式（默认）
@multi-agent speed=thorough  # 详细模式
```

### Agent数量

```
@multi-agent agents=3   # 最少Agent
@multi-agent agents=5   # 标准（默认）
@multi-agent agents=10  # 最多Agent
```

### Token限制

```
@multi-agent tokens=5000   # 低消耗
@multi-agent tokens=10000  # 标准（默认）
@multi-agent tokens=20000  # 高消耗
```

---

## 故障排除

### 问题1：Skill不激活

**解决方案：**
1. 检查是否正确安装了SKILL.md
2. 确认项目根目录下有 `.trae/skills/` 目录
3. 重启TRAE

### 问题2：Agent创建失败

**解决方案：**
1. 简化任务描述
2. 减少Agent数量
3. 检查网络连接

### 问题3：Token超限

**解决方案：**
1. 降低Token限制
2. 分割任务为多个小任务
3. 使用快速模式

---

## 技术支持

- **GitHub**: https://github.com/g11ma20230417/multi-agent-collaboration
- **问题反馈**: 在GitHub Issues中提交

---

## 更新日志

### v1.0.0 (2026-05-07)

- ✨ 初始版本发布
- ✅ 支持8种Agent类型
- ✅ 智能任务分解
- ✅ 并行执行
- ✅ 成本控制

---

**享受多Agent协作带来的高效开发体验！** 🚀
