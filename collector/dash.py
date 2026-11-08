#!/usr/bin/env python3
"""从 /r 的原始计数生成一个自带数据的 dashboard HTML。

    ./dash.sh                                   # 平时就跑这个
    curl '.../r?k=…&d=14' | python3 dash.py > out/dashboard.html

分三层，改东西只动对应那一层：

  1. 聚合层  `Bucket` / `rollup()`
     把会话按「业务日 × 午市/晚市」归堆。只做计数，不下任何结论。
  2. 公式层  `@metric` 注册的函数
     一个指标一个函数：输入一个 Bucket，输出一个数。加指标只需在这一层加个函数，
     卡片、走势图、和基线的对比全都自动跟着出来。
  3. 结论层  `@rule` 注册的函数
     一条结论一个函数：输入整段数据，输出一句话或者 None。阈值写在函数里，
     所以「多少算异常」是提前定好的，不是每次看图现编一个说法。

图表只画公式层算出来的数，自己不算数。

两个口径上的硬约束，别绕过去：
  * `ts` 是上报时间不是发生时间（见 README「已知的坑」），所以这里只用它分
    业务日和午市/晚市，不画任何「几点人最多」。
  * 所有比率的分子分母都按**会话**算，不按次数。同一个人反复点同一道菜
    不会把分子撑大。
"""
import html
import json
import math
import os
import re
import sys
import time
from collections import Counter, namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _names import DEFAULT_DRINK, PRICE, WITH_IMP, dname, sname   # noqa: E402

TZ = 3600          # Valencia 冬令时 UTC+1。三月底换夏令时要改成 7200
CUT_H = 5          # 业务日从早上 5 点切：23:00 打烊，事件缓冲最晚 01:00 才落库
DINNER_H = 18      # 这个点之后开的会话算晚市（营业 12:30–16:30 / 20:00–23:00）
DESK_W = 1000      # 屏幕宽到这个数就不太可能是店里桌上的手机
BASE_DAYS = 7      # 基线取前 7 天
DISH = re.compile(r"^\d+-\d+$")

div = lambda a, b: None if not b else a / float(b)
pc = lambda a, b: None if not b else 100.0 * a / b
esc = html.escape

WEEK = "一二三四五六日"
bizday = lambda ms: time.strftime("%Y-%m-%d", time.gmtime(ms / 1000.0 + TZ - CUT_H * 3600))
cet_h = lambda ms: time.gmtime(ms / 1000.0 + TZ).tm_hour
svc_of = lambda ms: "晚市" if cet_h(ms) >= DINNER_H else "午市"
wday = lambda d: "周" + WEEK[time.strptime(d, "%Y-%m-%d").tm_wday]
short = lambda d: d[5:]


# ────────────────────────────── 1. 聚合层 ──────────────────────────────

class Ses:
    """一个会话。/r 给的是「会话 × 事件名 × 值 × 来源」的计数行，这里拼回会话。"""

    def __init__(self, sid):
        self.sid = sid
        self.t0 = self.t1 = None
        self.w = self.country = self.lang = None
        self.nev = 0
        self.ev = Counter()        # 事件名 -> 次数
        self.src = Counter()       # (来源, 事件名) -> 次数
        self.dish = Counter()      # (菜号, 事件名) -> 次数
        self.drink = Counter()     # 饮料 id -> 次数
        self.pack = Counter()      # 套餐 id -> 次数
        self.sw = 0                # 切语言次数

    def feed(self, name, v, src, n, t0, t1, w, c):
        self.t0 = t0 if self.t0 is None else min(self.t0, t0)
        self.t1 = t1 if self.t1 is None else max(self.t1, t1)
        if w:
            self.w = max(self.w or 0, w)
        if c and not self.country:
            self.country = c
        self.nev += n
        self.ev[name] += n
        if name == "open" and v and not self.lang:
            self.lang = v
        if name == "lang":
            self.sw += n
        if name in ("imp", "det", "add", "drink"):
            self.src[(src or "(旧)", name)] += n
        if name in ("imp", "det", "add", "pair") and v and DISH.match(v):
            self.dish[(v, name)] += n
        if name == "drink" and v:
            self.drink[v] += n
        if name == "combo" and v:
            self.pack[v] += n

    day = property(lambda s: bizday(s.t0))
    svc = property(lambda s: svc_of(s.t0))
    # 整个会话的事件带着同一个毫秒落库 = 缓冲一次性清空。这个会话的时刻完全不可用
    flat = property(lambda s: s.t1 == s.t0)
    desktop = property(lambda s: (s.w or 0) >= DESK_W)


