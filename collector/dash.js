// 看板。从 /r 的原始计数算出一整页 HTML，跑在 Worker 里，所以打开就是当下的数字。
//
//   GET /d?k=口令        最近 14 天
//   GET /d?k=口令&d=30   最近 30 天
//
// 分三层，改东西只动对应那一层：
//
//   1. 聚合层  `Ses` / `Bucket` / `Ctx`
//      把会话按「业务日 × 午市/晚市」归堆。只做计数，不下任何结论。
//   2. 公式层  `metric(...)` 注册的函数
//      一个指标一个函数：输入一个 Bucket，输出一个数。加指标只需在这一层加个函数，
//      卡片、走势图、和基线的对比全都自动跟着出来。
//   3. 结论层  `rule(...)` 注册的函数
//      一条结论一个函数：输入整段数据，输出一句话或者 null。阈值写在函数里，
//      所以「多少算异常」是提前定好的，不是每次看图现编一个说法。
//
// 图表只画公式层算出来的数，自己不算数。
//
// 两个口径上的硬约束，别绕过去：
//   * `ts` 是上报时间不是发生时间（见 README「已知的坑」），所以这里只用它分
//     业务日和午市/晚市，不画任何「几点人最多」。
//   * 所有比率的分子分母都按**会话**算，不按次数。同一个人反复点同一道菜
//     不会把分子撑大。
//
// 菜名和来源名在 names.gen.js 里，由 source/build.py 从 source/data.py 生成——
// Worker 读不到 data.py，所以改了菜单要重新 build + deploy，名字才跟着变（只影响显示）。
import { NAME, PRICE, DEFAULT_DRINK, SRCN, WITH_IMP } from "./names.gen.js";

const TZ = 3600;        // Valencia 冬令时 UTC+1。三月底换夏令时要改成 7200
const CUT_H = 5;        // 业务日从早上 5 点切：23:00 打烊，事件缓冲最晚 01:00 才落库
const DINNER_H = 18;    // 这个点之后开的会话算晚市（营业 12:30–16:30 / 20:00–23:00）
const DESK_W = 1000;    // 屏幕宽到这个数就不太可能是店里桌上的手机
const BASE_DAYS = 7;    // 基线取前 7 天
const DISH = /^\d+-\d+$/;

// ── 小工具 ───────────────────────────────────────────────────────────────
const C = () => Object.create(null);
const gv = (o, k) => o[k] || 0;
const bump = (o, k, n) => { o[k] = (o[k] || 0) + n; };
const K = (a, b) => a + "\u0001" + b;                 // 当「元组键」用
const keys = (o) => Object.keys(o);
// 次数从多到少。并列时按键名排，免得同样的数据两次打开排出两个顺序
const top = (o, n) => keys(o).map((k) => [k, o[k]])
  .sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1)).slice(0, n == null ? undefined : n);
const sum = (a) => a.reduce((x, y) => x + (y || 0), 0);

const div = (a, b) => (!b ? null : a / b);
const pc = (a, b) => (!b ? null : (100 * a) / b);
const ESCS = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ESCS[c]);
const fx = (v, d) => (+v).toFixed(d);
const g = (v) => String(+(+v).toFixed(6));            // Python 的 %g：去掉多余的 0
const sgn = (v, d) => (v > 0 ? "+" : "") + fx(v, d);

const WEEK = "一二三四五六日";
const ymd = (ms) => new Date(ms).toISOString().slice(0, 10);
const bizday = (ms) => ymd(ms + (TZ - CUT_H * 3600) * 1000);
const cetH = (ms) => new Date(ms + TZ * 1000).getUTCHours();
const svcOf = (ms) => (cetH(ms) >= DINNER_H ? "晚市" : "午市");
// JS 的 getUTCDay 周日是 0，挪成周一是 0
const wday = (d) => "周" + WEEK[(new Date(d + "T00:00:00Z").getUTCDay() + 6) % 7];
const short = (d) => d.slice(5);
const sname = (s) => SRCN[s] || s || "(无)";
const dname = (c) => NAME[c] || "";

// ── 1. 聚合层 ────────────────────────────────────────────────────────────

class Ses {
  // 一个会话。/r 给的是「会话 × 事件名 × 值 × 来源」的计数行，这里拼回会话。
  constructor(sid) {
    this.sid = sid;
    this.t0 = null; this.t1 = null;
    this.w = null; this.country = null; this.lang = null;
    this.nev = 0;
    this.ev = C();      // 事件名 -> 次数
    this.src = C();     // (来源, 事件名) -> 次数
    this.dish = C();    // (菜号, 事件名) -> 次数
    this.drink = C();   // 饮料 id -> 次数
    this.pack = C();    // 套餐 id -> 次数
    this.sw = 0;        // 切语言次数
  }

  feed(name, v, src, n, t0, t1, w, c) {
    this.t0 = this.t0 === null ? t0 : Math.min(this.t0, t0);
    this.t1 = this.t1 === null ? t1 : Math.max(this.t1, t1);
    if (w) this.w = Math.max(this.w || 0, w);
    if (c && !this.country) this.country = c;
    this.nev += n;
    bump(this.ev, name, n);
    if (name === "open" && v && !this.lang) this.lang = v;
    if (name === "lang") this.sw += n;
    if (name === "imp" || name === "det" || name === "add" || name === "drink") {
      bump(this.src, K(src || "(旧)", name), n);
    }
    if ((name === "imp" || name === "det" || name === "add" || name === "pair")
        && v && DISH.test(v)) {
      bump(this.dish, K(v, name), n);
    }
    if (name === "drink" && v) bump(this.drink, v, n);
    if (name === "combo" && v) bump(this.pack, v, n);
  }

  get day() { return bizday(this.t0); }
  get svc() { return svcOf(this.t0); }
  // 整个会话的事件带着同一个毫秒落库 = 缓冲一次性清空。这个会话的时刻完全不可用
  get flat() { return this.t1 === this.t0; }
  get desktop() { return (this.w || 0) >= DESK_W; }
  // 这个会话里同一道菜被连加最多的次数，[次数, 菜号]
  get maxAdd() {
    let best = [0, ""];
    for (const k of keys(this.dish)) {
      const [code, nm] = k.split("\u0001");
      if (nm === "add" && this.dish[k] > best[0]) best = [this.dish[k], code];
    }
    return best;
  }
}

// 一堆会话的计数。CTRS / INTS 列全，absorb 才能把两堆并起来不漏字段
const CTRS = ["n", "s", "srcn", "srcs", "dishn", "dishs", "drink", "pack",
              "lang", "lang_staff", "country", "width"];
const INTS = ["ses", "ev", "sw_ses", "desk", "flat", "cart_dishes", "cart_ses"];

class Bucket {
  constructor(label = "") {
    this.label = label;
    this.days = new Set();
    for (const k of CTRS) this[k] = C();
    for (const k of INTS) this[k] = 0;
  }

  take(x) {
    this.ses += 1;
    this.ev += x.nev;
    this.days.add(x.day);
    if (x.sw) this.sw_ses += 1;
    if (x.desktop) this.desk += 1;
    if (x.flat) this.flat += 1;
    // 「清单里几道菜」按**不同的菜**算，不按加入次数：有人会把同一道菜连点二十下，
    // 按次数算那一个会话就能把全店的平均值翻倍
    const inc = new Set();
    for (const k of keys(x.dish)) {
      const [code, nm] = k.split("\u0001");
      if (nm === "add" && x.dish[k]) inc.add(code);
    }
    this.cart_dishes += inc.size;
    if (inc.size) this.cart_ses += 1;
    for (const k of keys(x.ev)) {
      bump(this.n, k, x.ev[k]);
      bump(this.s, k, 1);                      // 「出现过这个事件的会话数」
    }
    for (const k of keys(x.src)) { bump(this.srcn, k, x.src[k]); bump(this.srcs, k, 1); }
    for (const k of keys(x.dish)) { bump(this.dishn, k, x.dish[k]); bump(this.dishs, k, 1); }
    for (const k of keys(x.drink)) bump(this.drink, k, x.drink[k]);
    for (const k of keys(x.pack)) bump(this.pack, k, x.pack[k]);
    const lg = x.lang || "?";
    bump(this.lang, lg, 1);
    if (gv(x.ev, "staff")) bump(this.lang_staff, lg, 1);
    bump(this.country, x.country || "??", 1);
    bump(this.width, x.w || 0, 1);
  }

