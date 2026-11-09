#!/bin/sh
# 打开数据看板。
#
# 其实平时用不着这个脚本——看板就是一个网址，手机上存成书签，打开就是当下的数字：
#
#     https://sibisi-stats.cartaviva.workers.dev/d?k=看板口令
#
# 这里只是帮你把口令从钥匙串里取出来拼上，省得手打。
#
#   ./dash.sh          最近 14 天，在浏览器里打开
#   ./dash.sh 30       最近 30 天
#   ./dash.sh 14 s     不开浏览器，存一份到 out/dashboard.html（离线留档用）
#
# 口令从登录钥匙串取：不进文件，也不进命令历史。
# 看板专用的那个（sibisi-dash-token）跟脚本用的 sibisi-stats-token 是两个，
# 手机上那份想换就换，不影响这边。
set -eu

URL=https://sibisi-stats.cartaviva.workers.dev
DAYS=${1:-14}
HERE=$(cd "$(dirname "$0")" && pwd)

TOKEN=$(security find-generic-password -a sibisi-dash -s sibisi-dash-token -w 2>/dev/null) \
  || TOKEN=$(security find-generic-password -a sibisi-stats -s sibisi-stats-token -w 2>/dev/null) || {
  echo "钥匙串里没找到看板口令。新设一个：" >&2
  echo "  T=\$(openssl rand -hex 24)" >&2
  echo "  printf '%s' \"\$T\" | npx wrangler secret put DASH_TOKEN" >&2
  echo "  security add-generic-password -U -a sibisi-dash -s sibisi-dash-token -w \"\$T\"" >&2
  exit 1
}

if [ "${2:-}" = "s" ]; then
  mkdir -p "$HERE/out"
  OUT=$HERE/out/dashboard.html
  # 先写临时文件再换上去：抓挂了的话上一份还在，不会只剩个空页面
  # bare=1：存下来的 HTML 里不带换窗口的链接，也就不带口令
  curl -sS --fail --max-time 60 "$URL/d?k=$TOKEN&d=$DAYS&bare=1" > "$OUT.tmp"
  mv "$OUT.tmp" "$OUT"
  echo "$OUT"
else
  open "$URL/d?k=$TOKEN&d=$DAYS"
fi