class Bucket:
    """一堆会话的计数。`_CTRS` / `_INTS` 列全，`absorb` 才能把两堆并起来不漏字段。"""

    _CTRS = ("n", "s", "srcn", "srcs", "dishn", "dishs", "drink", "pack",
             "lang", "lang_staff", "country", "width")
    _INTS = ("ses", "ev", "sw_ses", "desk", "flat", "cart_dishes", "cart_ses")

    def __init__(self, label=""):
        self.label = label
        self.days = set()
        for k in self._CTRS:
            setattr(self, k, Counter())
        for k in self._INTS:
            setattr(self, k, 0)

    def take(self, x):
        self.ses += 1
        self.ev += x.nev
        self.days.add(x.day)
        self.sw_ses += 1 if x.sw else 0
        self.desk += 1 if x.desktop else 0
        self.flat += 1 if x.flat else 0
        # 「清单里几道菜」按**不同的菜**算，不按加入次数：有人会把同一道菜连点二十下，
        # 按次数算那一个会话就能把全店的平均值翻倍
        inc = {k[0] for k, v in x.dish.items() if k[1] == "add" and v}
        self.cart_dishes += len(inc)
        self.cart_ses += 1 if inc else 0
        for k, v in x.ev.items():
            self.n[k] += v
            self.s[k] += 1                       # 「出现过这个事件的会话数」
        for k, v in x.src.items():
            self.srcn[k] += v
            self.srcs[k] += 1
        for k, v in x.dish.items():
            self.dishn[k] += v
            self.dishs[k] += 1
        for k, v in x.drink.items():
            self.drink[k] += v
        for k, v in x.pack.items():
            self.pack[k] += v
        lg = x.lang or "?"
        self.lang[lg] += 1
        if x.ev.get("staff"):
            self.lang_staff[lg] += 1
        self.country[x.country or "??"] += 1
        self.width[x.w or 0] += 1

    def absorb(self, b):
        self.days |= b.days
        for k in self._CTRS:
            getattr(self, k).update(getattr(b, k))
        for k in self._INTS:
            setattr(self, k, getattr(self, k) + getattr(b, k))
        return self

    # 给公式层用的小口子
    seen = lambda s, src: s.srcs[(src, "imp")]
    added = lambda s, src: s.srcs[(src, "add")]
    adds = lambda s, src: s.srcn[(src, "add")]
    drinks = lambda s, src: s.srcn[(src, "drink")]


def load(fp):
    d = json.load(fp)
    if "error" in d:
        sys.exit("读取失败：口令不对，或者 Worker 上还没设 TOKEN")
    ci = {c: i for i, c in enumerate(d["cols"])}
    ses = {}
    for r in d["rows"]:
        sid = r[ci["sid"]]
        s = ses.get(sid)
        if s is None:
            s = ses[sid] = Ses(sid)
        s.feed(r[ci["name"]], r[ci["v"]], r[ci["src"]], r[ci["n"]],
               r[ci["t0"]], r[ci["t1"]], r[ci["w"]], r[ci["c"]])
    return d, sorted(ses.values(), key=lambda s: s.t0)


class Ctx:
    """聚合结果 + 取数的口子。公式层和结论层都只跟它打交道。"""

    def __init__(self, meta, sessions):
        self.meta = meta
        self.sessions = sessions
        self.svcb = {}
        for x in sessions:
            k = (x.day, x.svc)
            self.svcb.setdefault(k, Bucket("%s %s" % k)).take(x)
        self.daylist = sorted({d for d, _ in self.svcb})
        self.day = {d: self.pick([d], ("午市", "晚市")) for d in self.daylist}
        self.all = self.pick(self.daylist, ("午市", "晚市"))
        # 会话个数少于这个数的日子不是正常营业（周四休息、或者只有我自己在测），
        # 算基线时要排掉，不然一个空日子能把基线拉低一半
        self.live_days = [d for d in self.daylist if self.day[d].ses >= 5]

        # 今天只开了午市的话，拿昨天**整天**比就是拿半天比一天。
        # 基线按今天实际有的档口取，才是同口径
        self.today_day = self.daylist[-1] if self.daylist else None
        self.svcs = tuple(s for d, s in self.svcb if d == self.today_day) or ("午市",)
        self.svcs = tuple(s for s in ("午市", "晚市") if s in self.svcs)
        prev = [d for d in self.daylist if d != self.today_day]
        self.prev_day = prev[-1] if prev else None
        self.today = self.pick([self.today_day], self.svcs)
        self.prev = self.pick([self.prev_day], self.svcs) if self.prev_day else Bucket()
        self.base_days = [d for d in prev if d in self.live_days][-BASE_DAYS:]
        self.base = self.pick(self.base_days, self.svcs)
        self.partial = len(self.svcs) < 2 and wday(self.today_day) in ("周五", "周六", "周日")

    def pick(self, days, svcs):
        b = Bucket()
        for d in days:
            for s in svcs:
                x = self.svcb.get((d, s))
                if x:
                    b.absorb(x)
        return b

    def raw(self, key, b):
        return MBY[key].fn(b)

    def val(self, key, b):
        m = MBY[key]
        return value(m, m.fn(b))

    def base_val(self, key):
        """基线值。计数型指标要除以天数，不然等于拿一天去比一整周。"""
        m = MBY[key]
        v = value(m, m.fn(self.base))
        if v is not None and m.per_day and self.base_days:
            v /= len(self.base_days)
        return v


# ────────────────────────────── 2. 公式层 ──────────────────────────────
# 一个指标一个函数。比率一律返回 Frac(分子, 分母)，不直接返回百分数——
# 分母带着走，引擎才能在分母太小的时候直接不出数（而不是给出 1/1 = 100% 这种假结论）。

Frac = namedtuple("Frac", "a b")
Metric = namedtuple("Metric", "key name unit dec good note fn min_b per_day")
METRICS, MBY = [], {}


def metric(key, name, unit="", dec=0, good="up", note="", min_b=10, per_day=False):
    """注册一个指标。

    unit   "%" 的话 Frac 按百分数算，空的话按比值算
    good   变大是好事还是坏事，只影响涨跌的颜色；"neutral" 就一直是灰的
    min_b  分母至少要有这么多，不够就不出数。1/1 = 100% 这种是噪声不是信号
    per_day 计数型指标（会话数这种）：当基线用的时候要除以天数，否则等于拿一天比一周
    """
    def deco(fn):
        m = Metric(key, name, unit, dec, good, note, fn, min_b, per_day)
        METRICS.append(m)
        MBY[key] = m
        return fn
    return deco