  absorb(b) {
    for (const d of b.days) this.days.add(d);
    for (const c of CTRS) for (const k of keys(b[c])) bump(this[c], k, b[c][k]);
    for (const i of INTS) this[i] += b[i];
    return this;
  }

  // 给公式层用的小口子
  sv(name) { return gv(this.s, name); }             // 出现过这个事件的会话数
  nv(name) { return gv(this.n, name); }             // 这个事件发生了多少次
  seen(src) { return gv(this.srcs, K(src, "imp")); }
  added(src) { return gv(this.srcs, K(src, "add")); }
  adds(src) { return gv(this.srcn, K(src, "add")); }
  drinks(src) { return gv(this.srcn, K(src, "drink")); }
  dsv(code, name) { return gv(this.dishs, K(code, name)); }
  dnv(code, name) { return gv(this.dishn, K(code, name)); }
  // 某个事件各道菜的次数，{菜号: 次数}
  byDish(name) {
    const o = C();
    for (const k of keys(this.dishn)) {
      const [code, nm] = k.split("\u0001");
      if (nm === name) bump(o, code, this.dishn[k]);
    }
    return o;
  }
}

export function load(d) {
  const ci = {};
  d.cols.forEach((c, i) => { ci[c] = i; });
  const ses = new Map();
  for (const r of d.rows) {
    const sid = r[ci.sid];
    let s = ses.get(sid);
    if (!s) { s = new Ses(sid); ses.set(sid, s); }
    s.feed(r[ci.name], r[ci.v], r[ci.src], r[ci.n], r[ci.t0], r[ci.t1], r[ci.w], r[ci.c]);
  }
  return [...ses.values()].sort((a, b) => a.t0 - b.t0);
}

// 聚合结果 + 取数的口子。公式层和结论层都只跟它打交道。
// range = 头部那组卡片覆盖几天：1 就是「今天」，3/7/30 是「最近 N 天」
export class Ctx {
  constructor(meta, sessions, range = 1) {
    this.meta = meta;
    this.sessions = sessions;
    this.svcb = C();
    const seenKey = new Set();
    this.pairs = [];
    for (const x of sessions) {
      const k = K(x.day, x.svc);
      if (!this.svcb[k]) {
        this.svcb[k] = new Bucket(x.day + " " + x.svc);
        if (!seenKey.has(k)) { seenKey.add(k); this.pairs.push([x.day, x.svc]); }
      }
      this.svcb[k].take(x);
    }
    this.daylist = [...new Set(this.pairs.map((p) => p[0]))].sort();
    this.day = C();
    for (const d of this.daylist) this.day[d] = this.pick([d], ["午市", "晚市"]);
    this.all = this.pick(this.daylist, ["午市", "晚市"]);
    // 会话个数少于这个数的日子不是正常营业（周四休息、或者只有我自己在测），
    // 算基线时要排掉，不然一个空日子能把基线拉低一半
    this.live_days = this.daylist.filter((d) => this.day[d].ses >= 5);

    // 今天只开了午市的话，拿昨天**整天**比就是拿半天比一天。
    // 基线按今天实际有的档口取，才是同口径
    this.today_day = this.daylist.length ? this.daylist[this.daylist.length - 1] : null;
    const prev = this.daylist.filter((d) => d !== this.today_day);
    this.prev_day = prev.length ? prev[prev.length - 1] : null;
    // 最后一天只有午市，而那天本来该有晚市 = 这一天还没过完
    const here = new Set(this.pairs.filter((p) => p[0] === this.today_day).map((p) => p[1]));
    const open_svcs = ["午市", "晚市"].filter((x) => here.has(x));
    this.half_today = open_svcs.length < 2
      && ["周五", "周六", "周日"].includes(wday(this.today_day));

    this.range = range;
    if (range <= 1) {
      // 「今天」：按今天实际开过的档口取基线。今天只开了午市的话，拿昨天**整天**比
      // 就是拿半天比一天
      this.svcs = open_svcs.length ? open_svcs : ["午市"];
      this.head_days = [this.today_day];
      this.base_days = prev.filter((d) => this.live_days.includes(d)).slice(-BASE_DAYS);
      this.word = "今天";
      this.label = this.today_day + " 的" + this.svcs.join("/");
    } else {
      // 「最近 N 天」：整天对整天，所以只数正常营业的日子（会话 ≥5），
      // 周四休息和今天早上那种还没开门的半天都不算一天
      this.svcs = ["午市", "晚市"];
      this.head_days = this.live_days.slice(-range);
      const before = this.live_days.slice(0, Math.max(0, this.live_days.length - range));
      this.base_days = before.slice(-range);
      this.word = "这 " + range + " 天";
      this.label = "最近 " + range + " 天";
    }
    this.span = this.head_days.length || 1;
    this.today = this.pick(this.head_days, this.svcs);
    this.prev = this.prev_day ? this.pick([this.prev_day], this.svcs) : new Bucket();
    this.base = this.pick(this.base_days, this.svcs);
    // 「拿半天比整天」只有看「今天」时才会发生
    this.partial = range <= 1 && this.half_today;
  }

  pick(days, svcs) {
    const b = new Bucket();
    for (const d of days) for (const s of svcs) {
      const x = this.svcb[K(d, s)];
      if (x) b.absorb(x);
    }
    return b;
  }

  svcSes(day, svc) {
    const x = this.svcb[K(day, svc)];
    return x ? x.ses : 0;
  }

  raw(key, b) { return MBY[key].fn(b); }
  val(key, b) { return value(MBY[key], MBY[key].fn(b)); }

  // 头部那组卡片的值。计数型指标一律摊成「每天」，不然选了 3 天会话数看着像翻三倍
  head_val(key) {
    const m = MBY[key];
    const v = value(m, m.fn(this.today));
    return v !== null && m.per_day ? v / this.span : v;
  }

  // 基线值。同样摊成每天，不然等于拿一天去比一整周。
  // 一天基线都没有的时候要还 null——计数型指标会老老实实算出个 0，
  // 那会变成「比基线涨了 99」这种假结论
  base_val(key) {
    if (!this.base_days.length) return null;
    const m = MBY[key];
    const v = value(m, m.fn(this.base));
    return v !== null && m.per_day ? v / this.base_days.length : v;
  }
}

// ── 2. 公式层 ────────────────────────────────────────────────────────────
// 一个指标一个函数。比率一律返回 F(分子, 分母)，不直接返回百分数——
// 分母带着走，引擎才能在分母太小的时候直接不出数（而不是给出 1/1 = 100% 这种假结论）。

const F = (a, b) => ({ a, b, frac: true });
export const METRICS = [];
const MBY = C();

// o.unit    "%" 的话 F 按百分数算，空的话按比值算
// o.good    变大是好事还是坏事，只影响涨跌的颜色；"neutral" 就一直是灰的
// o.min_b   分母至少要有这么多，不够就不出数。1/1 = 100% 这种是噪声不是信号
// o.per_day 计数型指标（会话数这种）：当基线用的时候要除以天数，否则等于拿一天比一周
function metric(key, name, o, fn) {
  const m = {
    key, name, fn,
    unit: o.unit || "", dec: o.dec || 0, good: o.good || "up", note: o.note || "",
    min_b: o.min_b == null ? 10 : o.min_b, per_day: !!o.per_day,
  };
  METRICS.push(m);
  MBY[key] = m;
}

