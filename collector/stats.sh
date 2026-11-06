#!/bin/sh
# 看统计报表。口令从登录钥匙串里取，不用手输，也不进命令历史。
#
#   ./stats.sh          最近 14 天
#   ./stats.sh 7        最近 7 天
#   ./stats.sh 90 raw   最近 90 天，原始 JSON
set -eu

URL=https://sibisi-stats.cartaviva.workers.dev
DAYS=${1:-14}
HERE=$(dirname "$0")

TOKEN=$(security find-generic-password -a sibisi-stats -s sibisi-stats-token -w 2>/dev/null) || {
  echo "钥匙串里没找到口令。重新设一个：" >&2
  echo "  T=\$(openssl rand -hex 24)" >&2
  echo "  printf '%s' \"\$T\" | npx wrangler secret put TOKEN" >&2
  echo "  security add-generic-password -U -a sibisi-stats -s sibisi-stats-token -w \"\$T\"" >&2
  exit 1
}

JSON=$(curl -sS --max-time 20 "$URL/s?k=$TOKEN&d=$DAYS")
unset TOKEN

if [ "${2:-}" = "raw" ]; then
  echo "$JSON"
else
  echo "$JSON" | python3 "$HERE/_report.py"
fi
