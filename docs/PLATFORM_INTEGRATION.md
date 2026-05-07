# 多Agent协同系统 - 平台集成指南

> 本文档详细说明如何将多Agent协同系统集成到 OpenClaw、OpenCode、TRAE IDE、HERMES 等平台

## 📋 目录

- [1. OpenClaw 集成](#1-openclaw-集成)
- [2. OpenCode 集成](#2-opencode-集成)
- [3. TRAE IDE 集成](#3-trae-ide-集成)
- [4. HERMES 集成](#4-hermes-集成)
- [5. 通用 API 调用](#5-通用-api-调用)
- [6. MCP Server 配置](#6-mcp-server-配置)

---

## 1. OpenClaw 集成

### 1.1 简介

OpenClaw 是一个开源的个人 AI 助手框架，支持通过 Skills、Plugins 和 Webhooks 进行扩展。

### 1.2 安装 OpenClaw

```bash
# 安装 OpenClaw
npm install -g openclaw@latest

# 运行初始化向导
openclaw onboard

# 启动网关
openclaw gateway
```

### 1.3 创建 Skill

在 `~/.openclaw/skills/` 目录下创建技能：

```
~/.openclaw/skills/multi-agent/
├── SKILL.md
└── README.md
```

#### SKILL.md 示例

```markdown
---
name: multi-agent-collaboration
description: 多Agent协同工作系统 - 自动创建Agent、分配任务、学习进化
requires:
  bins:
    - python3
  env:
    - MULTI_AGENT_PATH
---

# Multi-Agent Collaboration System

这是一个多Agent协同工作系统，支持自动创建Agent、动态任务分配和自我学习。

## 功能

- 🤖 自动创建专用Agent
- 📋 智能任务分解
- ⚡ 异步并行执行
- 📚 自我学习进化
- 💰 成本实时监控

## 使用方法

### 运行系统
cd $MULTI_AGENT_PATH && python3 main.py "你的任务"

### 运行演示
cd $MULTI_AGENT_PATH && python3 main.py

### 查看统计
cd $MULTI_AGENT_PATH && python3 -c "from main import *; ..."
```

### 1.4 创建 Plugin

```bash
mkdir -p ~/.openclaw/plugins/multi-agent
cd ~/.openclaw/plugins/multi-agent
npm init -y
```

创建 `src/index.ts`:

```typescript
import { OpenClaw } from '@openclaw/api';

export default function register(api: OpenClaw) {
  api.registerTool({
    name: 'multi_agent_orchestrate',
    description: '使用多Agent协同系统处理复杂任务',
    inputSchema: {
      type: 'object',
      properties: {
        task: {
          type: 'string',
          description: '要处理的任务描述'
        }
      },
      required: ['task']
    },
    async handler({ task }) {
      // 调用多Agent系统
      const { execSync } = require('child_process');
      const result = execSync(
        `cd $MULTI_AGENT_PATH && python3 -c "import asyncio; from main import *; ..."`,
        { encoding: 'utf-8' }
      );
      return result;
    }
  });
}
```

### 1.5 Webhook 集成

在 OpenClaw 配置中添加 webhook：

```json
{
  "gateway": {
    "webhooks": {
      "multi_agent": {
        "url": "http://localhost:8080/webhook",
        "events": ["task.completed", "agent.created"]
      }
    }
  }
}
```

### 1.6 API 调用

启用 HTTP API：

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true },
        "responses": { "enabled": true }
      }
    }
  }
}
```

通过 API 调用：

```bash
curl -X POST http://localhost:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "model": "main",
    "messages": [{"role": "user", "content": "使用多Agent系统处理：创建一个博客系统"}]
  }'
```

---

## 2. OpenCode 集成

### 2.1 简介

OpenCode 是基于 OpenModelStudio 的 AI 编程助手，支持 REST API 调用。

### 2.2 API 配置

```bash
# 设置环境变量
export OMS_BASE_URL="http://localhost:31001"
export OMS_API_KEY="your_api_key_here"
```

### 2.3 Python SDK 集成

```python
import requests