// F → 数。分母不够就返回 null，页面上显示「—」
function value(m, f) {
  if (f === null || f === undefined) return null;
  if (!f.frac) return +f;
  if (!f.b || f.b < m.min_b) return null;
  return m.unit === "%" ? (100 * f.a) / f.b : f.a / f.b;
}

const fmt = (v, m) => (v === null ? "—" : fx(v, m.dec) + m.unit);
const fracTxt = (f) => (f && f.frac ? f.a + " / " + f.b : "");

metric("ses", "扫码会话",
  { per_day: true, note: "有多少台手机打开过菜单。它是下面几乎所有比率的分母" },
  (b) => b.ses);

metric("add_rate", "建了清单",
  { unit: "%", note: "最接近点单意图的信号。不等于成单——真实销量在店里那套 POS 里" },
  (b) => F(b.sv("add"), b.ses));

metric("det_rate", "点开过详情",
  { unit: "%", note: "看了照片和介绍，说明在认真挑" },
  (b) => F(b.sv("det"), b.ses));

metric("cart", "清单里几道不同的菜",
  { unit: "道", dec: 1, min_b: 5,
    note: "不同的菜数 ÷ 建了清单的会话。按不同的菜算，不按加入次数——同一道菜连点二十下只算一道" },
  (b) => F(b.cart_dishes, b.cart_ses));

metric("menu_conv", "菜单正文 看到→加入",
  { unit: "%", note: "唯一有分母、又真的在卖货的区域" },
  (b) => F(b.added("menu"), b.seen("menu")));

metric("luck_conv", "节气推荐 看到→加入",
  { unit: "%", note: "2026-11-07 16:33 起改成进页面直接显示；在那之前要先点一下才翻开，51 个会话里 0 个点过，等于没有分母" },
  (b) => F(b.added("luck"), b.seen("luck")));

metric("first_conv", "顶层推荐 看到→加入",
  { unit: "%", note: "「第一次来点什么」那块" },
  (b) => F(b.added("first"), b.seen("first")));

metric("staff_rate", "建清单的人里给服务员看",
  { unit: "%", min_b: 6,
    note: "分母是「建了清单的」会话，不是全部会话——这个按钮在「清单」那张卡里，没建清单的人看不到它。拿全部会话当分母的话，建清单率一掉它就跟着掉，看着像按钮出了问题，其实没有" },
  (b) => F(b.sv("staff"), b.sv("add")));

metric("drink_rate", "点了饮料",
  { unit: "%", note: "饮料是毛利最高的一档" },
  (b) => F(b.sv("drink"), b.ses));

metric("drink_list", "饮料里来自酒水单",
  { unit: "%", good: "neutral", min_b: 8,
    note: "剩下的来自推荐搭配、套餐、结算前加点。这项越高，说明推荐越带不动饮料" },
  (b) => F(b.drinks("drinks"), b.nv("drink")));

metric("switch", "中途切语言",
  { unit: "%", good: "down", note: "高了说明按浏览器语言自动判断不准，客人得自己动手" },
  (b) => F(b.sw_ses, b.ses));

metric("non_es", "非西语会话",
  { unit: "%", good: "neutral", note: "这项决定要不要加第四种语言" },
  (b) => F(b.ses - gv(b.lang, "es"), b.ses));

metric("depth", "每会话翻了多少下",
  { dec: 1, note: "事件数 ÷ 会话数。10 以下基本是打开就走" },
  (b) => F(b.ev, b.ses));

metric("desk", "桌面宽度会话",
  { good: "down", per_day: true,
    note: "屏幕 ≥" + DESK_W + "px，大概不是店里桌上的手机；小样本下足够把某个区域的转化率从 0 抬到「有」" },
  (b) => b.desk);

// ── 3. 结论层 ────────────────────────────────────────────────────────────
// 一条结论一个函数：输入整段数据，输出一句话或者 null。
// 阈值提前写死在函数里，所以「多少算异常」是定好的，不是每次看图现编一个说法。

const Fin = (lv, title, text) => ({ lv, title, text });
export const RULES = [];
const rule = (fn) => { RULES.push(fn); };

rule(function _r_partial(c) {
  if (!c.partial) return null;
  return Fin("info", "今天还没过完",
    "今天是" + wday(c.today_day) + "，晚市 20:00 才开。下面的数字只含午市，"
    + "所以基线也只拿前几天的午市来比——拿半天跟整天比会凭空少一半。");
});

// 看板是活的，所以早上打开时「今天」可能才几个会话——这时候所有卡片都是「—」，
// 得直接说清楚，并且把昨天的数报出来，免得白跑一趟
rule(function _r_early(c) {
  if (c.range > 1 || c.today.ses >= 5 || !c.prev_day) return null;
  const p = c.day[c.prev_day];
  const bits = [["扫码会话", "ses"], ["建了清单", "add_rate"], ["菜单正文转化", "menu_conv"]]
    .map(([lab, key]) => lab + " " + fmt(c.val(key, p), MBY[key]))
    .join("、");
  return Fin("warn", "今天才刚开始",
    "今天（" + c.today_day + "）到现在只有 " + c.today.ses + " 个会话，店 12:30 才开门，"
    + "所以上面的卡片基本都是「—」——不是出错，是还没有分母。完整的一天看 "
    + c.prev_day + "（" + wday(c.prev_day) + "）：" + bits + "。");
});

// 「最近 30 天」在只开了一周的店里就是「最近 3 天」。标题上看不出来，得说一声
rule(function _r_short_range(c) {
  if (c.range <= 1 || c.span >= c.range) return null;
  return Fin("warn", "其实只有 " + c.span + " 个营业日",
    "你选的是最近 " + c.range + " 天，但目前只攒到 " + c.span + " 个正常营业的日子（"
    + c.head_days[0] + " 起）。卡片算的是这 " + c.span + " 天"
    + (c.base_days.length ? "" : "，再往前没有可比的日子，所以没有基线")
    + "。周四休息和还没开门的半天不算一天。");
});

rule(function _r_sample(c) {
  if (c.today.ses >= 25 || c.today.ses < 5) return null;   // 比 5 还少的归上面那条管
  return Fin("warn", c.word + "样本小",
    "只有 " + c.today.ses + " 个会话。这个量级下单项指标的涨跌基本是噪声，"
    + "看「哪个区域在卖货」那段的全期合计更稳。");
});

// 推荐区的判定。有曝光才有分母；0 加入时用 3/n 估个上限，而不是说「0%」
function reco(c, src, label) {
  const b = c.all;
  const seen = b.seen(src), add = b.added(src);
  const menu = c.val("menu_conv", b);
  const mtxt = fmt(menu, MBY.menu_conv);
  if (seen < 30) {
    return Fin("info", label + "还看不出来",
      "累计 " + seen + " 个会话看到、" + add + " 个加入。曝光不到 30 个会话，先不下结论。");
  }
  if (add === 0) {
    const cap = (3 / seen) * 100;                 // 0/n 的 95% 上限 ≈ 3/n
    return Fin("bad", label + "零转化",
      "累计 " + seen + " 个会话看到、0 个加入。按 3/n 估，真实转化率上限约 " + fx(cap, 1)
      + "%，而菜单正文是 " + mtxt + "。它占掉正文之前的一屏多，该考虑的是"
      + "合并 / 挪到正文之后 / 去掉，不是继续调推荐算法。");
  }
  const conv = (100 * add) / seen;
  if (menu && conv * 2 < menu) {
    return Fin("warn", label + "还是比正文差一截",
      seen + " 看到 → " + add + " 加入（" + fx(conv, 1) + "%），菜单正文 " + mtxt
      + "，差 " + fx(menu / conv, 1) + " 倍。有转化了，但还撑不住它占的那块位置。");
  }
  return Fin("good", label + "开始有效了",
    seen + " 看到 → " + add + " 加入（" + fx(conv, 1) + "%），和菜单正文的 " + mtxt
    + " 在一个量级。");
}

