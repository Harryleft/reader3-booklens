# 集成与 API

## 配置

唯一必需的 AI 配置：

```dotenv
DEEPSEEK_API_KEY=replace-with-your-deepseek-api-key
```

本地运行会读取仓库根目录 `.env`，但不会覆盖进程中已有的同名环境变量。Docker Compose 从宿主机 `.env` 注入变量。

## 页面与接口

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/` | 书架 |
| `GET` | `/import` | 导入页面 |
| `POST` | `/api/upload` | 上传并解析 EPUB |
| `GET` | `/read/{book_id}` | 跳转到第一章 |
| `GET` | `/read/{book_id}/{chapter_index}` | 阅读章节 |
| `GET` | `/read/{book_id}/images/{image_name}` | 书内图片 |
| `GET` | `/api/search-book` | 搜索全书标题与正文 |
| `POST` | `/api/ask-book` | AI 问书 SSE |

### 全书搜索

```http
GET /api/search-book?book_id=<id>&q=<关键词>&limit=20
```

`q` 最长 80 字符，`limit` 为 1–30。每章最多返回一个结果，包含章节序号、标题、短摘要和命中数。

### AI 问书

请求示例：

```json
{
  "book_id": "example_data",
  "chapter_index": 3,
  "scope": "selected",
  "chapter_indices": [2, 3, 4],
  "question": "作者的论证链是什么？",
  "history": [],
  "analysis_prompt": null
}
```

`scope` 可为 `current`、`selected` 或 `book`。`selected` 必须传入 1–12 个有效章节序号。响应类型为 `text/event-stream`，事件协议见[架构文档](architecture.md#ai-问书链路)。客户端必须同时处理 HTTP 错误、`error` 事件和连接在 `done` 前中断。

## 安全约束

- `book_id` 只接受单个路径段，服务端会拒绝路径穿越。
- 用户自定义提示词最长 6,000 字符，只控制分析风格；服务端安全消息始终先于它。
- 书籍正文被视为不可信数据，不能改变系统角色或要求泄密。
- AI 只应基于检索出的原文回答；证据不足时应明确说明。
- API Key 不写入页面、响应、测试夹具或日志。

## 扩展原则

新增能力优先沿用现有边界：页面状态留在浏览器，书籍处理留在 `reader3.py`，服务端集成留在 `server.py`。只有出现真实的多用户、跨设备同步或搜索规模问题时，才引入数据库或独立前端。
