# 部署与故障处理

## 部署拓扑

- 生产入口：`https://reader.shendongchao.me`
- SSH：`ssh aliyun-ecs`
- 远端仓库：`/opt/reader3-booklens`
- 容器：`reader3-booklens`
- 宿主监听：`127.0.0.1:8123`
- 外部访问由反向代理和 Cloudflare Access 提供。

不要把真实 API Key、SSH 私钥或 Cloudflare 凭据写进仓库。

## 标准发布

先在本地验证：

```bash
uv sync
uv run pytest -q
docker compose config
```

确认工作区只包含本次改动，再同步已提交版本到服务器。在服务器执行：

```bash
cd /opt/reader3-booklens
docker compose up --build -d
docker compose ps
curl -fsS http://127.0.0.1:8123/ >/dev/null
```

应用没有专用 `/health` 路由，根页面成功返回是当前最小存活检查。随后在受 Cloudflare Access 保护的生产页面验证书架、正文、搜索和一次 AI 流式回答。

## AI 流式验收

合格条件：

- HTTP 200，`Content-Type` 包含 `text/event-stream`。
- 响应先出现一个或多个 `token`，最后出现且只出现一个 `done`。
- 正常链路没有 `error`；浏览器在回答过程中逐步更新，而不是结束后一次性出现。
- 页面和网络响应均不包含 API Key 或上游推理内容。

## 常见故障

### AI 按钮可用但请求返回 503

容器内没有 `DEEPSEEK_API_KEY`。检查 Compose 环境变量是否注入，修正 `.env` 后重建容器。不要在命令输出或工单中打印密钥。

### 生产域名返回登录页或重定向

这是 Cloudflare Access 的预期行为，不能用未认证的公网 `curl` 判断应用故障。先 SSH 到服务器，访问 `127.0.0.1:8123`，再通过已登录浏览器做端到端验证。

### AI 回答卡住或中断

检查浏览器是否收到 `token`、`done` 或 `error`；再看容器日志：

```bash
docker logs --tail 200 reader3-booklens
```

上游超时、额度、限流和客户端断开是不同故障，不要统一归因于前端。进程内并发为 2、单 IP 每小时 20 次，重启会清空计数。

### 书架为空

确认容器内 `/app/book` 有 `*_data/book.pkl`，并检查宿主 `./book` 是否正确挂载。不要从不可信来源复制 pickle 文件。

## 热修复边界

`docker cp` 加重启只适合止血，不能作为正式发布。若确需使用，必须把同一改动同步回 Git、跑完整测试并尽快执行标准重建，否则容器重建会丢失修复。

## 回滚

回滚到上一已验证 Git 提交，重新执行 `docker compose up --build -d`。`book/` 是挂载数据，不应随代码回滚删除；涉及解析格式变化时先备份数据并单独制定迁移方案。
