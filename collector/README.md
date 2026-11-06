# 菜单统计

## 记哪些事件

**第 0 期 · 会话层**

| 事件 | 什么时候发 | 带什么 |
|---|---|---|
| `open` | 菜单渲染完 | 初始语言（`es` / `en` / `zh`） |
| `lang` | 客人点了语言按钮 | 切到哪个语言 |
| `staff` | 客人点了「给服务员看」 | — |

**第 1 期 · 菜品层**

| 事件 | 什么时候发 | 带什么 |
|---|---|---|
| `imp` | 卡片露出一半**并停留 1 秒** | 菜号 |
| `det` | 点开菜品详情 | 菜号 |
| `add` | 加进清单（含套餐、推荐搭配带进去的） | 菜号 |
| `pair` | 走的是详情页「推荐搭配」那个按钮 | 菜号 |
| `combo` | 加了多人套餐 | 套餐 id |
| `drink` | 加了饮料 | 饮料 id |

`imp` 的口径是有意卡严的：划过去不算，一道菜一个会话只记一次。
三层用的是同一批会话，相除才有意义——「看到的人里有多少点开」「看到的人里有多少加进清单」。
按次数算的话，同一个人反复点同一道菜就会把分子撑大。

`staff` 是目前最接近「成单」的信号。它不等于成单：客人可能看完改主意，服务员也可能录成别的。
真实销量在店里那套 POS 里，这边拿不到。同理，`add` 是「进了清单」，不是「卖出去了」。

## 收了什么、没收什么

**收：** 会话 id（随机生成，只存在那台手机的内存里，页面一关就没了）、事件名、初始语言、屏幕宽度（按 60px 分桶）、国家代码、服务端收到的时间。

**不收：** IP（Worker 能看到，代码里明确不写入库）、精确位置、User-Agent、任何自由文本、任何能认出是谁的东西。

**不写 cookie，也不写 localStorage。** 所以不需要 cookie 横幅。菜单本身用 localStorage 存客人的清单和语言偏好，那是客人主动要求的功能，和统计是两回事，统计这部分一个字节都不往设备上写。

浏览器开了 Do Not Track 或 Global Privacy Control 的，直接不上报。

**保留期：** 原始事件留 90 天。Worker 每天 04:17 UTC 跑一次定时任务自动删掉过期的，
代码在 `worker.js` 的 `scheduled()` 里，天数是 `KEEP_DAYS`。按天聚合的长期趋势留给第 2 期的报表页。

## 已经部署好了

2026-11-05 部署完成，现在是活的：

| | |
|---|---|
| Worker | `https://sibisi-stats.cartaviva.workers.dev` |
| 收集口 | `/c`（已填进 `source/data.py` 的 `STATS`） |
| 报表口 | `/s?k=<TOKEN>&d=<天数>` |
| D1 数据库 | `sibisi` |
| 定时清理 | 每天 04:17 UTC |

`TOKEN` 存在 macOS 登录钥匙串里，服务名 `sibisi-stats-token`，`stats.sh` 会自己去取。
要在别的机器上看数据，用「钥匙串访问」把它复制出来。

改了 `worker.js` 之后重新部署：

```bash
cd ~/git/sibisi/collector && npx wrangler deploy
```

**从零再来一遍的话**（换账号、或者要在别的项目复刻）：

```bash
npx wrangler login
npx wrangler d1 create sibisi          # 把打印的 database_id 填进 wrangler.toml
npx wrangler d1 execute sibisi --remote --file=./schema.sql
T=$(openssl rand -hex 24)
printf '%s' "$T" | npx wrangler secret put TOKEN
security add-generic-password -U -a sibisi-stats -s sibisi-stats-token -w "$T"
npx wrangler deploy
```

新账号第一次用 Workers，要先在面板上打开一次 Workers & Pages 页面，
Cloudflare 才会分配 `*.workers.dev` 子域名，否则 `deploy` 会报 subdomain 不可用。
新子域名的 TLS 证书签发要一两分钟，这期间 curl 会报 handshake failure，等一下就好。

## 看数据

```bash
~/git/sibisi/collector/stats.sh
```

默认最近 14 天。`stats.sh 7` 看 7 天，`stats.sh 90 raw` 出原始 JSON。
口令它自己从钥匙串取，不用手输，也不会进 shell 历史。

输出里**「开菜单时的语言」这一项，直接回答了要不要加第四种语言**，
不用再靠瓦伦西亚的游客统计去猜。

## 本地调试

```bash
npx wrangler d1 execute sibisi --local --file=./schema.sql
```

```bash
npx wrangler dev --port 8787 --local
```

本地调试时把菜单的来源加进 `wrangler.toml` 的 `ORIGIN`（逗号分隔），比如 `http://127.0.0.1:8814`。`.dev.vars` 里放本地用的 `TOKEN`，这个文件不进 git。

## 免费额度够不够

Workers 每天 10 万请求，D1 每天 10 万行写入、5 GB 存储。

按每天 60 桌扫码、第 1 期全开估算：一个会话从头翻到尾大约 40 个事件
（35 道菜的曝光 + 点开和加入），批量发送后约 1–2 个请求。

| | 每天用掉 | 免费额度 | 占比 |
|---|---|---|---|
| Workers 请求 | ~120 | 100,000 | 0.1% |
| D1 写入行数 | ~2,400 | 100,000 | 2.4% |
| D1 存储 | 90 天累计约 17 MB | 5 GB | 0.3% |

生意翻十倍也还在免费额度内。真要逼近上限，先调 `app.js.tpl` 里 `dishSpy` 的停留门槛
（现在 1 秒），把「划过去」滤得更狠。

## 已知的坑

- **收集口是公开的，挡不住有人拿 curl 直接灌数据。** Worker 会校验来源头（挡住别的网站的浏览器）、字段白名单和大小上限，但公开端点没有真正的办法杜绝伪造。小店的菜单，这个风险可以接受；真被灌了，数据能按时间段删掉重来。
- **只看得见扫码的人。** 没扫码、直接问服务员的客人完全不在数据里，而且扫码的人本身偏年轻、偏外国人。拿这份数据下「哪道菜最受欢迎」的结论，只对扫码客群成立。
- **样本小。** 一天几十桌，单项指标一周可能只有十几个数据点，别过度解读。