class OpenCodeIntegration:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def call_multi_agent(self, task: str):
        """调用多Agent系统"""
        # 调用我们的系统
        response = requests.post(
            f"{self.base_url}/llm/chat",
            headers=self.headers,
            json={
                "prompt": f"使用多Agent系统处理: {task}",
                "model": "gpt-4"
            }
        )
        return response.json()
    
    def get_results(self):
        """获取执行结果"""
        response = requests.get(
            f"{self.base_url}/artifacts",
            headers=self.headers
        )
        return response.json()
```

### 2.4 OpenCode Plugin

创建 `opencode-plugin.js`:

```javascript
const { Client } = require('@opencode/sdk');

class MultiAgentPlugin {
  constructor() {
    this.client = new Client({
      baseUrl: process.env.OMS_BASE_URL,
      apiKey: process.env.OMS_API_KEY
    });
  }
  
  async onTaskCreated(task) {
    // 自动使用多Agent系统处理
    if (task.type === 'complex') {
      await this.client.call('multi_agent_orchestrate', {
        task: task.description
      });
    }
  }
}

module.exports = MultiAgentPlugin;
```

### 2.5 Agent 工具注册

```bash
# 在 OpenCode 中注册工具
opencode tools register multi-agent \
  --command "python3 /path/to/multi-agent-system/main.py" \
  --description "多Agent协同工作系统"
```

---

## 3. TRAE IDE 集成

### 3.1 简介

TRAE IDE 支持 MCP (Model Context Protocol) 和 Skills 扩展。

### 3.2 添加 MCP Server

#### 方式一：从市场添加

1. 打开设置 → MCP
2. 点击 "添加" → "从市场添加"
3. 选择需要的 MCP Server
4. 填写配置信息并确认

#### 方式二：手动添加

在项目根目录创建 `.trae/mcp.json`:

```json
{
  "mcpServers": {
    "multi-agent-system": {
      "command": "python3",
      "args": [
        "-m",
        "http.server",
        "8080",
        "--directory",
        "/path/to/multi-agent-system"
      ],
      "env": {
        "START_MCP_TIMEOUT_MS": "60000"
      }
    }
  }
}
```

### 3.3 创建 TRAE Skill

在项目根目录创建 `.trae/skills/`：

```
.trae/skills/multi-agent/
├── SKILL.md
└── instructions.md
```

#### SKILL.md 示例

```markdown
# Multi-Agent Collaboration Skill

## 简介

这是一个多Agent协同工作系统的Skill，支持自动创建Agent、动态任务分配和自我学习。

## 触发条件

当用户请求以下内容时自动激活：
- "创建完整系统"
- "多Agent协同"
- "自动分配任务"
- "复杂任务处理"

## 使用方法

### 基本命令

```
使用多Agent系统处理: <任务描述>
```

### 交互模式

```
启动多Agent协作引擎
```

### 查看统计

```
多Agent系统统计
```

## 能力

- ✅ 自动创建专用Agent
- ✅ 智能任务分解
- ✅ 异步并行执行
- ✅ 自我学习进化
- ✅ 成本实时监控
- ✅ 反思机制

## 限制

- 需要 Python 3.8+
- 需要网络连接访问外部API
- 建议单任务Token限制: 10000
```

### 3.4 自定义 Agent 配置

在 `.trae/agents/` 创建配置文件：

```json
{
  "agents": [
    {
      "name": "Multi-Agent Orchestrator",
      "description": "多Agent协同工作协调器",
      "systemPrompt": "你是一个专业的多Agent系统协调员，擅长分解复杂任务、分配给专用Agent、并整合结果。",
      "tools": ["multi-agent-orchestrate", "task-decompose"],
      "skills": ["multi-agent"]
    }
  ]
}
```

### 3.5 项目级配置

创建 `.trae/project_rules.md`:

```markdown
## 多Agent协同使用规范

### 任务类型判断

- **简单任务** (直接执行): 解释、简单查询
- **中等任务** (单Agent): 单个功能开发、代码审查
- **复杂任务** (多Agent): 完整系统、多个功能集成

### 触发多Agent的条件

当任务包含以下关键词时自动使用多Agent系统：
- "完整"、"系统"、"项目"
- "多个功能"、"集成"
- "自动化"、"工作流"

### Agent分配策略

