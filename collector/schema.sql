-- 第 0 期只有一张表。原始事件留着，聚合随时能算，聚合存下来原始就没了。
CREATE TABLE IF NOT EXISTS ev (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  ts      INTEGER NOT NULL,   -- 服务端收到的时间（毫秒）。不信客户端的钟
  sid     TEXT    NOT NULL,   -- 会话 id：只存在那台手机的内存里，关掉页面就没了
  name    TEXT    NOT NULL,   -- open | lang | staff
  v       TEXT,               -- 事件附带的值（open 带初始语言，lang 带切到哪个语言）
  w       INTEGER,            -- 屏幕宽度，按 60px 分桶，不存精确值
  country TEXT                -- 只存国家代码。IP 明确丢弃，不入库
);
CREATE INDEX IF NOT EXISTS ev_ts   ON ev(ts);
CREATE INDEX IF NOT EXISTS ev_name ON ev(name, ts);