rule(function _r_luck(c) { return reco(c, "luck", "节气推荐"); });
rule(function _r_first(c) { return reco(c, "first", "顶层推荐"); });

rule(function _r_menu_move(c) {
  const t = c.val("menu_conv", c.today), b = c.base_val("menu_conv");
  if (t === null || b === null || c.today.ses < 25) return null;
  const d = t - b;
  if (Math.abs(d) < 8) return null;
  return Fin(d > 0 ? "good" : "warn", "菜单正文转化" + (d > 0 ? "变好" : "变差") + "了",
    c.word + " " + fx(t, 0) + "%，前 " + c.base_days.length + " 天同档口（"
    + c.svcs.join("/") + "）的基线 " + fx(b, 0) + "%，差 " + sgn(d, 0) + " 个百分点。");
});

// 午市和晚市是两种客群：赶时间的，和坐下来吃的。混成「今天」会把两边都看糊
rule(function _r_service_gap(c) {
  const lun = c.pick(c.live_days, ["午市"]), din = c.pick(c.live_days, ["晚市"]);
  const a = c.val("add_rate", lun), b = c.val("add_rate", din);
  if (a === null || b === null || Math.min(lun.ses, din.ses) < 20 || Math.abs(a - b) < 8) {
    return null;
  }
  return Fin("info", (b > a ? "晚市" : "午市") + "的人更愿意建清单",
    "全期午市 " + fx(a, 0) + "%（" + lun.ses + " 会话）、晚市 " + fx(b, 0) + "%（"
    + din.ses + " 会话），差 " + fx(Math.abs(a - b), 0)
    + " 个百分点。同一份代码、同一批菜，所以这两场值得分开看。");
});

// UPSELL 那几道是出餐快、毛利高的小菜，位置在清单结算前
rule(function _r_order(c) {
  const b = c.all;
  if (b.added("order") + gv(b.srcs, K("order", "drink"))) return null;
  return Fin("warn", "结算前加点没人用",
    "累计 " + b.sv("add") + " 个会话建过清单，结算前那块加点一次都没被点过。"
    + "那几道是出餐快、毛利高的小菜——要么没人滑到那儿，要么它不像个能点的东西。");
});

rule(function _r_drink_src(c) {
  const b = c.all;
  const tot = b.nv("drink");
  if (tot < 8) return null;
  const lst = b.drinks("drinks");
  const box = b.drinks("pairbox") + b.drinks("det");
  return Fin("info", "饮料是客人自己翻出来的",
    tot + " 次点饮料里 " + lst + " 次来自酒水单，推荐搭配只带出 " + box
    + " 次。酒水单在干活，推荐位没在干活。");
});

// 客人自己挑的和推荐默认选中的不是同一款时，值得核一下这两款的进价
rule(function _r_drink_margin(c) {
  const b = c.all;
  const best = top(b.drink, 1);
  if (!best.length) return null;
  const [code, n] = best[0];
  const [did, dnm, dpr] = DEFAULT_DRINK;
  if (code === did || n < 3) return null;
  const tp = PRICE[code];
  const same = tp != null && dpr != null && Math.abs(tp - dpr) < 0.01;
  return Fin("info", "最常点的和推荐默认选中的不是同一款",
    "点得最多的是 " + (dname(code) || code) + "（" + n + " 次"
    + (tp == null ? "" : "，" + fx(tp, 2) + " €") + "），而推荐搭配默认选中的是 " + dnm
    + (dpr == null ? "" : "（" + fx(dpr, 2) + " €）") + "。"
    + (same ? "两款同价，客人付一样的钱，毛利不一样，值得核一下进价。"
            : "两款不同价，先看是不是价格在起作用。"));
});

rule(function _r_switch(c) {
  const v = c.val("switch", c.all);
  if (v === null || c.all.ses < 30) return null;
  if (v > 10) {
    return Fin("warn", "切语言的人偏多",
      "全期 " + fx(v, 0) + "% 的会话中途切过语言，说明按浏览器语言自动判断不够准。");
  }
  return Fin("good", "初始语言判断是对的",
    "全期 " + c.all.ses + " 个会话里只有 " + c.all.sw_ses + " 个中途切过语言（"
    + fx(v, 0) + "%），按浏览器语言自动判断基本都判对了，这上面不用再花力气。");
});

// 「给服务员看」是非西语客人在用。一拨外国团能把它顶上去，第二天就「掉」回来。
// 所以它动了的时候，先拿基线期各语言的率套到今天的构成上，看构成解不解释得了
rule(function _r_staff_mix(c) {
  const t = c.today, b = c.base;
  if (t.ses < 25 || b.ses < 25) return null;
  const tr = pc(t.sv("staff"), t.ses), br = pc(b.sv("staff"), b.ses);
  if (tr === null || br === null || Math.abs(tr - br) < 5) return null;
  const known = keys(t.lang).filter((lg) => gv(b.lang, lg));
  const cov = sum(known.map((lg) => t.lang[lg]));
  if (cov < t.ses * 0.8) return null;             // 今天的语言在基线期没见过，套不过去
  const expn = sum(known.map((lg) => (t.lang[lg] * gv(b.lang_staff, lg)) / b.lang[lg]));
  const obs = t.sv("staff");
  const mix = ["es", "en", "zh"].filter((lg) => known.includes(lg))
    .map((lg) => lg + " " + fx(pc(b.lang[lg], b.ses), 0) + "%→"
                 + fx(pc(t.lang[lg], t.ses), 0) + "%").join("、");
  // 按百分点卡阈值在这个样本量下没意义（5 个会话和 9 个会话差 6 个百分点）。
  // 拿计数比：泊松噪声大约 sqrt(预期)，两倍以内就当没动
  const noise = 2 * Math.sqrt(Math.max(expn, 1));
  if (Math.abs(obs - expn) <= noise) {
    return Fin("info", "「给服务员看」的变化是客群变了，不是按钮变难找了",
      c.word + " " + fx(tr, 0) + "%，基线 " + fx(br, 0) + "%。但按基线期各语言自己的"
      + "使用率套到这一段的语言构成上，预期 " + fx(expn, 1) + " 个会话，实际 " + obs
      + " 个，差在噪声范围内（±" + fx(noise, 1) + "）。构成变化：" + mix
      + "。这个按钮主要是非西语客人在用，一拨外国团就能把它顶上去，第二天看着就像「掉下来了」。");
  }
  return Fin("warn", "「给服务员看」真的变了",
    c.word + " " + fx(tr, 0) + "%，基线 " + fx(br, 0) + "%。按语言构成算预期 " + fx(expn, 1)
    + " 个会话，实际 " + obs + " 个，超出噪声范围（±" + fx(noise, 1)
    + "）——构成解释不了。值得看看那个按钮是不是被什么挡住了。");
});

rule(function _r_staff_lang(c) {
  const b = c.all;
  const rows = ["es", "en", "zh"].filter((lg) => gv(b.lang, lg) >= 8)
    .map((lg) => [lg, b.lang[lg], gv(b.lang_staff, lg)]);
  const es = rows.find((r) => r[0] === "es");
  if (!es || rows.length < 2) return null;
  const esr = pc(es[2], es[1]) || 0;
  const oth = rows.filter((r) => r[0] !== "es");
  const on = sum(oth.map((r) => r[1])), os = sum(oth.map((r) => r[2]));
  const othr = pc(os, on);
  if (othr === null || esr === 0 || othr < esr * 2) return null;
  return Fin("info", "「给服务员看」是给外国人用的",
    "西语会话 " + es[1] + " 个里 " + es[2] + " 个点过（" + fx(esr, 0) + "%），非西语 "
    + on + " 个里 " + os + " 个（" + fx(othr, 0) + "%），差 " + fx(othr / esr, 1)
    + " 倍。西语客人会浏览，然后直接跟店员说话，不需要给手机看。");
});