def value(m, f):
    """Frac → 数。分母不够就返回 None，页面上显示「—」。"""
    if f is None:
        return None
    if not isinstance(f, Frac):
        return float(f)
    if not f.b or f.b < m.min_b:
        return None
    return 100.0 * f.a / f.b if m.unit == "%" else f.a / float(f.b)


def fmt(v, m):
    return "—" if v is None else ("%.*f%s" % (m.dec, v, m.unit))


def frac_txt(f):
    return "" if not isinstance(f, Frac) else "%d / %d" % (f.a, f.b)


@metric("ses", "扫码会话", per_day=True,
        note="有多少台手机打开过菜单。它是下面几乎所有比率的分母")
def _m_ses(b):
    return b.ses


@metric("add_rate", "建了清单", "%", good="up",
        note="最接近点单意图的信号。不等于成单——真实销量在店里那套 POS 里")
def _m_add(b):
    return Frac(b.s["add"], b.ses)


@metric("det_rate", "点开过详情", "%", good="up", note="看了照片和介绍，说明在认真挑")
def _m_det(b):
    return Frac(b.s["det"], b.ses)


@metric("cart", "清单里几道不同的菜", "道", 1, good="up", min_b=5,
        note="不同的菜数 ÷ 建了清单的会话。按不同的菜算，不按加入次数——"
             "同一道菜连点二十下只算一道")
def _m_cart(b):
    return Frac(b.cart_dishes, b.cart_ses)


@metric("menu_conv", "菜单正文 看到→加入", "%", good="up",
        note="唯一有分母、又真的在卖货的区域")
def _m_menu(b):
    return Frac(b.added("menu"), b.seen("menu"))


@metric("luck_conv", "节气推荐 看到→加入", "%", good="up",
        note="2026-11-07 16:33 起改成进页面直接显示；在那之前要先点一下才翻开，"
             "51 个会话里 0 个点过，等于没有分母")
def _m_luck(b):
    return Frac(b.added("luck"), b.seen("luck"))


@metric("first_conv", "顶层推荐 看到→加入", "%", good="up", note="「第一次来点什么」那块")
def _m_first(b):
    return Frac(b.added("first"), b.seen("first"))


@metric("staff_rate", "给服务员看", "%", good="up", note="目前最接近「成单」的信号")
def _m_staff(b):
    return Frac(b.s["staff"], b.ses)


@metric("drink_rate", "点了饮料", "%", good="up", note="饮料是毛利最高的一档")
def _m_drink(b):
    return Frac(b.s["drink"], b.ses)


@metric("drink_list", "饮料里来自酒水单", "%", good="neutral", min_b=8,
        note="剩下的来自推荐搭配、套餐、结算前加点。这项越高，说明推荐越带不动饮料")
def _m_drink_list(b):
    return Frac(b.drinks("drinks"), b.n["drink"])


@metric("switch", "中途切语言", "%", good="down",
        note="高了说明按浏览器语言自动判断不准，客人得自己动手")
def _m_switch(b):
    return Frac(b.sw_ses, b.ses)


@metric("non_es", "非西语会话", "%", good="neutral", note="这项决定要不要加第四种语言")
def _m_nonwes(b):
    return Frac(b.ses - b.lang.get("es", 0), b.ses)


@metric("depth", "每会话翻了多少下", "", 1, good="up",
        note="事件数 ÷ 会话数。10 以下基本是打开就走")
def _m_depth(b):
    return Frac(b.ev, b.ses)


@metric("desk", "桌面宽度会话", "", good="down", per_day=True,
        note="屏幕 ≥%dpx，大概不是店里桌上的手机；小样本下足够把某个区域的转化率"
             "从 0 抬到「有」" % DESK_W)
def _m_desk(b):
    return b.desk


# ────────────────────────────── 3. 结论层 ──────────────────────────────
# 一条结论一个函数：输入整段数据，输出一句话或者 None。
# 阈值提前写死在函数里，所以「多少算异常」是定好的，不是每次看图现编一个说法。

Fin = namedtuple("Fin", "lv title text")
RULES = []
rule = lambda fn: (RULES.append(fn), fn)[1]


@rule
def _r_partial(c):
    if not c.partial:
        return None
    return Fin("info", "今天还没过完",
               "今天是%s，晚市 20:00 才开。下面的数字只含午市，所以基线也只拿前几天的"
               "午市来比——拿半天跟整天比会凭空少一半。" % wday(c.today_day))


@rule
def _r_sample(c):
    if c.today.ses >= 25:
        return None
    return Fin("warn", "今天样本小",
               "只有 %d 个会话。这个量级下单项指标的涨跌基本是噪声，"
               "看「哪个区域在卖货」那段的全期合计更稳。" % c.today.ses)


def _reco(c, src, key, label):
    """推荐区的判定。有曝光才有分母；0 加入时用 3/n 估个上限，而不是说「0%」。"""
    b = c.all
    seen, add = b.seen(src), b.added(src)
    menu = c.val("menu_conv", b)
    mtxt = fmt(menu, MBY["menu_conv"])
    if seen < 30:
        return Fin("info", "%s还看不出来" % label,
                   "累计 %d 个会话看到、%d 个加入。曝光不到 30 个会话，先不下结论。"
                   % (seen, add))
    if add == 0:
        cap = 3.0 / seen * 100                      # 0/n 的 95% 上限 ≈ 3/n
        return Fin("bad", "%s零转化" % label,
                   "累计 %d 个会话看到、0 个加入。按 3/n 估，真实转化率上限约 %.1f%%，"
                   "而菜单正文是 %s。它占掉正文之前的一屏多，该考虑的是"
                   "合并 / 挪到正文之后 / 去掉，不是继续调推荐算法。" % (seen, cap, mtxt))
    conv = 100.0 * add / seen
    if menu and conv * 2 < menu:
        return Fin("warn", "%s还是比正文差一截" % label,
                   "%d 看到 → %d 加入（%.1f%%），菜单正文 %s，差 %.1f 倍。"
                   "有转化了，但还撑不住它占的那块位置。"
                   % (seen, add, conv, mtxt, menu / conv))
    return Fin("good", "%s开始有效了" % label,
               "%d 看到 → %d 加入（%.1f%%），和菜单正文的 %s 在一个量级。"
               % (seen, add, conv, mtxt))


