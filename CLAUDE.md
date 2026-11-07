# Sibisi Ramen 菜单网站

Valencia 的 Sibisi Ramen（食必思）三语（西 / 英 / 中）手机菜单。GitHub Pages 发布：https://hao1992.github.io/sibisi/

## 结构
- `index.html` — 线上页面，**由脚本生成，不要手改**
- `img/` — 菜品照片，按菜号命名（`2-5.jpg`），800×800 JPG
- `source/data.py` — 菜品、价格、过敏原、口味、加配菜、饮料、推荐搭配、界面文字
- `source/det.py` — 每道菜点开后的详细介绍（zh / es / en）
- `source/app.js.tpl`、`head2.part`、`illo.part` — 页面逻辑、样式、无照片时的示意插画
- `source/build.py` — 生成 `index.html`

## 电话号码
店里的电话**只在 `data.py` 的 `TEL` 里写一次**。页脚显示的分组号码（`TELTXT`，去 +34、按 3-3-3 分）、
`tel:` 链接、复制按钮全都从它推出来。`build.py` 末尾有防回归检查：号码要是又被写死进任何模板，构建直接失败。
`head2.part` 现在也做 token 替换，但只认 `__TELRAW__` / `__TELTXT__` 这两个（原样插入，不走 JSON）；
要加新 token 得在 `build.py` 那个 head 的循环里加。

## 改动流程
1. 改 `source/data.py` 或 `source/det.py`（价格是 `d("菜号", 中文名, 西语名, 英文名, 价格, ...)` 的第 5 个参数）
2. `python3 source/build.py`，输出里 `missing images` 应为 `none`
3. 用 grep 核对 `index.html` 里确实是新值，再 `git commit` + `git push`
4. Pages 部署需 1–3 分钟；查看时可加 `?v=数字` 绕过缓存

## 统计
- `collector/` 是 Cloudflare Worker + D1 的事件收集器，**不是网页的一部分**（跟着 Pages 一起发布，但没人会去访问）
- 菜单这边只有一个开关：`source/data.py` 的 `STATS`。留空就一个请求都不发
- 第 0 期（会话层）：`open`（带初始语言）、`lang`（切语言）、`staff`（点了「给服务员看」）
- 第 1 期（菜品层）：`imp`（卡片露出一半停 1 秒）、`det`（点开详情）、
  `add`（加进清单，套餐带进去的也算）、`pair`（走的是「推荐搭配」按钮）、`combo`（多人套餐）、`drink`（饮料）
- 第 1.5 期（来源）：`imp` / `det` / `add` / `drink` 都带 `src`，记这一下发生在哪个区域：
  `menu` 菜单正文、`luck` 节气推荐、`first` 顶层推荐、`hero` 首屏按钮、`det` 详情页里、
  `pairbox` 详情页「整套加入」带进去的、`order` 结算前加点、`pick` 加小菜/饮料全屏列表、
  `pack` 多人套餐、`drinks` 酒水单。**同一道菜从节气推荐进清单和从菜单正文进清单，含义完全不一样**
- `imp` 的去重键是「菜 + 来源」，所以一道菜在节气框和菜单正文各算一次露出；
  要是只按菜号去重，从节气框加的菜会被算进菜单正文的转化率里
- 会话 id 只在内存里，统计不写 cookie 也不写 localStorage；IP 不入库
- 加新事件时在 `worker.js` 的 `NAMES` 白名单里同步加，否则会被服务端丢掉；
  新增区域要三处同步：`app.js.tpl` 的 `SRC`、`worker.js` 的 `SRCS`、`_report.py` 的 `SRCN`
- 页面上任何新的「加进清单」入口，容器 id 必须进 `SRC` 表，否则来源会落成空值
- 已部署：`https://sibisi-stats.cartaviva.workers.dev`，`STATS` 已填，线上在收数据
- 看报表：`collector/stats.sh`（口令在 macOS 钥匙串里，服务名 `sibisi-stats-token`）
- 原始事件只留 90 天，Worker 每天定时清理一次
- 细节见 `collector/README.md`

## 新照片
裁成正方形、去雾提亮、暖色、轻锐化，存成 `img/<菜号>.jpg`，然后在 `data.py` 对应菜加 `img="<菜号>"`。

## 规则
- 菜号是稳定的点单依据，不要改菜号
- 三种语言内容必须一致；改一种语言时同步另外两种
- 过敏原（G 麸质、H 鸡蛋、S 大豆、Sé 芝麻、P 鱼类、M 菌菇）每道菜都要准确；拿不准时宁可多标，并问店主
- 推荐搭配是**另收费**的加点，不能写得像套餐赠送
- 不要写店里没有的食材或做法；涉及做法的新描述先让店主确认
- 先改中文给 Hao 审核，确认方向后再同步西语 / 英语
