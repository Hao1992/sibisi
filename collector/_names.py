"""菜号 / 来源代码 → 看得懂的名字 + 价格。报表和 dashboard 共用这一份。

菜名直接读 `source/data.py`，所以改了菜单这边不用跟着改。
`SRCN` 的键必须和 `app.js.tpl` 的 `SRC`、`worker.js` 的 `SRCS` 对得上——
少一个这边只会显示原始代码，不报错，所以加新区域时三处要一起改。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

NAME = {}
PRICE = {}
# 推荐加点里默认选中的那一款饮料。dashboard 要拿它和「客人自己翻酒水单最常点的」比
DEFAULT_DRINK = ("dr-beers-0", "dr-beers-0", None)


def _t(x):
    """data.py 里的名字有两种写法：三语列表 ['中','es','en'] 或者单个字符串。
    写成 x[0] 的话字符串形式会被取成第一个字母（"Amstel 1/3" → "A"）。"""
    return x[0] if isinstance(x, (list, tuple)) else x


try:
    sys.path.insert(0, os.path.join(HERE, "..", "source"))
    import data as _d
    for _s in _d.S:
        for _dish in _s["d"]:
            NAME[_dish["c"]] = _dish["zh"]
            PRICE[_dish["c"]] = _dish.get("p")
    for _c in _d.COMBO:
        NAME[_c["id"]] = "套餐 " + _t(_c.get("zh", _c["id"]))
    for _k, _v in _d.DRK.items():                  # 推荐加点用的饮料键
        NAME[_k], PRICE[_k] = _t(_v[0]), _v[1]
    # 酒水单里的饮料 id 是「分类-序号」，和 DRK 是两套键，两套都要能翻
    for _cat, _lst in _d.DR.items():
        for _i, _x in enumerate(_lst):
            _id = "dr-%s-%d" % (_cat, _i)
            NAME[_id], PRICE[_id] = _t(_x[0]), _x[1]
    DEFAULT_DRINK = ("dr-beers-0", NAME.get("dr-beers-0", "dr-beers-0"), PRICE.get("dr-beers-0"))
except Exception:
    pass                                            # 读不到就只显示代码，不让报表挂掉

# 来源代码 → 看得懂的名字
SRCN = {
    "menu": "菜单正文",
    "luck": "节气推荐",
    "first": "顶层推荐",
    "hero": "首屏按钮",
    "det": "详情页里",
    "pairbox": "推荐搭配整套",
    "order": "结算前加点",
    "pick": "加小菜/饮料列表",
    "pack": "多人套餐",
    "drinks": "酒水单",
    "(旧)": "(旧数据，未分来源)",
}

# 只有这三处会记「看到」，所以只有它们能算「看到→加入」的转化率。
# 其余区域的「加入」是按钮点出来的，没有分母
WITH_IMP = ("menu", "luck", "first")

sname = lambda s: SRCN.get(s, s or "(无)")
dname = lambda c: NAME.get(c, "")