@rule
def _r_luck(c):
    return _reco(c, "luck", "luck_conv", "节气推荐")


@rule
def _r_first(c):
    return _reco(c, "first", "first_conv", "顶层推荐")


@rule
def _r_menu_move(c):
    t, b = c.val("menu_conv", c.today), c.base_val("menu_conv")
    if t is None or b is None or c.today.ses < 25:
        return None
    d = t - b
    if abs(d) < 8:
        return None
    return Fin("good" if d > 0 else "warn", "菜单正文转化%s了" % ("变好" if d > 0 else "变差"),
               "今天 %.0f%%，前 %d 天同档口（%s）的基线 %.0f%%，差 %+.0f 个百分点。"
               % (t, len(c.base_days), "/".join(c.svcs), b, d))


@rule
def _r_service_gap(c):
    """午市和晚市是两种客群：赶时间的，和坐下来吃的。混成「今天」会把两边都看糊。"""
    lun, din = c.pick(c.live_days, ("午市",)), c.pick(c.live_days, ("晚市",))
    a, b = c.val("add_rate", lun), c.val("add_rate", din)
    if a is None or b is None or min(lun.ses, din.ses) < 20 or abs(a - b) < 8:
        return None
    hi = "晚市" if b > a else "午市"
    return Fin("info", "%s的人更愿意建清单" % hi,
               "全期午市 %.0f%%（%d 会话）、晚市 %.0f%%（%d 会话），差 %.0f 个百分点。"
               "同一份代码、同一批菜，所以这两场值得分开看。"
               % (a, lun.ses, b, din.ses, abs(a - b)))


@rule
def _r_order(c):
    """UPSELL 那几道是出餐快、毛利高的小菜，位置在清单结算前。"""
    b = c.all
    if b.added("order") + b.srcs[("order", "drink")]:
        return None
    return Fin("warn", "结算前加点没人用",
               "累计 %d 个会话建过清单，结算前那块加点一次都没被点过。那几道是出餐快、"
               "毛利高的小菜——要么没人滑到那儿，要么它不像个能点的东西。" % b.s["add"])


@rule
def _r_drink_src(c):
    b = c.all
    tot = b.n["drink"]
    if tot < 8:
        return None
    lst = b.drinks("drinks")
    box = b.drinks("pairbox") + b.drinks("det")
    return Fin("info", "饮料是客人自己翻出来的",
               "%d 次点饮料里 %d 次来自酒水单，推荐搭配只带出 %d 次。"
               "酒水单在干活，推荐位没在干活。" % (tot, lst, box))


@rule
def _r_drink_margin(c):
    """客人自己挑的和推荐默认选中的不是同一款时，值得核一下这两款的进价。"""
    b = c.all
    if not b.drink:
        return None
    top, n = b.drink.most_common(1)[0]
    did, dnm, dpr = DEFAULT_DRINK
    if top == did or n < 3:
        return None
    tp = PRICE.get(top)
    same = tp is not None and dpr is not None and abs(tp - dpr) < 0.01
    return Fin("info", "最常点的和推荐默认选中的不是同一款",
               "点得最多的是 %s（%d 次%s），而推荐搭配默认选中的是 %s%s。%s"
               % (dname(top) or top, n, "，%.2f €" % tp if tp is not None else "",
                  dnm, "（%.2f €）" % dpr if dpr is not None else "",
                  "两款同价，客人付一样的钱，毛利不一样，值得核一下进价。" if same
                  else "两款不同价，先看是不是价格在起作用。"))


@rule
def _r_switch(c):
    v = c.val("switch", c.all)
    if v is None or c.all.ses < 30:
        return None
    if v > 10:
        return Fin("warn", "切语言的人偏多",
                   "全期 %.0f%% 的会话中途切过语言，说明按浏览器语言自动判断不够准。" % v)
    return Fin("good", "初始语言判断是对的",
               "全期 %d 个会话里只有 %d 个中途切过语言（%.0f%%），"
               "按浏览器语言自动判断基本都判对了，这上面不用再花力气。"
               % (c.all.ses, c.all.sw_ses, v))


@rule
def _r_staff_lang(c):
    b = c.all
    rows = [(lg, b.lang[lg], b.lang_staff[lg]) for lg in ("es", "en", "zh") if b.lang[lg] >= 8]
    es = dict((lg, (n, s)) for lg, n, s in rows).get("es")
    if not es or len(rows) < 2:
        return None
    esr = pc(es[1], es[0]) or 0
    oth = [(lg, n, s) for lg, n, s in rows if lg != "es"]
    on = sum(n for _, n, _ in oth)
    os_ = sum(s for _, _, s in oth)
    othr = pc(os_, on)
    if othr is None or esr == 0 or othr < esr * 2:
        return None
    return Fin("info", "「给服务员看」是给外国人用的",
               "西语会话 %d 个里 %d 个点过（%.0f%%），非西语 %d 个里 %d 个（%.0f%%），"
               "差 %.1f 倍。西语客人会浏览，然后直接跟店员说话，不需要给手机看。"
               % (es[0], es[1], esr, on, os_, othr, othr / esr))