| 任务类型 | Agent | 数量 |
|---------|-------|------|
| 代码生成 | CoderAgent | 1-2 |
| 测试 | TesterAgent | 1 |
| 部署 | DevOpsAgent | 1 |
| 研究 | ResearcherAgent | 1 |
| 分析 | AnalystAgent | 1 |
```

### 3.6 启用项目级 MCP

1. 打开设置 → MCP
2. 启用 "启用项目级 MCP" 开关
3. 在项目 `.trae/mcp.json` 中配置

---

## 4. HERMES 集成

### 4.1 简介

HERMES 是一个开源的 AI Agent 框架，支持自定义 Agent 和任务编排。

### 4.2 安装 HERMES

```bash
pip install hermes-ai
hermes init my-project
cd my-project
```

### 4.3 创建自定义 Agent

创建 `agents/multi_agent_orchestrator.py`:

```python
from hermes.agent import Agent
from hermes.tool import Tool

class MultiAgentOrchestrator(Agent):
    name = "multi_agent_orchestrator"
    description = "多Agent协同工作协调器"
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """
        你是一个专业的多Agent系统协调员。
        你的职责：
        1. 分析用户任务复杂度
        2. 决定是否需要启动多Agent
        3. 协调各Agent工作
        4. 整合最终结果
        """
    
    async def plan(self, task: str) -> dict:
        """分析任务并制定计划"""
        # 调用任务分析
        is_complex = len(task) > 100 or any(
            kw in task for kw in ['系统', '完整', '多个', '项目']
        )
        
        return {
            'use_multi_agent': is_complex,
            'estimated_agents': 3 if is_complex else 1,
            'task_breakdown': self._breakdown_task(task)
        }
    
    async def execute(self, plan: dict):
        """执行计划"""
        if plan['use_multi_agent']:
            # 启动多Agent系统
            return await self._run_multi_agent(plan)
        else:
            # 单Agent执行
            return await self._run_single_agent(plan)
    
    async def _run_multi_agent(self, plan: dict):
        """运行多Agent系统"""
        # 调用我们的系统
        from multi_agent_system.main import MultiAgentSystem
        
        system = MultiAgentSystem()
        result = await system.process_task(plan['task'])
        return result
```

### 4.4 注册 Tool

创建 `tools/multi_agent_tools.py`:

```python
from hermes.tool import Tool

class OrchestrateTask(Tool):
    name = "orchestrate_task"
    description = "使用多Agent协同系统处理复杂任务"
    
    parameters = {
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "要处理的任务"
            },
            "options": {
                "type": "object",
                "description": "可选配置",
                "properties": {
                    "max_agents": {"type": "number"},
                    "timeout": {"type": "number"},
                    "parallel": {"type": "boolean"}
                }
            }
        },
        "required": ["task"]
    }
    
    async def execute(self, task: str, options: dict = None):
        """执行任务编排"""
        from multi_agent_system.main import MultiAgentSystem
        
        system = MultiAgentSystem()
        result = await system.process_task(task)
        return result
```

### 4.5 HERMES 配置文件

创建 `hermes.config.json`:

```json
{
  "agents": [
    {
      "name": "multi_agent_orchestrator",
      "type": "custom",
      "module": "agents.multi_agent_orchestrator",
      "enabled": true
    }
  ],
  "tools": [
    {
      "name": "orchestrate_task",
      "type": "custom",
      "module": "tools.multi_agent_tools",
      "enabled": true
    }
  ],
  "mcp_servers": [
    {
      "name": "multi-agent-system",
      "command": "python3 -m http.server 8080",
      "cwd": "/path/to/multi-agent-system"
    }
  ]
}
```

### 4.6 启动 HERMES

```bash
hermes start --config hermes.config.json
```

---

## 5. 通用 API 调用

### 5.1 REST API

将多Agent系统暴露为 REST API：

```python
from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)

@app.route('/api/orchestrate', methods=['POST'])
def orchestrate():
    data = request.json
    task = data.get('task')
    
    if not task:
        return jsonify({'error': 'Task is required'}), 400
    
    # 运行多Agent系统
    async def run():
        from main import MultiAgentSystem
        system = MultiAgentSystem()
        return await system.process_task(task)
    
    result = asyncio.run(run())
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def stats():
    from main import MultiAgentSystem
    system = MultiAgentSystem()
    return jsonify(system.get_stats())

