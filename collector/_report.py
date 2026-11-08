"""把 /s 返回的 JSON 排成人能读的样子。stats.sh 调它，不单独用。

菜名和来源名在 `_names.py` 里，报表和 dashboard 共用，改菜单这边不用动。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _names import NAME, SRCN            # noqa: E402


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

fuentes = d.get("fuentes") or []
if fuentes:
    print()
    print("各区域的表现（按多少个会话算）")
    print("-" * 52)
    print("  %s %4s %4s %4s   %s" % (pad("区域", 20), "看到", "点开", "加入", "看到→加入"))
    for r in fuentes:
        visto, an = r["visto"], r["anadido"]
        pct = ("%.0f%%" % (an / visto * 100)) if visto else "—"
        beb = "  (饮料 %d)" % r["bebida"] if r["bebida"] else ""
        print("  %s %4d %4d %4d   %6s%s"
              % (pad(SRCN.get(r["fuente"], r["fuente"]), 20), visto, r["abierto"], an, pct, beb))
    print()
    print("  只有菜单正文、节气推荐、顶层推荐三处会记「看到」，其余是点出来的，所以没有分母。")
    print("  推荐搭配整套 / 多人套餐 / 加小菜列表的「加入」是按下一个按钮带进去的一批菜。")

pxf = d.get("plato_x_fuente") or []
if pxf:
    by = {}
    for r in pxf:
        by.setdefault(r["plato"], []).append((r["fuente"], r["anadido"]))
    print()
    print("每道菜是从哪儿被点走的")
    print("-" * 52)
    for code, lst in sorted(by.items(), key=lambda x: -sum(n for _, n in x[1]))[:20]:
        lst.sort(key=lambda x: -x[1])
        src = " · ".join("%s %d" % (SRCN.get(f, f), n) for f, n in lst)
        print("  %s %s" % (label(code), src))
    print()
    print("  一道菜大部分来自节气或顶层推荐，说明是「被推出去的」，不是自己被挑中的。")

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
