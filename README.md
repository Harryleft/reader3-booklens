# BookLens

![homepage](/image/homepage.jpg)

一个自托管 EPUB 阅读器，让你逐章阅读 EPUB 电子书，并将章节内容一键复制给 LLM 进行共读理解。

## 功能

- 逐章阅读 EPUB 电子书，支持目录导航
- 浮动按钮一键复制章节内容，自动用提示词模板包裹
- 内置提示词模板 + 自定义模板管理
- Web 端导入页面，支持拖拽上传 EPUB 文件，自动解析入库
- 自动提取书籍元数据（标题、作者、目录结构、图片）
- 微信读书式正文界面：目录抽屉、双栏、字号/行距/字体和深浅色主题
- 内置 AI 问书：使用 DeepSeek V4 Pro，自动检索当前章与全书相关段落
- AI 回答沿用“阅读分析”框架：论证链、隐含前提、暗线、联想与反例

## 快速开始

本项目使用 [uv](https://docs.astral.sh/uv/) 管理依赖。

**1. 启动服务**

先配置 DeepSeek API Key（`.env` 已被 Git 忽略）：

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

```bash
uv run server.py
```

或使用一键启动脚本：

```bash
start.bat
```

**2. 导入书籍**

![homepage](/image/import-book.jpg)

**3. 打开浏览器**

访问 [localhost:8123](http://localhost:8123/) 即可看到书库。

## AI辅助功能

正文右侧点击 `Ai` 即可直接问书。服务端使用 `deepseek-v4-pro`，不会把 API Key 下发到浏览器；每次请求会优先检索与问题相关的章节，并限制并发与每小时请求次数。

![AI tools](/image/AI-tools.jpg)

点击右下角图标，自动复制当前章节内容，并拼接为提示词。然后就可以发送给喜欢的AI模型，帮助理解本章内容。

也可以自定义提示词：

![prompt-settings](/image/prompt-settings.jpg)

## License

MIT