@rule
def _r_desktop(c):
    n = c.all.desk
    if not n:
        return None
    desk = [x for x in c.sessions if x.desktop]
    det = sum(1 for x in desk if x.ev.get("det"))
    add = sum(1 for x in desk if x.ev.get("add"))
    return Fin("warn", "有 %d 个桌面宽度的会话" % n,
               "屏幕 ≥%dpx，大概不是店里桌上的手机（我自己开页面也会算进来）。"
               "其中 %d 个点开过详情、%d 个建过清单。小样本下这几个会话足够把"
               "某个区域的转化率从 0 抬到「有」。" % (DESK_W, det, add))


@rule
def _r_spam(c):
    """有人会对着同一道菜的 + 按钮连点。按次数算的任何数字都会被这种会话撑大。"""
    bad = []
    for x in c.sessions:
        top = max([(v, k[0]) for k, v in x.dish.items() if k[1] == "add"] or [(0, "")])
        if top[0] >= 5:
            bad.append((x, top))
    if not bad:
        return None
    x, (n, code) = max(bad, key=lambda z: z[1][0])
    srcs = "、".join(sname(k[0]) for k in x.src if k[1] == "add") or "不明"
    return Fin("warn", "有 %d 个会话把同一道菜连加了 5 次以上" % len(bad),
               "最多的那个在 %s%s：%s %s 连加 %d 次，来源是%s，整个会话一共 %d 次加入。"
               "所以这个页面所有转化率都按「会话」算；只有「加入次数」那一列会被这种"
               "会话撑大，看的时候对着会话数一起看。"
               % (x.day, x.svc, code, dname(code), n, srcs, x.ev.get("add", 0)))


@rule
def _r_flush(c):
    n, tot = c.all.flat, c.all.ses
    if not n:
        return None
    return Fin("info", "时段分析做不了（口径问题，不是数据问题）",
               "%d / %d 个会话的全部事件带着同一个毫秒落库——事件先攒在队列里，攒到 40 条"
               "或者页面被关掉才发一次，所以 ts 是「上报时间」不是「发生时间」。这个页面"
               "因此只用它分业务日和午市/晚市，不画「几点人最多」。" % (n, tot))


@rule
def _r_top_dish(c):
    t = Counter({k[0]: v for k, v in c.today.dishn.items() if k[1] == "add"})
    if not t:
        return None
    prev = Counter({k[0]: v for k, v in c.base.dishn.items() if k[1] == "add"})
    old = {k for k, _ in prev.most_common(5)}
    new = [k for k, _ in t.most_common(3) if k not in old and not prev.get(k)]
    code, n = t.most_common(1)[0]
    txt = "今天加得最多的是 %s %s（%d 次）。" % (code, dname(code), n)
    if new:
        txt += "没在前几天前五里出现过的新面孔：%s。" % "、".join(
            "%s %s" % (k, dname(k)) for k in new)
    return Fin("info", "今天的菜品榜", txt)


# ────────────────────────────── 4. 画图 ──────────────────────────────
# 图表只认公式层算出来的数。这里没有任何业务判断，纯粹是把数字摆成形状。

C_LUNCH, C_DINNER = "#e0962f", "#4a6fa5"
C_LINE = ("#c0392b", "#2e7d52", "#8a63b8")
C_LANG = {"es": "#c0392b", "en": "#2e7d52", "zh": "#4a6fa5", "?": "#9a9a9a"}


def nice(v):
    """y 轴顶端取个整数，不然刻度上全是 37、74 这种数。"""
    if v <= 5:
        return 5
    e = 10 ** int(math.log10(v))
    for mul in (1, 2, 2.5, 5, 10):
        if v <= mul * e:
            return int(mul * e)
    return int(10 * e)


def svg_stack(days, series, unit="", h=190, note=""):
    """堆叠柱状图。series: [(名字, 颜色, [每天的值])]"""
    n = len(days)
    if not n:
        return ""
    pl, pb, pt = 36, 40, 16
    slot = max(46, min(104, int(820 / n)))
    bw = int(slot * 0.58)
    gap = slot - bw
    w = pl + n * slot + 12
    top = nice(max([sum(s[2][i] or 0 for s in series) for i in range(n)] + [1]))
    y = lambda v: pt + (h - pt - pb) * (1 - v / float(top))
    p = ['<svg viewBox="0 0 %d %d" class="ch" style="max-width:%dpx" '
         'preserveAspectRatio="xMinYMid meet" role="img">' % (w, h, w)]
    for g in (0, 0.5, 1):
        v = top * g
        p.append('<line class="gl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                 % (pl - 4, y(v), w - 6, y(v)))
        p.append('<text class="ax" x="%d" y="%.1f" text-anchor="end">%g</text>'
                 % (pl - 8, y(v) + 4, v))
    for i, d in enumerate(days):
        x = pl + i * (bw + gap)
        acc = 0.0
        for name, col, vals in series:
            v = vals[i] or 0
            if v:
                p.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" rx="2">'
                         '<title>%s %s %g</title></rect>'
                         % (x, y(acc + v), bw, max(1.0, y(acc) - y(acc + v)), col,
                            esc(short(d)), esc(name), v))
            acc += v
        if acc:
            p.append('<text class="vl" x="%.1f" y="%.1f" text-anchor="middle">%g</text>'
                     % (x + bw / 2.0, y(acc) - 5, acc))
        p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>'
                 % (x + bw / 2.0, h - pb + 18, esc(short(d))))
        p.append('<text class="ax2" x="%.1f" y="%d" text-anchor="middle">%s</text>'
                 % (x + bw / 2.0, h - pb + 32, esc(wday(d))))
    p.append("</svg>")
    leg = "".join('<span class="lg"><i style="background:%s"></i>%s</span>' % (c, esc(nm))
                  for nm, c, _ in series)
    return '<div class="chwrap">%s<div class="legend">%s</div>%s</div>' % (
        "".join(p), leg, '<p class="note">%s</p>' % esc(note) if note else "")


