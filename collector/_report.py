"""把 /s 返回的 JSON 排成人能读的样子。stats.sh 调它，不单独用。"""
import sys, json

d = json.load(sys.stdin)
if "error" in d:
    sys.exit("读取失败：口令不对，或者 Worker 上还没设 TOKEN")

t = d["total"]
ses, staff = t["sesiones"], t["al_camarero"]

print()
print("最近 %d 天" % d["dias"])
print("=" * 36)
print("  扫码看菜单   %6d 次" % ses)
print("  给服务员看   %6d 次   (%s%%)" % (staff, t["al_camarero_pct"]))
print("  事件总数     %6d" % t["eventos"])

if ses < 50:
    print()
    print("  ⚠ 样本还太小，数字波动基本是噪声，攒够一周再看。")


def block(title, rows, k, v, note=""):
    if not rows:
        return
    print()
    print(title + note)
    print("-" * 36)
    top = max(r[v] for r in rows) or 1
    for r in rows:
        bar = "█" * max(1, round(r[v] / top * 16))
        print("  %-6s %5d  %s" % (r[k], r[v], bar))


block("开菜单时的语言", d["idioma_inicial"], "idioma", "sesiones",
      "   ← 这项决定要不要加第四种语言")
block("中途切到的语言", d["cambios_de_idioma"], "a_idioma", "veces")
block("访客所在国家", d["paises"], "pais", "sesiones")

if d["por_dia"]:
    print()
    print("按天")
    print("-" * 36)
    for r in d["por_dia"][:14]:
        print("  %s   %3d 次扫码   %3d 次给服务员看"
              % (r["dia"], r["sesiones"], r["al_camarero"]))
print()
