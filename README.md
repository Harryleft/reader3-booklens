# BookLens

![homepage](/image/homepage.jpg)

一个轻量级的自托管 EPUB 阅读器，让你逐章阅读 EPUB 电子书，并将章节内容一键复制给 LLM 进行共读分析。

灵感来源于 [reader3](https://github.com/karpathy/reader3)，在此基础上增加了导入页面、提示词模板系统等功能。

## 功能

- 逐章阅读 EPUB 电子书，支持目录导航
- 浮动按钮一键复制章节内容，自动用提示词模板包裹
- 内置提示词模板 + 自定义模板管理
- Web 端导入页面，支持拖拽上传 EPUB 文件，自动解析入库
- 自动提取书籍元数据（标题、作者、目录结构、图片）

## 快速开始

本项目使用 [uv](https://docs.astral.sh/uv/) 管理依赖。

**1. 处理 EPUB 文件**

```bash
uv run reader3.py <你的文件.epub>
```

**2. 启动服务**

```bash
uv run server.py
```

或使用一键启动脚本：

```bash
start.bat
```

**3. 打开浏览器**

访问 [localhost:8123](http://localhost:8123/) 即可看到书库。你也可以直接在网页上通过 `/import` 页面拖拽上传 EPUB 文件。

## 书籍管理

- 处理后的书籍存放在 `book/` 目录下
- 删除书籍：直接删除 `book/` 下对应的 `*_data` 文件夹即可
- 添加书籍：命令行运行 `uv run reader3.py <file.epub>` 或通过网页导入

## AI辅助功能

![AI tools](/image/AI tools.jpg)

点击右下角图标，自动复制当前章节内容，并拼接为提示词。然后就可以发送给喜欢的AI模型，帮助理解本章内容。

也可以自定义提示词：

![prompt-settings](/image/prompt-settings.jpg)

## License

MIT
