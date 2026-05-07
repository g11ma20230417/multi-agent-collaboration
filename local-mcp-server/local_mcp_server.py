#!/usr/bin/env python3
"""
本地MCP Server - 让你通过手机控制电脑

功能：
1. Web服务器 - 手机浏览器控制电脑
2. 命令执行 - 运行终端命令
3. 文件操作 - 读写文件
4. 应用控制 - 打开/关闭应用
5. 剪贴板 - 读写剪贴板
"""

import os
import sys
import json
import time
import subprocess
import webbrowser
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import socket

# 配置文件
CONFIG = {
    'host': '0.0.0.0',
    'port': 8888,
    'password': 'trae2026',  # 访问密码
    'auto_open_browser': True
}

# 存储执行结果
results = {}


class MCPHandler(SimpleHTTPRequestHandler):
    """处理MCP请求"""
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")
    
    def do_GET(self):
        """处理GET请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            self.send_html()
        elif path == '/api/status':
            self.send_json({'status': 'online', 'time': time.time()})
        elif path == '/api/commands':
            self.send_json({'commands': list(results.keys())})
        elif path.startswith('/api/result/'):
            cmd_id = path.split('/')[-1]
            self.send_json(results.get(cmd_id, {'error': 'Not found'}))
        else:
            super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except:
            data = {}
        
        # 验证密码
        if data.get('password') != CONFIG['password']:
            self.send_json({'error': 'Invalid password'})
            return
        
        if path == '/api/execute':
            self.handle_execute(data)
        elif path == '/api/open_app':
            self.handle_open_app(data)
        elif path == '/api/read_file':
            self.handle_read_file(data)
        elif path == '/api/write_file':
            self.handle_write_file(data)
        elif path == '/api/clipboard':
            self.handle_clipboard(data)
        else:
            self.send_json({'error': 'Unknown endpoint'})
    
    def send_json(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_html(self):
        """发送控制页面"""
        html = """<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 电脑控制中心</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 600px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        h1 { 
            text-align: center; 
            color: white; 
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        h2 { color: #333; margin-bottom: 16px; font-size: 18px; }
        .input-group { margin-bottom: 16px; }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        button:active { transform: translateY(0); }
        .quick-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .quick-btn {
            padding: 16px;
            background: #f8f9fa;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            color: #333;
        }
        .quick-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        #output {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 16px;
            border-radius: 10px;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 14px;
            white-space: pre-wrap;
            margin-top: 16px;
        }
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 16px;
            background: #e8f5e9;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            background: #4caf50;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .info {
            background: #e3f2fd;
            padding: 16px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 14px;
            color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 电脑控制中心</h1>
        
        <div class="status">
            <div class="status-dot"></div>
            <span>✅ 系统在线 - 等待指令</span>
        </div>
        
        <div class="card">
            <h2>⚡ 快速操作</h2>
            <div class="quick-btns">
                <button class="quick-btn" onclick="openApp('chrome')">🌐 Chrome</button>
                <button class="quick-btn" onclick="openApp('vscode')">💻 VS Code</button>
                <button class="quick-btn" onclick="openApp('terminal')">⌨️ 终端</button>
                <button class="quick-btn" onclick="openApp('finder')">📁 文件</button>
            </div>
        </div>
        
        <div class="card">
            <h2>⌨️ 执行命令</h2>
            <div class="input-group">
                <input type="text" id="command" placeholder="输入命令，例如: ls, dir, python --version">
            </div>
            <button onclick="executeCommand()">▶️ 执行</button>
            <div id="output">等待命令输出...</div>
        </div>
        
        <div class="card">
            <h2>📁 文件操作</h2>
            <div class="input-group">
                <input type="text" id="filePath" placeholder="文件路径，例如: /Users/test/document.txt">
            </div>
            <button onclick="readFile()">📖 读取</button>
        </div>
        
        <div class="card">
            <h2>📋 剪贴板</h2>
            <div class="input-group">
                <textarea id="clipboardInput" rows="3" placeholder="输入要复制的内容"></textarea>
            </div>
            <button onclick="copyClipboard()">📋 复制到剪贴板</button>
        </div>
        
        <div class="card">
            <h2>📝 执行Python代码</h2>
            <div class="input-group">
                <textarea id="pythonCode" rows="4" placeholder="输入Python代码"></textarea>
            </div>
            <button onclick="runPython()">🐍 执行Python</button>
        </div>
        
        <div class="info">
            <strong>💡 使用提示：</strong><br>
            - 访问地址: <code id="localIP">获取中...</code><br>
            - 手机和电脑需要在同一网络<br>
            - 默认密码: <code>trae2026</code>
        </div>
    </div>
    
    <script>
        const API_BASE = '';
        
        async function executeCommand() {
            const cmd = document.getElementById('command').value;
            if (!cmd) return alert('请输入命令');
            
            const output = document.getElementById('output');
            output.textContent = '执行中...';
            
            try {
                const resp = await fetch(API_BASE + '/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({password: 'trae2026', command: cmd})
                });
                const data = await resp.json();
                output.textContent = data.output || data.error || '完成';
            } catch (e) {
                output.textContent = '错误: ' + e.message;
            }
        }
        
        async function openApp(app) {
            try {
                await fetch(API_BASE + '/api/open_app', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({password: 'trae2026', app: app})
                });
                alert('应用已打开: ' + app);
            } catch (e) {
                alert('错误: ' + e.message);
            }
        }
        
        async function readFile() {
            const path = document.getElementById('filePath').value;
            if (!path) return alert('请输入文件路径');
            
            try {
                const resp = await fetch(API_BASE + '/api/read_file', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({password: 'trae2026', path: path})
                });
                const data = await resp.json();
                document.getElementById('output').textContent = data.content || data.error;
            } catch (e) {
                alert('错误: ' + e.message);
            }
        }
        
        async function copyClipboard() {
            const text = document.getElementById('clipboardInput').value;
            try {
                await fetch(API_BASE + '/api/clipboard', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({password: 'trae2026', action: 'write', text: text})
                });
                alert('已复制到剪贴板');
            } catch (e) {
                alert('错误: ' + e.message);
            }
        }
        
        async function runPython() {
            const code = document.getElementById('pythonCode').value;
            if (!code) return alert('请输入Python代码');
            
            const output = document.getElementById('output');
            output.textContent = '执行中...';
            
            try {
                const resp = await fetch(API_BASE + '/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({password: 'trae2026', command: 'python3 -c "' + code.replace(/"/g, '\\\\"') + '"'})
                });
                const data = await resp.json();
                output.textContent = data.output || data.error;
            } catch (e) {
                output.textContent = '错误: ' + e.message;
            }
        }
        
        // 显示本机IP
        fetch(API_BASE + '/api/status').then(r => r.json()).then(() => {
            fetch('https://api.ipify.org?format=json').then(r => r.json()).then(data => {
                document.getElementById('localIP').textContent = 'http://' + data.ip + ':' + """ + str(CONFIG['port']) + """';
            }).catch(() => {
                document.getElementById('localIP').textContent = 'localhost:""" + str(CONFIG['port']) + """';
            });
        });
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_execute(self, data):
        """执行命令"""
        command = data.get('command', '')
        if not command:
            self.send_json({'error': 'No command provided'})
            return
        
        try:
            # 分离命令和参数
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            
            # 生成唯一ID
            cmd_id = str(int(time.time() * 1000))
            results[cmd_id] = {
                'command': command,
                'output': output,
                'returncode': result.returncode,
                'timestamp': time.time()
            }
            
            self.send_json({
                'success': True,
                'output': output,
                'returncode': result.returncode,
                'id': cmd_id
            })
        except subprocess.TimeoutExpired:
            self.send_json({'error': 'Command timeout'})
        except Exception as e:
            self.send_json({'error': str(e)})
    
    def handle_open_app(self, data):
        """打开应用"""
        app = data.get('app', '')
        
        app_map = {
            'chrome': 'Google Chrome' if sys.platform == 'darwin' else 'chrome',
            'vscode': 'Visual Studio Code' if sys.platform == 'darwin' else 'code',
            'terminal': 'Terminal' if sys.platform == 'darwin' else 'cmd.exe',
            'finder': 'Finder' if sys.platform == 'darwin' else 'explorer.exe'
        }
        
        app_name = app_map.get(app, app)
        
        try:
            if sys.platform == 'darwin':
                subprocess.run(['open', '-a', app_name])
            elif sys.platform == 'win32':
                subprocess.Popen(app_name)
            else:
                subprocess.run([app_name])
            
            self.send_json({'success': True, 'message': f'Opened: {app_name}'})
        except Exception as e:
            self.send_json({'error': str(e)})
    
    def handle_read_file(self, data):
        """读取文件"""
        filepath = data.get('path', '')
        if not filepath:
            self.send_json({'error': 'No path provided'})
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(10000)  # 限制读取大小
            self.send_json({'success': True, 'content': content})
        except FileNotFoundError:
            self.send_json({'error': 'File not found'})
        except Exception as e:
            self.send_json({'error': str(e)})
    
    def handle_write_file(self, data):
        """写入文件"""
        filepath = data.get('path', '')
        content = data.get('content', '')
        
        if not filepath:
            self.send_json({'error': 'No path provided'})
            return
        
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.send_json({'success': True, 'message': 'File written'})
        except Exception as e:
            self.send_json({'error': str(e)})
    
    def handle_clipboard(self, data):
        """剪贴板操作"""
        action = data.get('action', 'read')
        
        try:
            if sys.platform == 'darwin':
                if action == 'write':
                    subprocess.run(['pbcopy'], input=data.get('text', '').encode())
                else:
                    result = subprocess.run(['pbpaste'], capture_output=True)
                    self.send_json({'success': True, 'text': result.stdout.decode()})
            elif sys.platform == 'win32':
                import win32clipboard
                if action == 'write':
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardText(data.get('text', ''))
                    win32clipboard.CloseClipboard()
                else:
                    win32clipboard.OpenClipboard()
                    text = win32clipboard.GetClipboardText()
                    win32clipboard.CloseClipboard()
                    self.send_json({'success': True, 'text': text})
            else:
                self.send_json({'error': 'Clipboard not supported on this platform'})
        except Exception as e:
            self.send_json({'error': str(e)})


def get_local_ip():
    """获取本机IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def main():
    """主函数"""
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🎮 本地MCP Server - 电脑控制中心")
    print("="*60)
    print(f"\n✅ 服务器启动成功!")
    print(f"\n📱 手机访问地址:")
    print(f"   http://{local_ip}:{CONFIG['port']}")
    print(f"\n💻 本机访问:")
    print(f"   http://localhost:{CONFIG['port']}")
    print(f"\n🔐 访问密码: {CONFIG['password']}")
    print(f"\n按 Ctrl+C 停止服务器")
    print("="*60 + "\n")
    
    # 启动服务器
    server = HTTPServer((CONFIG['host'], CONFIG['port']), MCPHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        server.shutdown()


if __name__ == '__main__':
    main()
