#!/bin/sh
# 生成并打开数据看板。
#
#   ./dash.sh          最近 14 天
#   ./dash.sh 30       最近 30 天
#   ./dash.sh 14 x     只生成不打开
#
# 口令从登录钥匙串取：不用手输，不进命令历史，也不会写进生成的 HTML。
# 生成的是**快照**——数字不会自己更新，想看最新的就再跑一次。
set -eu

URL=https://sibisi-stats.cartaviva.workers.dev
DAYS=${1:-14}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/out/dashboard.html

TOKEN=$(security find-generic-password -a sibisi-stats -s sibisi-stats-token -w 2>/dev/null) || {
  echo "钥匙串里没找到口令。重新设一个：" >&2
  echo "  T=\$(openssl rand -hex 24)" >&2
  echo "  printf '%s' \"\$T\" | npx wrangler secret put TOKEN" >&2
  echo "  security add-generic-password -U -a sibisi-stats -s sibisi-stats-token -w \"\$T\"" >&2
  exit 1
}

mkdir -p "$HERE/out"
JSON=$(curl -sS --max-time 60 "$URL/r?k=$TOKEN&d=$DAYS")
unset TOKEN

# 先写到临时文件再换上去：拉数据或者算指标挂了的话，上一版看板还在，不会只剩个空页面
printf '%s' "$JSON" | python3 "$HERE/dash.py" > "$OUT.tmp"
mv "$OUT.tmp" "$OUT"
echo "$OUT"
[ "${2:-}" = "x" ] || open "$OUT"