rule(function _r_desktop(c) {
  const n = c.all.desk;
  if (!n) return null;
  const desk = c.sessions.filter((x) => x.desktop);
  const det = desk.filter((x) => gv(x.ev, "det")).length;
  const add = desk.filter((x) => gv(x.ev, "add")).length;
  return Fin("warn", "有 " + n + " 个桌面宽度的会话",
    "屏幕 ≥" + DESK_W + "px，大概不是店里桌上的手机（我自己开页面也会算进来）。其中 "
    + det + " 个点开过详情、" + add + " 个建过清单。小样本下这几个会话足够把某个区域的"
    + "转化率从 0 抬到「有」。");
});

// 有人会对着同一道菜的 + 按钮连点。按次数算的任何数字都会被这种会话撑大
rule(function _r_spam(c) {
  const bad = c.sessions.filter((x) => x.maxAdd[0] >= 5);
  if (!bad.length) return null;
  let worst = bad[0];
  for (const x of bad) if (x.maxAdd[0] > worst.maxAdd[0]) worst = x;
  const [n, code] = worst.maxAdd;
  const srcs = keys(worst.src).filter((k) => k.split("\u0001")[1] === "add")
    .map((k) => sname(k.split("\u0001")[0])).join("、") || "不明";
  return Fin("warn", "有 " + bad.length + " 个会话把同一道菜连加了 5 次以上",
    "最多的那个在 " + worst.day + worst.svc + "：" + code + " " + dname(code) + " 连加 "
    + n + " 次，来源是" + srcs + "，整个会话一共 " + gv(worst.ev, "add")
    + " 次加入。所以这个页面所有转化率都按「会话」算；只有「加入次数」那一列会被这种"
    + "会话撑大，看的时候对着会话数一起看。");
});

rule(function _r_flush(c) {
  const n = c.all.flat, tot = c.all.ses;
  if (!n) return null;
  return Fin("info", "时段分析做不了（口径问题，不是数据问题）",
    n + " / " + tot + " 个会话的全部事件带着同一个毫秒落库——事件先攒在队列里，攒到 40 条"
    + "或者页面被关掉才发一次，所以 ts 是「上报时间」不是「发生时间」。这个页面因此只用它"
    + "分业务日和午市/晚市，不画「几点人最多」。");
});

rule(function _r_top_dish(c) {
  const t = c.today.byDish("add");
  if (!keys(t).length) return null;
  const prev = c.base.byDish("add");
  const old = new Set(top(prev, 5).map((r) => r[0]));
  const fresh = top(t, 3).map((r) => r[0]).filter((k) => !old.has(k) && !gv(prev, k));
  const [code, n] = top(t, 1)[0];
  let txt = c.word + "加得最多的是 " + code + " " + dname(code) + "（" + n + " 次）。";
  if (fresh.length) {
    txt += "没在上一段前五里出现过的新面孔："
      + fresh.map((k) => k + " " + dname(k)).join("、") + "。";
  }
  return Fin("info", c.word + "的菜品榜", txt);
});

// ── 4. 画图 ──────────────────────────────────────────────────────────────
// 图表只认公式层算出来的数。这里没有任何业务判断，纯粹是把数字摆成形状。

const C_LUNCH = "#e0962f", C_DINNER = "#4a6fa5";
const C_LINE = ["#c0392b", "#2e7d52", "#8a63b8"];
const C_LANG = { es: "#c0392b", en: "#2e7d52", zh: "#4a6fa5", "?": "#9a9a9a" };

// y 轴顶端取个整数，不然刻度上全是 37、74 这种数
function nice(v) {
  if (v <= 5) return 5;
  const e = Math.pow(10, Math.floor(Math.log10(v)));
  for (const mul of [1, 2, 2.5, 5, 10]) if (v <= mul * e) return Math.round(mul * e);
  return Math.round(10 * e);
}

const legend = (series) => series
  .map(([nm, col]) => '<span class="lg"><i style="background:' + col + '"></i>' + esc(nm) + "</span>")
  .join("");

const chwrap = (svg, series, note) => '<div class="chwrap">' + svg
  + '<div class="legend">' + legend(series) + "</div>"
  + (note ? '<p class="note">' + esc(note) + "</p>" : "") + "</div>";

// 堆叠柱状图。series: [[名字, 颜色, [每天的值]]]
function svgStack(days, series, note, h = 190) {
  const n = days.length;
  if (!n) return "";
  const pl = 36, pb = 40, pt = 16;
  const slot = Math.max(46, Math.min(104, Math.floor(820 / n)));
  const bw = Math.floor(slot * 0.58);
  const gap = slot - bw;
  const w = pl + n * slot + 12;
  const tp = nice(Math.max(...days.map((_, i) => sum(series.map((s) => s[2][i]))), 1));
  const Y = (v) => pt + (h - pt - pb) * (1 - v / tp);
  const p = ['<svg viewBox="0 0 ' + w + " " + h + '" class="ch" style="max-width:' + w
    + 'px" preserveAspectRatio="xMinYMid meet" role="img">'];
  for (const q of [0, 0.5, 1]) {
    const v = tp * q;
    p.push('<line class="gl" x1="' + (pl - 4) + '" y1="' + fx(Y(v), 1) + '" x2="' + (w - 6)
      + '" y2="' + fx(Y(v), 1) + '"/>');
    p.push('<text class="ax" x="' + (pl - 8) + '" y="' + fx(Y(v) + 4, 1)
      + '" text-anchor="end">' + g(v) + "</text>");
  }
  days.forEach((d, i) => {
    const x = pl + i * (bw + gap);
    let acc = 0;
    for (const [nm, col, vals] of series) {
      const v = vals[i] || 0;
      if (v) {
        p.push('<rect x="' + x + '" y="' + fx(Y(acc + v), 1) + '" width="' + bw
          + '" height="' + fx(Math.max(1, Y(acc) - Y(acc + v)), 1) + '" fill="' + col
          + '" rx="2"><title>' + esc(short(d)) + " " + esc(nm) + " " + g(v) + "</title></rect>");
      }
      acc += v;
    }
    if (acc) {
      p.push('<text class="vl" x="' + fx(x + bw / 2, 1) + '" y="' + fx(Y(acc) - 5, 1)
        + '" text-anchor="middle">' + g(acc) + "</text>");
    }
    p.push('<text class="ax" x="' + fx(x + bw / 2, 1) + '" y="' + (h - pb + 18)
      + '" text-anchor="middle">' + esc(short(d)) + "</text>");
    p.push('<text class="ax2" x="' + fx(x + bw / 2, 1) + '" y="' + (h - pb + 32)
      + '" text-anchor="middle">' + esc(wday(d)) + "</text>");
  });
  p.push("</svg>");
  return chwrap(p.join(""), series, note);
}