def svg_lines(days, series, unit="%", h=210, note=""):
    """折线图。None 会把线断开，不会假装是 0。"""
    n = len(days)
    if n < 2:
        return ""
    pl, pr, pb, pt = 40, 14, 40, 16
    step = max(56, min(130, int(760 / (n - 1))))
    w = pl + (n - 1) * step + pr + 14
    flat = [v for _, _, vals in series for v in vals if v is not None]
    top = nice(max(flat + [1]))
    X = lambda i: pl + i * step
    Y = lambda v: pt + (h - pt - pb) * (1 - v / float(top))
    p = ['<svg viewBox="0 0 %d %d" class="ch" style="max-width:%dpx" '
         'preserveAspectRatio="xMinYMid meet" role="img">' % (w, h, w)]
    for g in (0, 0.25, 0.5, 0.75, 1):
        v = top * g
        p.append('<line class="gl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                 % (pl - 4, Y(v), w - 8, Y(v)))
        p.append('<text class="ax" x="%d" y="%.1f" text-anchor="end">%g</text>'
                 % (pl - 8, Y(v) + 4, v))
    for i, d in enumerate(days):
        p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>'
                 % (X(i), h - pb + 18, esc(short(d))))
        p.append('<text class="ax2" x="%.1f" y="%d" text-anchor="middle">%s</text>'
                 % (X(i), h - pb + 32, esc(wday(d))))
    for name, col, vals in series:
        seg = []
        for i, v in enumerate(vals):
            if v is None:
                if len(seg) > 1:
                    p.append('<polyline class="pl" stroke="%s" points="%s"/>'
                             % (col, " ".join("%.1f,%.1f" % q for q in seg)))
                seg = []
            else:
                seg.append((X(i), Y(v)))
        if len(seg) > 1:
            p.append('<polyline class="pl" stroke="%s" points="%s"/>'
                     % (col, " ".join("%.1f,%.1f" % q for q in seg)))
        for i, v in enumerate(vals):
            if v is None:
                continue
            p.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"><title>%s %s %.1f%s'
                     '</title></circle>'
                     % (X(i), Y(v), col, esc(short(days[i])), esc(name), v, unit))
        last = [(i, v) for i, v in enumerate(vals) if v is not None]
        if last:
            i, v = last[-1]
            p.append('<text class="vl" x="%.1f" y="%.1f" fill="%s">%.0f%s</text>'
                     % (X(i) + 7, Y(v) + 4, col, v, unit))
    p.append("</svg>")
    leg = "".join('<span class="lg"><i style="background:%s"></i>%s</span>' % (c, esc(nm))
                  for nm, c, _ in series)
    return '<div class="chwrap">%s<div class="legend">%s</div>%s</div>' % (
        "".join(p), leg, '<p class="note">%s</p>' % esc(note) if note else "")


def hbars(rows, unit="", width_of=None, dec=0):
    """横条。rows: [(标签, 数值, 右边那行小字)]。CSS 画的，比 SVG 清楚。"""
    rows = [r for r in rows]
    if not rows:
        return '<p class="note">没有数据</p>'
    top = max([abs(r[1]) for r in rows if r[1] is not None] + [1e-9])
    out = ['<div class="bars">']
    for lab, v, sub in rows:
        pctw = 0 if v is None else max(1.2, (width_of(v) if width_of else v / top) * 100)
        zero = (v == 0)
        out.append(
            '<div class="row"><div class="lab">%s</div>'
            '<div class="track"><div class="fill%s" style="width:%.1f%%"></div></div>'
            '<div class="val">%s</div><div class="sub">%s</div></div>'
            % (esc(lab), " zero" if zero else "", pctw,
               "—" if v is None else ("0" + unit if zero else "%.*f%s" % (dec, v, unit)),
               esc(sub)))
    out.append("</div>")
    return "".join(out)


# ────────────────────────────── 5. 组页面 ──────────────────────────────

CSS = """
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
"""

LV = {"good": "好", "bad": "坏", "warn": "注意", "info": "留意"}


def formula(fn):
    """把指标函数里那一行 return 直接印出来——公式不另抄一份，省得写的和算的不一样。"""
    import inspect
    try:
        lines = [l.strip() for l in inspect.getsource(fn).splitlines()]
    except Exception:
        return ""
    r = [l[7:] for l in lines if l.startswith("return ")]
    return r[-1] if r else ""


def cards(ctx):
    out = ['<div class="cards">']
    nb = len(ctx.base_days)
    for m in METRICS:
        f = m.fn(ctx.today)
        t = value(m, f)
        b = ctx.base_val(m.key)
        d = None if (t is None or b is None) else t - b
        bf = m.fn(ctx.base)
        cls = "flat"
        lab = "基线样本不够" if (isinstance(bf, Frac) and 0 < bf.b < m.min_b) else "没有基线可比"
        if d is not None:
            # 先按要显示的位数四舍五入再判断，不然 -0.5 会印成「-0」
            shown = round(d, m.dec)
            if shown == 0:
                lab = "和基线一样"
            else:
                cls = "neutral" if m.good == "neutral" else (
                    "up" if (shown > 0) == (m.good == "up") else "down")
                lab = "%+.*f%s" % (m.dec, shown, "pp" if m.unit == "%" else m.unit)
        bits = [x for x in (frac_txt(f),
                            "基线 %s%s" % (fmt(b, m), "/天" if m.per_day else "")) if x]
        out.append('<div class="c" title="%s"><div class="k">%s</div>'
                   '<div class="v">%s</div><div class="d %s">%s</div>'
                   '<div class="b">%s</div></div>'
                   % (esc("%s（基线 = 前 %d 天的同档口）" % (m.note, nb)), esc(m.name),
                      fmt(t, m), cls, esc(lab), esc(" · ".join(bits))))
    out.append("</div>")
    return "".join(out)


