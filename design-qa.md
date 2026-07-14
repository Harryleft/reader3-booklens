# Design QA

## Visual truth and evidence

- Source visual truth: `output/qa/ai-panel-before-resize-redesign.png`，来自生产阅读页 928 × 863 视口。
- Implementation screenshots:
  - `output/qa/ai-panel-production-928x863.png`
  - `output/qa/ai-panel-after-resize-redesign-928x863.png`
  - `output/qa/ai-settings-after-redesign-928x863.png`
  - `output/qa/reader-topbar-tools-928x863.png`
- Combined comparison: `output/qa/ai-panel-resize-redesign-comparison.png`，左右两图均来自同一生产书籍页面、均为 928 × 863，同高并排。

## Full-view comparison

- AI 侧栏仍是独立右栏，不覆盖正文；928 px 视口下默认宽 360 px，正文、顶栏右边界与侧栏左边界均为 568 px。
- AI 主界面只保留标题、紧凑问书范围、消息区和输入框，删除了书名、模型、提示词预览、三条问题胶囊和三枚快捷按钮。
- 阅读工具从正文右侧竖排改为顶栏中部工具区；在 928 px 下打开侧栏时隐藏，在更大桌面视口下随剩余阅读区居中避让，不覆盖书名、顶部导航或侧栏。
- 侧栏宽度、正文 margin 与顶栏宽度使用同一 CSS 变量同步变化，拖动时不产生覆盖、空隙或横向滚动。

## Focused-region comparison

- AI header: 只显示“AI 问书”，右侧仅保留设置与关闭。
- Scope: 收起态固定 48 px，只显示“问书范围”和当前模式；章节详情及 current / selected / book 控件只在展开后出现。
- Prompt configuration: 阅读分析提示词迁入右上角设置覆层，保留默认/自定义状态、字数限制、保存和恢复默认；设置页与问书范围互斥。
- Resize handle: 桌面端左边缘可拖动，范围为 320 px 到 `min(900px, viewport - 360px)`；支持方向键、Shift 加速、Home 恢复默认和双击恢复默认。
- Responsive: 899 px 下侧栏为全屏抽屉、拖动手柄隐藏、正文 margin 清零；回到 928 px 后恢复已保存的桌面宽度。

## Primary interactions tested

- 928 × 863：打开/关闭 AI，验证标题、快捷内容删除、48 px 范围入口和无横向溢出。
- 生产页拖动左侧手柄后，AI 侧栏 360 px → 439 px；正文与顶栏边界同步到 489 px，松手后拖动状态正确结束。
- 刷新页面后侧栏保持 439 px；键盘 Shift+Left 增宽 64 px、Home 恢复默认均生效。
- 899 px：侧栏宽度等于视口、手柄不可见、正文无残留右边距；恢复桌面尺寸后读取桌面宽度。
- AI 设置打开时提示词文本框可见，问书范围自动收起；再打开范围时设置页自动关闭。
- 1280 px：AI 打开时顶部工具区居中于剩余阅读区，不与书名、顶部导航或 AI 侧栏重叠。
- 浏览器控制台 error / warning 为 0。

## Required surfaces

- Typography: passed — 保留阅读页既有中文字体、正文尺度与行高。
- Spacing and layout: passed — 顶栏、正文、AI 侧栏三者同步重排；设置页与输入区均可达。
- Colors: passed — 延续灰白阅读背景、浅灰分隔线和蓝色交互反馈。
- Imagery/icons: passed — 无新增图片资产，继续复用 Bootstrap Icons。
- Copy: passed — 删除不必要信息，范围、设置和输入提示保持简洁明确。

## Automated checks

- Python tests: 26 passed.
- Rendered inline JavaScript: `node --check` passed.
- Rendered markup: 无 `DeepSeek V4 Pro`、`.question-prompt`、`.suggestion`，包含 `#ai-resizer` 与 `#ai-settings-toggle`。
- Patch whitespace: `git diff --check` passed.

final result: passed

---

# 阅读笔记功能下线

- 已删除顶部“阅读笔记”入口、笔记侧栏及全部笔记样式、事件监听和 `booklens-notes-*` 本地存储代码。
- Production toolbar: `目录 / AI 问书 / 字号与字体 / 深浅色转换`。
- Production verification: 不存在 `[data-action="notes"]`、`#notes-sheet` 或笔记存储初始化代码；无横向溢出。
- Production screenshot: `output/qa/reader-without-notes-production.png`。
- Browser console error / warning: 0。
- Automated tests: 27 passed；渲染后 JavaScript `node --check` passed；`git diff --check` passed。

final result: passed

---

# 顶栏与正文对齐修正

## Visual truth and evidence

- Source visual truth: `/var/folders/lx/t6z2k7w56sgg59d46wk3_2d40000gn/T/codex-clipboard-6f30fdff-7bb0-4a2e-97bd-e2fe9f38102e.png`，原图 3600 × 2016，对应逻辑视口 1800 × 1008。
- Local implementation screenshot: `output/qa/header-aligned-local-1800x1008.png`。
- Production implementation screenshot: `output/qa/header-aligned-production-1800x1008.png`。
- Same-viewport comparison: `output/qa/header-alignment-comparison.png`，参考图与本地实现均按 1800 × 1008 同高并排。

## Finding and correction

- P1: 顶部工具区原先是独立的 fixed 覆层，左右边框与顶栏分隔线叠加，视觉上把顶栏切成三个互不相属的块。
- P1: 正文滚动容器只在右侧占用滚动条宽度，顶栏和正文使用不同的水平基准，导致左右边界出现轻微漂移。
- Correction: 将工具区移动到 `.topbar` 内部，顶栏统一为“书名 / 工具 / 导航”三栏网格；桌面端移除工具区独立边框、背景和阴影。
- Correction: `#main` 使用 `scrollbar-gutter: stable both-edges`，让正文在滚动条存在时仍保持对称的水平坐标系。
- Responsive: 901–1199 px 打开目录或 AI 侧栏时隐藏顶栏中部工具区，并让书名与导航使用剩余两栏；900 px 以下继续使用底部浮动工具条。

## Post-fix measurements

- Production viewport: 1800 × 1008。
- `.topbar`: x 330，right 1470，width 1140。
- `.content-wrap`: x 330，right 1470，width 1140。
- `.book-content`: x 330，right 1470，width 1140。
- `.toolbar`: x 760，right 1040，width 280；父元素为 `.topbar`；左右边框均为 0 px。
- `body.scrollWidth` 与 `html.scrollWidth` 均为 1800，无横向溢出。
- 928 × 863 回归：AI 打开时正文与侧栏仍同步重排，工具区隐藏，书名完整显示，无横向溢出。
- Production browser console error / warning: 0。

## Automated checks

- Python tests: 26 passed。
- Rendered inline JavaScript: `node --check` passed。
- Patch whitespace: `git diff --check` passed。

final result: passed