// 折线图。null 会把线断开，不会假装是 0
function svgLines(days, series, note, unit = "%", h = 210) {
  const n = days.length;
  if (n < 2) return "";
  const pl = 40, pr = 14, pb = 40, pt = 16;
  const step = Math.max(56, Math.min(130, Math.floor(760 / (n - 1))));
  const w = pl + (n - 1) * step + pr + 14;
  const flat = [];
  for (const [, , vals] of series) for (const v of vals) if (v !== null) flat.push(v);
  const tp = nice(Math.max(...flat, 1));
  const X = (i) => pl + i * step;
  const Y = (v) => pt + (h - pt - pb) * (1 - v / tp);
  const p = ['<svg viewBox="0 0 ' + w + " " + h + '" class="ch" style="max-width:' + w
    + 'px" preserveAspectRatio="xMinYMid meet" role="img">'];
  for (const q of [0, 0.25, 0.5, 0.75, 1]) {
    const v = tp * q;
    p.push('<line class="gl" x1="' + (pl - 4) + '" y1="' + fx(Y(v), 1) + '" x2="' + (w - 8)
      + '" y2="' + fx(Y(v), 1) + '"/>');
    p.push('<text class="ax" x="' + (pl - 8) + '" y="' + fx(Y(v) + 4, 1)
      + '" text-anchor="end">' + g(v) + "</text>");
  }
  days.forEach((d, i) => {
    p.push('<text class="ax" x="' + fx(X(i), 1) + '" y="' + (h - pb + 18)
      + '" text-anchor="middle">' + esc(short(d)) + "</text>");
    p.push('<text class="ax2" x="' + fx(X(i), 1) + '" y="' + (h - pb + 32)
      + '" text-anchor="middle">' + esc(wday(d)) + "</text>");
  });
  for (const [nm, col, vals] of series) {
    let seg = [];
    const flush = () => {
      if (seg.length > 1) {
        p.push('<polyline class="pl" stroke="' + col + '" points="'
          + seg.map((q) => fx(q[0], 1) + "," + fx(q[1], 1)).join(" ") + '"/>');
      }
      seg = [];
    };
    vals.forEach((v, i) => { if (v === null) flush(); else seg.push([X(i), Y(v)]); });
    flush();
    vals.forEach((v, i) => {
      if (v === null) return;
      p.push('<circle cx="' + fx(X(i), 1) + '" cy="' + fx(Y(v), 1) + '" r="3.5" fill="'
        + col + '"><title>' + esc(short(days[i])) + " " + esc(nm) + " " + fx(v, 1) + unit
        + "</title></circle>");
    });
    const last = vals.map((v, i) => [i, v]).filter((q) => q[1] !== null).pop();
    if (last) {
      p.push('<text class="vl" x="' + fx(X(last[0]) + 7, 1) + '" y="' + fx(Y(last[1]) + 4, 1)
        + '" fill="' + col + '">' + fx(last[1], 0) + unit + "</text>");
    }
  }
  p.push("</svg>");
  return chwrap(p.join(""), series, note);
}

// 横条。rows: [[标签, 数值, 右边那行小字]]。CSS 画的，比 SVG 清楚
function hbars(rows, unit = "", widthOf = null, dec = 0) {
  if (!rows.length) return '<p class="note">没有数据</p>';
  const tp = Math.max(...rows.filter((r) => r[1] !== null).map((r) => Math.abs(r[1])), 1e-9);
  const out = ['<div class="bars">'];
  for (const [lab, v, sub] of rows) {
    const pw = v === null ? 0 : Math.max(1.2, (widthOf ? widthOf(v) : v / tp) * 100);
    const zero = v === 0;
    out.push('<div class="row"><div class="lab">' + esc(lab) + "</div>"
      + '<div class="track"><div class="fill' + (zero ? " zero" : "") + '" style="width:'
      + fx(pw, 1) + '%"></div></div>'
      + '<div class="val">' + (v === null ? "—" : zero ? "0" + unit : fx(v, dec) + unit)
      + "</div>" + '<div class="sub">' + esc(sub) + "</div></div>");
  }
  out.push("</div>");
  return out.join("");
}

// ── 5. 组页面 ────────────────────────────────────────────────────────────

const CSS = `
*{box-sizing:border-box}
:root{--bg:#f6f5f2;--card:#fff;--fg:#1d1d1f;--mut:#6c6c73;--line:#e4e2dc;
 --good:#1f7a4d;--bad:#c0392b;--warn:#a9741a;--info:#42618f;--accent:#c0392b}
@media (prefers-color-scheme:dark){:root{--bg:#14151a;--card:#1c1e24;--fg:#e9e9ec;
 --mut:#9b9ba4;--line:#2b2e36;--good:#56c48c;--bad:#f0837a;--warn:#e0b355;
 --info:#8fb0e8;--accent:#f0837a}}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,
 BlinkMacSystemFont,"Helvetica Neue","PingFang SC","Hiragino Sans GB",sans-serif}
.wrap{max-width:1060px;margin:0 auto;padding:22px 16px 70px}
h1{font-size:21px;margin:0 0 4px}
h2{font-size:16px;margin:34px 0 12px;padding-bottom:7px;border-bottom:1px solid var(--line)}
h3{font-size:13px;margin:18px 0 8px;color:var(--mut);font-weight:700;letter-spacing:.04em}
.sub{color:var(--mut);font-size:13px;margin:0 0 2px}
.snap{margin:14px 0 0;padding:9px 12px;border-radius:8px;background:var(--card);
 border:1px solid var(--line);font-size:13px;color:var(--mut)}
.snap b{color:var(--fg)}
.nav{display:flex;gap:8px;margin:12px 0 0;flex-wrap:wrap}
.nav a{font-size:13px;padding:4px 11px;border-radius:99px;text-decoration:none;
 background:var(--card);border:1px solid var(--line);color:var(--mut)}
.nav a.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
.nav a.go{margin-left:auto;font-weight:700;color:var(--fg)}
.c .v small{font-size:12px;font-weight:600;color:var(--mut);margin-left:1px}
.cards{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(152px,1fr));
 margin-top:14px}
.c{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 12px}
.c .k{font-size:12px;color:var(--mut);line-height:1.35;min-height:2.7em}
.c .v{font-size:25px;font-weight:700;letter-spacing:-.02em;margin:3px 0 2px}
.c .d{font-size:12px;font-weight:600}
.c .d.up{color:var(--good)}.c .d.down{color:var(--bad)}
.c .d.flat,.c .d.neutral{color:var(--mut)}
.c .b{font-size:11px;color:var(--mut)}
.fin{display:grid;gap:9px}
.f{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--mut);
 border-radius:8px;padding:10px 13px}
.f.good{border-left-color:var(--good)}.f.bad{border-left-color:var(--bad)}
.f.warn{border-left-color:var(--warn)}.f.info{border-left-color:var(--info)}
.f .t{font-weight:700;font-size:14px;margin-bottom:2px}
.f .t i{font-style:normal;font-size:11px;font-weight:700;padding:1px 6px;border-radius:99px;
 margin-right:7px;vertical-align:1px;color:#fff;background:var(--mut)}
.f.good .t i{background:var(--good)}.f.bad .t i{background:var(--bad)}
.f.warn .t i{background:var(--warn)}.f.info .t i{background:var(--info)}
.f .x{font-size:13.5px;color:var(--fg)}
.chwrap{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:12px 10px 8px;overflow-x:auto}
svg.ch{display:block;width:100%;min-width:320px;height:auto;overflow:visible}
.gl{stroke:var(--line);stroke-width:1}
text.ax{font-size:10px;fill:var(--mut)}
text.ax2{font-size:9px;fill:var(--mut);opacity:.75}
text.vl{font-size:10.5px;font-weight:700;fill:var(--fg)}
.pl{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
.legend{display:flex;flex-wrap:wrap;gap:12px;padding:8px 4px 2px;font-size:12px;
 color:var(--mut)}
.lg i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px}
.bars{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 12px}
.bars .row{display:grid;grid-template-columns:7.6em 1fr 3.4em;align-items:center;
 gap:9px;padding:7px 0;border-bottom:1px solid var(--line)}
.bars .row:last-child{border-bottom:0}
.lab{font-size:13px}
.track{height:9px;background:var(--line);border-radius:99px;overflow:hidden}
.fill{height:100%;background:var(--accent);border-radius:99px}
.fill.zero{background:repeating-linear-gradient(45deg,var(--mut),var(--mut) 2px,
 transparent 2px,transparent 4px);min-width:26px}
.val{font-size:13px;font-weight:700;text-align:right}
.sub{grid-column:2/4;font-size:11.5px;color:var(--mut);margin-top:-4px}
table{width:100%;border-collapse:collapse;font-size:13px;background:var(--card);
 border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{padding:6px 9px;border-bottom:1px solid var(--line);text-align:right}
th:first-child,td:first-child{text-align:left}
th{font-size:11.5px;color:var(--mut);font-weight:700;white-space:nowrap}
tr:last-child td{border-bottom:0}
td.z{color:var(--mut)}
.note{font-size:12px;color:var(--mut);margin:7px 2px 0}
.gl2{display:grid;gap:7px;margin-top:4px}
.gi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 11px;
 font-size:13px}
.gi b{font-weight:700}
.gi code{font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--accent);
 background:rgba(128,128,128,.12);padding:1px 5px;border-radius:4px}
.gi span{color:var(--mut);display:block;font-size:12.5px;margin-top:2px}
.two{display:grid;gap:14px;grid-template-columns:1fr 1fr}
@media (max-width:620px){.two{grid-template-columns:1fr}
 .bars .row{grid-template-columns:6.4em 1fr 3.2em}}
footer{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);
 font-size:12px;color:var(--mut)}
footer li{margin:4px 0}
`;

