# 🎮 本地MCP Server - 手机控制电脑

> 通过手机浏览器控制你的电脑，执行命令、打开应用、管理文件

## 🚀 快速开始

### 1. 下载程序

从GitHub下载：`local-mcp-server/local_mcp_server.py`

或者复制代码到本地文件。

### 2. 运行程序

```bash
# 安装依赖（如果需要）
pip install pywin32  # Windows用户

# 运行
python local_mcp_server.py
```

### 3. 手机访问

程序运行后会显示访问地址：

```
📱 手机访问地址:
   http://192.168.x.x:8888

💻 本机访问:
   http://localhost:8888

🔐 访问密码: trae2026
```

用手机浏览器打开显示的地址即可！

---

## 🎯 功能介绍

### 1. 快速操作

一键打开常用应用：
- 🌐 Chrome浏览器
- 💻 VS Code编辑器
- ⌨️ 终端
- 📁 文件管理器

### 2. 命令执行

在手机上执行电脑命令：
```
ls                    # 列出文件 (Mac/Linux)
dir                   # 列出文件 (Windows)
python --version      # 查看Python版本
git status            # 查看Git状态
```

### 3. 文件操作

- 📖 读取文件内容
- 📝 写入文件
- 📁 查看文件列表

### 4. 剪贴板

- 📋 复制内容到剪贴板
- 📄 从剪贴板读取

### 5. Python代码

直接运行Python代码！

---

## 📱 使用步骤

### 第一步：确保在同一网络

手机和电脑需要连接同一个WiFi。

### 第二步：运行程序

```bash
python local_mcp_server.py
```

### 第三步：记录IP地址

程序会显示手机访问地址，例如：
```
http://192.168.1.100:8888
```

### 第四步：手机访问

1. 打开手机浏览器
2. 输入显示的地址
3. 输入密码：`trae2026`
4. 开始控制！

---

## 💡 使用示例

### 示例1：打开应用

1. 点击"Chrome"按钮
2. 电脑自动打开Chrome浏览器 ✅

### 示例2：执行命令

1. 输入框输入：`python --version`
2. 点击"执行"
3. 看到Python版本信息 ✅

### 示例3：读取文件

1. 输入文件路径：`/Users/你的名字/文档/test.txt`
2. 点击"读取"
3. 看到文件内容 ✅

### 示例4：运行Python

1. 输入代码：`print("Hello from phone!")`
2. 点击"执行Python"
3. 看到输出结果 ✅

---

## 🔐 安全说明

### 密码保护

默认密码：`trae2026`

可以修改代码中的密码：
```python
CONFIG = {
    'password': '你的新密码'
}
```

### 网络安全

- ⚠️ 建议在私人网络使用
- ⚠️ 公共WiFi时请谨慎
- ⚠️ 使用后记得关闭程序

---

## 🛠️ 故障排除

### 问题1：手机打不开页面

**解决：**
1. 检查电脑防火墙设置
2. 确保手机和电脑在同一WiFi
3. 尝试用电脑访问localhost确认程序运行

### 问题2：提示密码错误

**解决：**
1. 检查密码是否正确
2. 默认密码：`trae2026`

### 问题3：命令执行失败

**解决：**
1. 检查命令是否正确
2. Mac/Linux用户使用Unix命令
3. Windows用户使用CMD命令

---

## 📝 代码结构

```python
local_mcp_server.py
├── Web服务器 - 提供网页界面
├── API接口 - 处理各种请求
│   ├── /api/execute - 执行命令
│   ├── /api/open_app - 打开应用
│   ├── /api/read_file - 读取文件
│   ├── /api/write_file - 写入文件
│   └── /api/clipboard - 剪贴板操作
└── HTML页面 - 手机端控制界面
```

---

## 🎨 界面预览

程序提供美观的手机端网页界面：

- 快速操作按钮
- 命令输入框
- 文件浏览器
- 剪贴板工具
- Python执行器

---

## 🔧 高级配置

### 修改端口

```python
CONFIG = {
    'port': 9999  # 改成其他端口
}
```

### 修改密码

```python
CONFIG = {
    'password': 'your_password'  # 改成你的密码
}
```

### 自动打开浏览器

```python
CONFIG = {
    'auto_open_browser': True  # 启动时自动打开浏览器
}
```

---

## 📦 依赖

- Python 3.6+
- pywin32（Windows剪贴板，可选）

安装依赖：
```bash
pip install pywin32  # Windows
```

---

## 🎯 应用场景

### 场景1：远程办公

- 在床上用手机操作电脑
- 躺在沙发上写代码
- 远程控制演示

### 场景2：手机投屏

- 手机查看电脑文件
- 手机操作演示
- 远程技术支持

### 场景3：自动化

- 手机触发电脑脚本
- 远程运行测试
- 定时任务控制

---

## ⚠️ 注意事项

1. **网络安全**
   - 私人网络使用
   - 定期修改密码
   - 不用时关闭程序

2. **权限控制**
   - 部分操作需要管理员权限
   - Windows可能需要以管理员运行

3. **兼容性**
   - 支持 macOS, Windows, Linux
   - 部分功能因系统而异

---

## 📞 支持

- GitHub Issues: https://github.com/g11ma20230417/multi-agent-collaboration/issues

---

## 📄 许可证

MIT License

---

**🎉 让你的手机成为电脑的遥控器！**