def findings(ctx):
    out = ['<div class="fin">']
    order = {"bad": 0, "warn": 1, "good": 2, "info": 3}
    got = []
    for r in RULES:
        try:
            f = r(ctx)
        except Exception as e:                       # 一条结论挂了不该拖垮整页
            f = Fin("warn", "结论 %s 算挂了" % r.__name__, "%s: %s" % (type(e).__name__, e))
        if f:
            got.append(f)
    for f in sorted(got, key=lambda f: order.get(f.lv, 9)):
        out.append('<div class="f %s"><div class="t"><i>%s</i>%s</div><div class="x">%s</div>'
                   "</div>" % (f.lv, LV.get(f.lv, "?"), esc(f.title), esc(f.text)))
    out.append("</div>")
    return "".join(out)


def table(head, rows, zero_cols=()):
    out = ["<table><tr>"]
    out += ["<th>%s</th>" % esc(h) for h in head]
    out.append("</tr>")
    for r in rows:
        out.append("<tr>")
        for i, cell in enumerate(r):
            z = " class='z'" if (i in zero_cols and cell in (0, "0", "—")) else ""
            out.append("<td%s>%s</td>" % (z, esc(str(cell))))
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)


def render(ctx):
    days = ctx.daylist
    dayb = [ctx.day[d] for d in days]
    sv = lambda s: [(ctx.svcb.get((d, s)).ses if (d, s) in ctx.svcb else 0) for d in days]
    gen = time.strftime("%m-%d %H:%M", time.localtime())
    svcs = "/".join(ctx.svcs)
    partial_note = "最后一天还没过完。" if ctx.partial else ""

    h = ['<!doctype html><html lang="zh"><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width,initial-scale=1">'
         '<meta name="color-scheme" content="light dark">'
         "<title>Sibisi 菜单数据 · %s</title><style>%s</style></head><body><div class='wrap'>"
         % (esc(ctx.today_day), CSS)]
    h.append("<h1>Sibisi 菜单数据</h1>")
    h.append('<p class="sub">%s – %s（%d 天有数据，共 %d 个会话 / %d 条事件）</p>'
             % (esc(days[0]), esc(days[-1]), len(days), ctx.all.ses, ctx.all.ev))
    h.append('<div class="snap">这是 <b>%s</b> 生成的快照，数字不会自己更新——'
             '重新跑 <b>collector/dash.sh</b> 就是最新的。<br>'
             '卡片上的大数字是 <b>%s 的%s</b>，「基线」是前 %d 天的同一档口（%s），'
             '所以半天不会拿去跟整天比。</div>'
             % (esc(gen), esc(ctx.today_day), esc(svcs), len(ctx.base_days), esc(svcs)))

    h.append("<h2>今天</h2>")
    h.append(cards(ctx))
    h.append("<h2>自动结论</h2>")
    h.append('<p class="note">每条结论是 dash.py 里一个 @rule 函数，阈值提前写死在函数里。'
             "数字满足条件它才出现，不满足就不出现。</p>")
    h.append(findings(ctx))

    h.append("<h2>每天多少人扫码</h2>")
    h.append(svg_stack(days, [("午市", C_LUNCH, sv("午市")), ("晚市", C_DINNER, sv("晚市"))],
                       note="按业务日分（早上 5 点切），%s周四休息。" % partial_note))

    h.append("<h2>关键比率的走势</h2>")
    h.append(svg_lines(days, [
        ("建了清单", C_LINE[0], [ctx.val("add_rate", b) for b in dayb]),
        ("菜单正文转化", C_LINE[1], [ctx.val("menu_conv", b) for b in dayb]),
        ("节气推荐转化", C_LINE[2], [ctx.val("luck_conv", b) for b in dayb]),
    ], note="线断开 = 那天这个指标没有分母，不是 0。%s" % partial_note))

    h.append("<h2>今天的漏斗</h2>")
    t, bs = ctx.today, ctx.base
    rows = []
    for lab, key in [("打开菜单", None), ("看到菜", "imp"), ("点开详情", "det"),
                     ("建了清单", "add"), ("给服务员看", "staff")]:
        n = t.ses if key is None else t.s[key]
        bn = bs.ses if key is None else bs.s[key]
        v = pc(n, t.ses)
        bv = pc(bn, bs.ses)
        rows.append((lab, v, "%d 个会话%s" % (n, "" if bv is None else " · 基线 %.0f%%" % bv)))
    h.append(hbars(rows, "%", width_of=lambda v: (v or 0) / 100.0))

    h.append("<h2>哪个区域在卖货</h2>")
    a = ctx.all
    rows = []
    CONV = {"menu": "menu_conv", "luck": "luck_conv", "first": "first_conv"}
    for s in WITH_IMP:
        rows.append((sname(s), ctx.val(CONV[s], a),
                     "%d 看到 → %d 点开 → %d 加入（%d 次）"
                     % (a.seen(s), a.srcs[(s, "det")], a.added(s), a.adds(s))))
    h.append(hbars(rows, "%", width_of=lambda v: (v or 0) / 100.0, dec=1))
    h.append('<p class="note">只有这三处会记「看到」，所以只有它们有分母。'
             "斜纹条 = 真的是 0，不是没数据。全期合计，不只今天。</p>")
    click = [(sname(s), a.srcs[(s, "add")], a.srcn[(s, "add")], a.srcn[(s, "drink")])
             for s in sorted({k[0] for k in a.srcs} - set(WITH_IMP))
             if a.srcs[(s, "add")] or a.srcn[(s, "drink")]]
    if click:
        h.append("<h3>点出来的区域（没有曝光，所以没有转化率）</h3>")
        h.append(table(["区域", "加入的会话", "加入次数", "饮料次数"],
                       sorted(click, key=lambda r: -r[2]), zero_cols=(1, 2, 3)))

    h.append("<h2>语言</h2>")
    langs = [l for l in ("es", "en", "zh", "?") if a.lang.get(l)]
    h.append(svg_stack(days, [(l, C_LANG.get(l, "#999"),
                               [ctx.day[d].lang.get(l, 0) for d in days]) for l in langs],
                       note="按会话打开菜单时的语言分。这项决定要不要加第四种语言。"))
    h.append(table(["语言", "会话", "给服务员看", "占该语言"],
                   [(l, a.lang[l], a.lang_staff[l],
                     "%.0f%%" % (pc(a.lang_staff[l], a.lang[l]) or 0)) for l in langs],
                   zero_cols=(2,)))

    h.append("<h2>菜</h2>")
    tadd = Counter({k[0]: v for k, v in t.dishn.items() if k[1] == "add"})
    h.append("<h3>今天加进清单最多的</h3>")
    if tadd:
        h.append(hbars([("%s %s" % (c, dname(c)), n,
                         "看到 %d 会话 · 点开 %d" % (t.dishs[(c, "imp")], t.dishs[(c, "det")]))
                        for c, n in tadd.most_common(8)], "次"))
    else:
        h.append('<p class="note">今天还没有人把菜加进清单。</p>')
    h.append("<h3>全期漏斗（按会话算，前 15）</h3>")
    codes = sorted({k[0] for k in a.dishs},
                   key=lambda c: (-a.dishs[(c, "add")], -a.dishs[(c, "imp")]))[:15]
    h.append(table(["菜", "看到", "点开", "加入", "看到→加入", "加入次数"],
                   [("%s %s" % (c, dname(c)), a.dishs[(c, "imp")], a.dishs[(c, "det")],
                     a.dishs[(c, "add")],
                     "%.0f%%" % pc(a.dishs[(c, "add")], a.dishs[(c, "imp")])
                     if a.dishs[(c, "imp")] else "—", a.dishn[(c, "add")]) for c in codes],
                   zero_cols=(1, 2, 3, 5)))

    h.append("<h2>饮料</h2>")
    if a.drink:
        h.append(hbars([(dname(k) or k, n, "%.2f €" % PRICE[k] if PRICE.get(k) else "")
                        for k, n in a.drink.most_common(10)], "次"))
        h.append('<p class="note">全期合计。推荐搭配默认选中的是 %s。</p>'
                 % esc(DEFAULT_DRINK[1]))
    else:
        h.append('<p class="note">还没有人点过饮料。</p>')

    h.append("<h2>设备和地区</h2>")
    h.append('<div class="two">')
    h.append(table(["国家", "会话"], a.country.most_common(8)))
    h.append(table(["屏幕宽度", "会话"],
                   [("%dpx%s" % (w, "（桌面）" if w >= DESK_W else ""), n)
                    for w, n in sorted(a.width.items(), key=lambda x: -x[1])[:8]]))
    h.append("</div>")

    h.append("<h2>这些数是怎么算的</h2>")
    h.append('<div class="gl2">')
    for m in METRICS:
        h.append('<div class="gi"><b>%s</b> <code>%s</code><span>%s</span></div>'
                 % (esc(m.name), esc(formula(m.fn)), esc(m.note)))
    h.append("</div>")
    h.append('<p class="note">b 是一堆会话的计数：b.ses 会话数、b.s[事件] 出现过该事件的'
             "会话数、b.n[事件] 次数、b.seen(区域) / b.added(区域) 该区域的曝光和加入会话数。"
             "想加指标就在 dash.py 的公式层加一个 @metric 函数，卡片和走势图自动跟着出来。</p>")

    h.append("<footer><b>口径，别绕过去：</b><ul>"
             "<li><b>ts 是上报时间，不是发生时间。</b>事件攒到 40 条或页面关掉才发一次，"
             "所以这里只用它分业务日和午市/晚市，不画「几点人最多」。</li>"
             "<li><b>「看到」卡得很严：</b>卡片露出一半并停留 1 秒才算，划过去不算；"
             "一道菜一个会话只记一次，同一个人反复点不会把分子撑大。</li>"
             "<li><b>「加入」不等于成单。</b>它只是进了清单。真实销量在店里那套 POS 里。</li>"
             "<li><b>只看得见扫码的人。</b>没扫码、直接问服务员的客人完全不在数据里，"
             "而扫码的人本身偏年轻、偏外国人。</li>"
             "<li><b>一天几十桌。</b>单项指标一天可能只有十几个数据点，别过度解读。</li>"
             "</ul></footer></div></body></html>")
    return "".join(h)


def main():
    meta, sessions = load(sys.stdin)
    if not sessions:
        sys.exit("这段时间一条数据都没有")
    sys.stdout.write(render(Ctx(meta, sessions)))


if __name__ == "__main__":
    main()