const LV = { good: "好", bad: "坏", warn: "注意", info: "留意" };

// 把指标函数箭头右边那一截直接印出来——公式不另抄一份，省得写的和算的不一样
function formula(fn) {
  const s = String(fn);
  const i = s.indexOf("=>");
  return i < 0 ? "" : s.slice(i + 2).trim().replace(/\s+/g, " ");
}

function cards(ctx) {
  const out = ['<div class="cards">'];
  const nb = ctx.base_days.length;
  for (const m of METRICS) {
    const f = m.fn(ctx.today);
    const t = ctx.head_val(m.key);
    const b = ctx.base_val(m.key);
    const d = t === null || b === null ? null : t - b;
    const bf = m.fn(ctx.base);
    let cls = "flat";
    let lab = bf && bf.frac && bf.b > 0 && bf.b < m.min_b ? "基线样本不够" : "没有基线可比";
    if (d !== null) {
      // 先按要显示的位数四舍五入再判断，不然 -0.5 会印成「-0」
      const shown = +d.toFixed(m.dec);
      if (shown === 0) {
        lab = "和基线一样";
      } else {
        cls = m.good === "neutral" ? "neutral"
          : (shown > 0) === (m.good === "up") ? "up" : "down";
        lab = sgn(shown, m.dec) + (m.unit === "%" ? "pp" : m.unit);
      }
    }
    const bits = [fracTxt(f), "基线 " + fmt(b, m) + (m.per_day ? "/天" : "")].filter(Boolean);
    const vtxt = fmt(t, m)
      + (m.per_day && t !== null && ctx.span > 1 ? "<small>/天</small>" : "");
    out.push('<div class="c" title="'
      + esc(m.note + "（基线 = 前 " + nb + " 天的同档口）") + '"><div class="k">'
      + esc(m.name) + '</div><div class="v">' + vtxt + '</div><div class="d ' + cls
      + '">' + esc(lab) + '</div><div class="b">' + esc(bits.join(" · ")) + "</div></div>");
  }
  out.push("</div>");
  return out.join("");
}

function findings(ctx) {
  const order = { bad: 0, warn: 1, good: 2, info: 3 };
  const got = [];
  for (const r of RULES) {
    let f;
    try {
      f = r(ctx);
    } catch (e) {                                  // 一条结论挂了不该拖垮整页
      f = Fin("warn", "结论 " + r.name + " 算挂了", String((e && e.message) || e));
    }
    if (f) got.push(f);
  }
  got.sort((a, b) => (order[a.lv] == null ? 9 : order[a.lv])
                   - (order[b.lv] == null ? 9 : order[b.lv]));
  return '<div class="fin">' + got.map((f) => '<div class="f ' + f.lv + '"><div class="t"><i>'
    + (LV[f.lv] || "?") + "</i>" + esc(f.title) + '</div><div class="x">' + esc(f.text)
    + "</div></div>").join("") + "</div>";
}

function table(head, rows, zeroCols = []) {
  const out = ["<table><tr>"];
  for (const h of head) out.push("<th>" + esc(h) + "</th>");
  out.push("</tr>");
  for (const r of rows) {
    out.push("<tr>");
    r.forEach((cell, i) => {
      const z = zeroCols.includes(i) && (cell === 0 || cell === "0" || cell === "—")
        ? " class='z'" : "";
      out.push("<td" + z + ">" + esc(cell) + "</td>");
    });
    out.push("</tr>");
  }
  out.push("</table>");
  return out.join("");
}