@app.route('/api/agents', methods=['GET'])
def list_agents():
    from agents.agent_factory import AgentFactory
    factory = AgentFactory()
    return jsonify(factory.get_factory_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### 5.2 启动 API 服务器

```bash
python3 api_server.py
```

### 5.3 客户端调用示例

```python
import requests

class MultiAgentClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
    
    def orchestrate(self, task: str):
        """编排任务"""
        response = requests.post(
            f"{self.base_url}/api/orchestrate",
            json={'task': task}
        )
        return response.json()
    
    def get_stats(self):
        """获取统计"""
        response = requests.get(f"{self.base_url}/api/stats")
        return response.json()
    
    def list_agents(self):
        """列出Agent"""
        response = requests.get(f"{self.base_url}/api/agents")
        return response.json()
```

### 5.4 WebSocket 支持

```python
import asyncio
import websockets
import json

async def websocket_handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        
        if data['type'] == 'orchestrate':
            from main import MultiAgentSystem
            system = MultiAgentSystem()
            
            # 流式发送进度
            async def progress_callback(progress):
                await websocket.send(json.dumps({
                    'type': 'progress',
                    'data': progress
                }))
            
            result = await system.process_task(
                data['task'],
                progress_callback=progress_callback
            )
            
            await websocket.send(json.dumps({
                'type': 'result',
                'data': result
            }))

asyncio.get_event_loop().run_until_complete(
    websockets.serve(websocket_handler, '0.0.0.0', 8765)
)
asyncio.get_event_loop().run_forever()
```

---

## 6. MCP Server 配置

### 6.1 stdio 类型配置

```json
{
  "mcpServers": {
    "multi-agent": {
      "command": "python3",
      "args": ["/path/to/multi-agent-system/mcp_server.py"],
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_CONCURRENT": "5"
      }
    }
  }
}
```

### 6.2 HTTP 类型配置

```json
{
  "mcpServers": {
    "multi-agent": {
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

### 6.3 MCP Server 实现

创建 `mcp_server.py`:

```python
#!/usr/bin/env python3
"""MCP Server 实现"""

import json
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("multi-agent-system")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="orchestrate_task",
            description="使用多Agent协同系统处理复杂任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "要处理的任务描述"
                    },
                    "options": {
                        "type": "object",
                        "description": "可选配置",
                        "properties": {
                            "max_agents": {"type": "number"},
                            "timeout": {"type": "number"}
                        }
                    }
                },
                "required": ["task"]
            }
        ),
        Tool(
            name="get_system_stats",
            description="获取多Agent系统统计信息",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="list_agents",
            description="列出所有已创建的Agent",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "orchestrate_task":
        from main import MultiAgentSystem
        system = MultiAgentSystem()
        result = await system.process_task(arguments['task'])
        return [TextContent(type="text", text=json.dumps(result))]
    
    elif name == "get_system_stats":
        from main import MultiAgentSystem
        system = MultiAgentSystem()
        return [TextContent(type="text", text=json.dumps(system.get_stats()))]
    
    elif name == "list_agents":
        from agents.agent_factory import AgentFactory
        factory = AgentFactory()
        return [TextContent(type="text", text=json.dumps(factory.get_factory_stats()))]
    
    return [TextContent(type="text", text="Unknown tool")]

if __name__ == "__main__":
    import mcp.server.stdio
    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())
```

---

## 📚 总结

| 平台 | 集成方式 | 难度 | 推荐度 |
|------|---------|------|--------|
| **OpenClaw** | Skills/Plugins/Webhooks | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **OpenCode** | REST API/Python SDK | ⭐⭐ | ⭐⭐⭐⭐ |
| **TRAE** | MCP/Skills | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **HERMES** | Custom Agent/Tools | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🔗 相关资源

- [OpenClaw 官方文档](https://openclawapi.org/)
- [OpenModelStudio API](https://github.com/GACWR/OpenModelStudio)
- [TRAE MCP 文档](https://docs.trae.ai/)
- [HERMES GitHub](https://github.com/hermes-ai)
- [MCP 官方规范](https://modelcontextprotocol.io/)

---

**最后更新**: 2026-05-07
