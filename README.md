## 快速开始

### 环境要求

- **Python 3.11+**（由 uv 自动管理，无需手动安装）
- **uv** 最新版
- 一个可用的 API Key（DeepSeek / OpenAI / Qwen 任选其一）

### 1. 安装 uv

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装后关闭并重新打开终端，执行 `uv --version` 验证。

### 2. 克隆项目

```bash
git clone https://github.com/OUENWEI/local-doc-agent.git
cd local-doc-agent
```

### 3. 安装依赖

```bash
uv sync
```

> 国内用户可创建 `uv.toml` 加速：
> ```toml
> [[index]]
> url = "https://pypi.tuna.tsinghua.edu.cn/simple"
> default = true
> ```

### 4. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env`，至少填入一个 Key（等号两边不要空格，值不加引号）：

```text
DS_API_KEY=sk-你的DeepSeek密钥
```

### 5. 启动 WebUI

```bash
uv run streamlit run scripts/webui.py
```

浏览器会自动打开 `http://localhost:8501`，左侧选择模型，点击「启动 Agent」即可对话。

### 6. 启动 CLI（备选）

```bash
uv run python scripts/run_cli.py
```

按提示输入模型别名和用户 ID，即可在终端对话。

### 可选：3D 建模

需要额外安装 [Blender](https://www.blender.org/download/) 和 [MCP for Blender 插件](https://github.com/ahujasid/mcp-for-blender)。在 Blender 中启动 MCP 服务器（显示 `Connected on port 9876`），然后在 WebUI 中勾选「导入 Blender 工具」即可使用。

## 📖 使用说明

### 文件读取方式

当前版本**仅支持通过输入文件路径来读取本地文件**，暂不支持在 WebUI 中直接上传文件。

使用方式：在对话框中输入文件的完整路径，例如：

```text
帮我分析一下 C:\Users\pc\Desktop\学生成绩表.xlsx
```

或

```text
帮我读一下 /Users/pc/Documents/报告.docx
```

Agent 会自动识别文件类型（Word / Excel），读取内容并进行分析。

> ⚠️ 注意：
> - 文件必须位于本地磁盘，且路径正确。
> - 暂不支持网络文件或云盘链接。
> - 后续版本会加入文件上传功能，敬请期待。