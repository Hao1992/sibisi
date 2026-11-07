"""Rebuild ../index.html from data.py + det.py.  Run:  python3 source/build.py  (from repo root)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import *
from det import DET
rd = lambda f: open(os.path.join(HERE, f), encoding="utf-8").read()
js = rd("app.js.tpl")
J = lambda o: json.dumps(o, ensure_ascii=False)
for k, v in dict(T=T, LBL=LBL, ALGN=ALGN, TASTE=TASTE, S=S, FIRST=FIRST, EXTRAS=EXTRAS, DR=DR, SIDE=SIDE, DRK=DRK, PR=PR, DET=DET, SP=SP, CT=CT, CORI=CORI, DRKMAP=DRKMAP, UPSELL=UPSELL, TEL=TEL, MAP=MAP, REV=REV, TOP=TOP, FRONT=FRONT, GRP=GRP, COMBO=COMBO, JQ=JQ, JQW=JQW, HANZI=HANZI, SAYING=SAYING, CHOP=CHOP, HOURS=HOURS, DRILL=DRILL, DRILLV=DRILLV, BRAND=BRAND, BYURL=BYURL, STATS=STATS).items():
    js = js.replace("__%s__" % k, J(v))
js = js.replace("__ILLO__", rd("illo.part"))
# head2.part 以前不做 token 替换，所以电话号码只能写死在里面。
# 这两个是原样插入的（不是 JSON，不带引号）：一个进 href，一个当可见文字
head = rd("head2.part")
for k, v in dict(TELRAW=TEL, TELTXT=TELTXT).items():
    assert "__%s__" % k in head, "head2.part 里找不到 __%s__" % k
    head = head.replace("__%s__" % k, v)
head = head.replace(".alab{", ".algbox{display:grid;gap:4px}\n.algbox dt{font-size:12px;font-weight:800;letter-spacing:.08em;color:var(--red)}\n.alab{", 1)
body = head + "<script>\n" + js + "</script>\n"
title = re.search(r"<title>(.*?)</title>", body).group(1)
body = body.replace("<title>%s</title>" % title, "", 1)
links = re.findall(r"<link [^>]*>", body)
for l in links: body = body.replace(l, "", 1)
style = re.search(r"<style>.*?</style>", body, re.S).group(0)
body = body.replace(style, "", 1)
doc = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<title>Sibisi Ramen · Carta · 菜单 · Menu</title>
<meta name="description" content="Carta de Sibisi Ramen, Valencia: ollas Huangmen y fideos hechos a mano. Español, English, 中文.">
<link rel="icon" href="img/logo.jpg">
%s
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style>
%s
</head>
<body>
%s
</body>
</html>
""" % ("\n".join(links), style, body.strip())
out = os.path.join(HERE, "..", "index.html")
open(out, "w", encoding="utf-8").write(doc)
# sanity: every img referenced exists
names = set(re.findall(r'"img": "([\w-]+)"', doc))
missing = [m for m in names if not os.path.exists(os.path.join(HERE, "..", "img", m + ".jpg"))]
# 列表用 img/t/ 下的 192px 缩略图，详情页用原图：两边都得在
nothumb = [m for m in names if not os.path.exists(os.path.join(HERE, "..", "img", "t", m + ".jpg"))]
# 号码只能在 data.py 的 TEL 里出现。这个检查是防回归的——
# 它本来就在 head2.part 和 app.js.tpl 里各写死过一份
for f in ("app.js.tpl", "head2.part", "illo.part"):
    src = rd(f)
    for lit in (TEL, TELTXT, TEL[3:]):
        if lit in src:
            sys.exit("source/%s 里又写死了电话号码 %r。号码只放 data.py 的 TEL" % (f, lit))

print("built index.html", "| missing images:", missing or "none", "| missing thumbs:", nothumb or "none")
