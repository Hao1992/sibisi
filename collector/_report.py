"""把 /s 返回的 JSON 排成人能读的样子。stats.sh 调它，不单独用。

菜号到菜名的对照直接读 source/data.py，所以改了菜单这边不用跟着改。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = {}
try:
    sys.path.insert(0, os.path.join(HERE, "..", "source"))
    import data as _d
    for _s in _d.S:
        for _dish in _s["d"]:
            NAME[_dish["c"]] = _dish["zh"]
    for _c in _d.COMBO:
        NAME[_c["id"]] = "套餐 " + _c.get("zh", _c["id"])
    for _k, _v in _d.DRK.items():
        NAME[_k] = _v[0][0]
    # 酒水单里的饮料 id 是「分类-序号」，和推荐加点用的 DRK 键是两套，两套都要能翻
    for _cat, _lst in _d.DR.items():
        for _i, _x in enumerate(_lst):
            NAME["dr-%s-%d" % (_cat, _i)] = _x[0][0]
except Exception:
    pass            # 读不到就只显示菜号，不让报表挂掉


def w(s):
    """终端显示宽度。中文、日文这些是双宽，按字符数补空格会错位。"""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s, width):
    """按显示宽度截断并右补空格。"""
    out = ""
    for c in s:
        if w(out) + w(c) > width:
            break
        out += c
    return out + " " * (width - w(out))


def label(code, width=24):
    n = NAME.get(code, "")
    return pad("%-5s %s" % (code, n) if n else code, width)


def bars(rows, k, v, width=16):
    top = max((r[v] for r in rows), default=0) or 1
    for r in rows:
        print("  %-6s %5d  %s" % (r[k], r[v], "█" * max(1, round(r[v] / top * width))))


d = json.load(sys.stdin)
if "error" in d:
    sys.exit("读取失败：口令不对，或者 Worker 上还没设 TOKEN")

t = d["total"]
ses = t["sesiones"]

print()
print("最近 %d 天" % d["dias"])
print("=" * 52)
print("  扫码看菜单   %6d 次" % ses)
print("  给服务员看   %6d 次   (%s%%)" % (t["al_camarero"], t["al_camarero_pct"]))
print("  事件总数     %6d" % t["eventos"])
if ses < 50:
    print()
    print("  ⚠ 样本还太小，数字波动基本是噪声，攒够一周再看。")

platos = d.get("platos") or []
if platos:
    print()
    print("菜品漏斗（按多少个会话算，不是按次数）")
    print("-" * 52)
    print("  %s %4s %4s %4s   %s" % (pad("菜", 24), "看到", "点开", "加入", "看到→加入"))
    for r in platos[:40]:
        visto, ab, an = r["visto"], r["abierto"], r["anadido"]
        pct = ("%.0f%%" % (an / visto * 100)) if visto else "—"
        sug = "  (推荐搭配 %d)" % r["por_sugerencia"] if r["por_sugerencia"] else ""
        print("  %s %4d %4d %4d   %6s%s" % (label(r["plato"]), visto, ab, an, pct, sug))
    print()
    print("  「看到」= 卡片露出一半并停留 1 秒，划过去的不算，一道菜一个会话只记一次。")
    print("  「加入」不等于成单——真实销量在店里那套 POS 里。")

for title, rows, k, v, note in [
    ("开菜单时的语言", d["idioma_inicial"], "idioma", "sesiones",
     "   ← 这项决定要不要加第四种语言"),
    ("中途切到的语言", d["cambios_de_idioma"], "a_idioma", "veces", ""),
    ("多人套餐", d.get("packs") or [], "pack", "sesiones", ""),
    ("饮料", d.get("bebidas") or [], "bebida", "sesiones", ""),
    ("访客所在国家", d["paises"], "pais", "sesiones", ""),
]:
    if not rows:
        continue
    print()
    print(title + note)
    print("-" * 52)
    if title in ("多人套餐", "饮料"):
        top = max(r[v] for r in rows) or 1
        for r in rows:
            print("  %s %4d  %s" % (label(r[k], 26), r[v],
                                    "█" * max(1, round(r[v] / top * 16))))
    else:
        bars(rows, k, v)

if d["por_dia"]:
    print()
    print("按天")
    print("-" * 52)
    for r in d["por_dia"][:14]:
        print("  %s   %3d 次扫码   %3d 次给服务员看"
              % (r["dia"], r["sesiones"], r["al_camarero"]))
print()