// o = { days 窗口天数, token 口令（只用来拼换窗口的链接） }
export function render(ctx, o = {}) {
  const days = ctx.daylist;
  const dayb = days.map((d) => ctx.day[d]);
  const sv = (s) => days.map((d) => ctx.svcSes(d, s));
  const gen = new Date(Date.now() + TZ * 1000).toISOString().slice(5, 16).replace("T", " ");
  const svcs = ctx.svcs.join("/");
  const partial = ctx.half_today ? "最后一天还没过完。" : "";
  const a = ctx.all, t = ctx.today, bs = ctx.base;

  const h = ['<!doctype html><html lang="zh"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width,initial-scale=1">'
    + '<meta name="color-scheme" content="light dark">'
    + "<title>Sibisi 菜单数据 · " + esc(ctx.today_day) + "</title><style>" + CSS
    + "</style></head><body><div class='wrap'>"];
  h.push("<h1>Sibisi 菜单数据</h1>");
  h.push('<p class="sub">' + esc(days[0]) + " – " + esc(days[days.length - 1]) + "（"
    + days.length + " 天有数据，共 " + a.ses + " 个会话 / " + a.ev + " 条事件）</p>");
  if (o.token) {
    const k = encodeURIComponent(o.token);
    const pill = (r, lab) => '<a class="' + (r === ctx.range ? "on" : "") + '" href="?k='
      + k + "&r=" + r + '">' + lab + "</a>";
    // 刷新链接带个时间戳：和当前地址不一样，点了一定是一次新请求
    h.push('<div class="nav">' + pill(1, "今天") + pill(3, "最近 3 天") + pill(7, "最近 7 天")
      + pill(30, "最近 30 天")
      + '<a class="go" href="?k=' + k + "&r=" + ctx.range + "&t=" + Date.now()
      + '">↻ 刷新</a></div>');
  }
  const headTxt = ctx.range > 1 && ctx.head_days.length
    ? ctx.label + "（" + short(ctx.head_days[0]) + " – "
      + short(ctx.head_days[ctx.head_days.length - 1]) + "，" + ctx.span + " 个营业日）"
    : ctx.label;
  const baseTxt = !ctx.base_days.length ? "再往前没有可比的日子了"
    : ctx.range > 1
      ? "「基线」是再往前的 " + ctx.base_days.length + " 个营业日，整天对整天"
      : "「基线」是前 " + ctx.base_days.length + " 天的同一档口（" + svcs
        + "），所以半天不会拿去跟整天比";
  h.push('<div class="snap">这一页是<b>打开的时候现算的</b>，算于 <b>' + esc(gen)
    + "</b>——这里没有缓存，<b>刷新页面（或者点上面那个 ↻）就是最新的数字</b>。"
    + "<br>卡片上的大数字是 <b>" + esc(headTxt) + "</b>，" + esc(baseTxt) + "。"
    + (ctx.range > 1 ? "只数正常营业的日子：周四休息、和还没开门的半天都不算一天。" : "")
    + "</div>");

  h.push("<h2>" + esc(ctx.range > 1 ? ctx.label : "今天") + "</h2>");
  h.push(cards(ctx));
  h.push("<h2>自动结论</h2>");
  h.push('<p class="note">每条结论是 collector/dash.js 里一个 rule() 函数，阈值提前写死在'
    + "函数里。数字满足条件它才出现，不满足就不出现。</p>");
  h.push(findings(ctx));

  h.push("<h2>每天多少人扫码</h2>");
  h.push(svgStack(days, [["午市", C_LUNCH, sv("午市")], ["晚市", C_DINNER, sv("晚市")]],
    "按业务日分（早上 5 点切），" + partial + "周四休息。"));

  h.push("<h2>关键比率的走势</h2>");
  h.push(svgLines(days, [
    ["建了清单", C_LINE[0], dayb.map((b) => ctx.val("add_rate", b))],
    ["菜单正文转化", C_LINE[1], dayb.map((b) => ctx.val("menu_conv", b))],
    ["节气推荐转化", C_LINE[2], dayb.map((b) => ctx.val("luck_conv", b))],
  ], "线断开 = 那天这个指标没有分母，不是 0。" + partial));

  h.push("<h2>" + esc(ctx.word) + "的漏斗</h2>");
  const frows = [];
  for (const [lab, key] of [["打开菜单", null], ["看到菜", "imp"], ["点开详情", "det"],
                            ["建了清单", "add"], ["给服务员看", "staff"]]) {
    const n = key === null ? t.ses : t.sv(key);
    const bn = key === null ? bs.ses : bs.sv(key);
    const v = pc(n, t.ses), bv = pc(bn, bs.ses);
    // 「给服务员看」那一格的分母其实是上一格：按钮在「清单」卡里，没建清单看不到
    const extra = key === "staff" && t.sv("add")
      ? "，占建了清单的 " + fx(pc(n, t.sv("add")), 0) + "%" : "";
    frows.push([lab, v, n + " 个会话" + extra
      + (bv === null ? "" : " · 基线 " + fx(bv, 0) + "%")]);
  }
  h.push(hbars(frows, "%", (v) => (v || 0) / 100));

  h.push("<h2>哪个区域在卖货</h2>");
  const CONV = { menu: "menu_conv", luck: "luck_conv", first: "first_conv" };
  h.push(hbars(WITH_IMP.map((s) => [sname(s), ctx.val(CONV[s], a),
    a.seen(s) + " 看到 → " + gv(a.srcs, K(s, "det")) + " 点开 → " + a.added(s)
    + " 加入（" + a.adds(s) + " 次）"]), "%", (v) => (v || 0) / 100, 1));
  h.push('<p class="note">只有这三处会记「看到」，所以只有它们有分母。'
    + "斜纹条 = 真的是 0，不是没数据。全期合计，不只今天。</p>");
  const click = [...new Set(keys(a.srcs).map((k) => k.split("\u0001")[0]))]
    .filter((s) => !WITH_IMP.includes(s)).sort()
    .map((s) => [sname(s), a.added(s), a.adds(s), a.drinks(s)])
    .filter((r) => r[1] || r[3])
    .sort((x, y) => y[2] - x[2]);
  if (click.length) {
    h.push("<h3>点出来的区域（没有曝光，所以没有转化率）</h3>");
    h.push(table(["区域", "加入的会话", "加入次数", "饮料次数"], click, [1, 2, 3]));
  }

  h.push("<h2>语言</h2>");
  const langs = ["es", "en", "zh", "?"].filter((l) => gv(a.lang, l));
  h.push(svgStack(days, langs.map((l) => [l, C_LANG[l] || "#999",
    days.map((d) => gv(ctx.day[d].lang, l))]),
    "按会话打开菜单时的语言分。这项决定要不要加第四种语言。"));
  h.push(table(["语言", "会话", "给服务员看", "占该语言"],
    langs.map((l) => [l, a.lang[l], gv(a.lang_staff, l),
      fx(pc(gv(a.lang_staff, l), a.lang[l]) || 0, 0) + "%"]), [2]));

  h.push("<h2>菜</h2>");
  const tadd = t.byDish("add");
  h.push("<h3>" + esc(ctx.word) + "加进清单最多的</h3>");
  if (keys(tadd).length) {
    h.push(hbars(top(tadd, 8).map(([c, n]) => [c + " " + dname(c), n,
      "看到 " + t.dsv(c, "imp") + " 会话 · 点开 " + t.dsv(c, "det")]), "次"));
  } else {
    h.push('<p class="note">' + esc(ctx.word) + "还没有人把菜加进清单。</p>");
  }
  h.push("<h3>全期漏斗（按会话算，前 15）</h3>");
  const codes = [...new Set(keys(a.dishs).map((k) => k.split("\u0001")[0]))]
    .sort((x, y) => a.dsv(y, "add") - a.dsv(x, "add") || a.dsv(y, "imp") - a.dsv(x, "imp")
      || (x < y ? -1 : 1)).slice(0, 15);
  h.push(table(["菜", "看到", "点开", "加入", "看到→加入", "加入次数"],
    codes.map((c) => [c + " " + dname(c), a.dsv(c, "imp"), a.dsv(c, "det"), a.dsv(c, "add"),
      a.dsv(c, "imp") ? fx(pc(a.dsv(c, "add"), a.dsv(c, "imp")), 0) + "%" : "—",
      a.dnv(c, "add")]), [1, 2, 3, 5]));

  h.push("<h2>饮料</h2>");
  if (keys(a.drink).length) {
    h.push(hbars(top(a.drink, 10).map(([k, n]) => [dname(k) || k, n,
      PRICE[k] == null ? "" : fx(PRICE[k], 2) + " €"]), "次"));
    h.push('<p class="note">全期合计。推荐搭配默认选中的是 ' + esc(DEFAULT_DRINK[1]) + "。</p>");
  } else {
    h.push('<p class="note">还没有人点过饮料。</p>');
  }

  h.push("<h2>设备和地区</h2>");
  h.push('<div class="two">');
  h.push(table(["国家", "会话"], top(a.country, 8)));
  // 宽度是数字，并列时按宽度从大到小——按字符串排会把 "720" 排到 "1260" 后面
  const widths = keys(a.width).map((w) => [+w, a.width[w]])
    .sort((x, y) => y[1] - x[1] || y[0] - x[0]).slice(0, 8);
  h.push(table(["屏幕宽度", "会话"],
    widths.map(([w, n]) => [w + "px" + (w >= DESK_W ? "（桌面）" : ""), n])));
  h.push("</div>");

  h.push("<h2>这些数是怎么算的</h2>");
  h.push('<div class="gl2">');
  for (const m of METRICS) {
    h.push('<div class="gi"><b>' + esc(m.name) + "</b> <code>" + esc(formula(m.fn))
      + "</code><span>" + esc(m.note) + "</span></div>");
  }
  h.push("</div>");
  h.push('<p class="note">b 是一堆会话的计数：b.ses 会话数、b.sv(事件) 出现过该事件的'
    + "会话数、b.nv(事件) 次数、b.seen(区域) / b.added(区域) 该区域的曝光和加入会话数。"
    + "想加指标就在 collector/dash.js 的公式层加一个 metric()，卡片和走势图自动跟着出来。</p>");

  h.push("<footer><b>口径，别绕过去：</b><ul>"
    + "<li><b>ts 是上报时间，不是发生时间。</b>事件攒到 40 条或页面关掉才发一次，"
    + "所以这里只用它分业务日和午市/晚市，不画「几点人最多」。</li>"
    + "<li><b>「看到」卡得很严：</b>卡片露出一半并停留 1 秒才算，划过去不算；"
    + "一道菜一个会话只记一次，同一个人反复点不会把分子撑大。</li>"
    + "<li><b>「加入」不等于成单。</b>它只是进了清单。真实销量在店里那套 POS 里。</li>"
    + "<li><b>只看得见扫码的人。</b>没扫码、直接问服务员的客人完全不在数据里，"
    + "而扫码的人本身偏年轻、偏外国人。</li>"
    + "<li><b>一天几十桌。</b>单项指标一天可能只有十几个数据点，别过度解读。</li>"
    + "</ul></footer></div></body></html>");
  return h.join("");
}

// 原始数据 → 整页 HTML。Worker 和本地核对脚本都走这一个入口
export function dashboard(data, o = {}) {
  const sessions = load(data);
  if (!sessions.length) {
    return "<!doctype html><meta charset='utf-8'><p style='font:16px/1.6 sans-serif;"
      + "padding:24px'>这段时间一条数据都没有。</p>";
  }
  return render(new Ctx(data, sessions, o.range || 1), o);
}
