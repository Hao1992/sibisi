// 菜单统计收集器（第 0 期）。只认三个事件，不碰 IP，不发 cookie。
// 部署：见 README.md

// 白名单之外的事件名服务端一律丢掉。菜单那边加新埋点，这里要同步加
const NAMES = new Set([
  "open", "lang", "staff",                      // 第 0 期：会话层
  "imp", "det", "add", "pair", "combo", "drink" // 第 1 期：菜品层
]);
const MAX_BODY = 8 * 1024;   // 一次最多 8 KB，超了直接丢
const MAX_EVENTS = 50;       // 一批最多 50 条
const DAY = 86400000;
const KEEP_DAYS = 90;        // 原始事件只留 90 天，之后自动删掉

const allowed = (env) => String(env.ORIGIN || "").split(",").map((x) => x.trim()).filter(Boolean);

const cors = (origin) => ({
  "Access-Control-Allow-Origin": origin,
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
});

export default {
  async fetch(req, env) {
    const origin = allowed(env)[0] || "*";
    const url = new URL(req.url);

    if (req.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(origin) });
    }
    if (url.pathname === "/c" && req.method === "POST") {
      return collect(req, env, origin);
    }
    if (url.pathname === "/s" && req.method === "GET") {
      return stats(url, env);
    }
    return new Response("sibisi-stats", { status: 200 });
  },

  // 每天跑一次，删掉过了保留期的原始事件。
  // README 里写了「原始事件留 60–90 天」，这个钩子就是把那句话落实了，
  // 不靠人记得去清。按天聚合的长期趋势是第 2 期报表页的事。
  async scheduled(_evt, env, ctx) {
    ctx.waitUntil(
      env.DB.prepare("DELETE FROM ev WHERE ts < ?")
        .bind(Date.now() - KEEP_DAYS * DAY)
        .run()
    );
  },
};

async function collect(req, env, origin) {
  const head = { ...cors(origin), "Content-Type": "application/json" };
  const ok = (n) => new Response(JSON.stringify({ ok: true, n }), { headers: head });
  const no = (why) => new Response(JSON.stringify({ ok: false, why }), { status: 400, headers: head });

  // 浏览器一定会带 Origin。带了但不在白名单里就拒掉，挡住别的网站拿这个口灌数据。
  // 挡不住 curl（公开的收集口都挡不住），所以下面每个字段还是要自己验。
  const from = req.headers.get("Origin");
  if (from && !allowed(env).includes(from)) return no("origin");

  // sendBeacon 发的是 text/plain，这样不会触发 CORS 预检，省一个往返
  const raw = await req.text();
  if (raw.length > MAX_BODY) return no("too big");

  let b;
  try { b = JSON.parse(raw); } catch { return no("bad json"); }

  const sid = typeof b.s === "string" ? b.s.slice(0, 64) : "";
  if (!sid) return no("no sid");
  if (!Array.isArray(b.e) || !b.e.length) return no("no events");

  // 屏幕宽度按 60px 分桶：知道大概是手机还是平板就够了，不需要精确值
  const w = Number.isFinite(b.w) ? Math.round(Math.min(b.w, 3000) / 60) * 60 : null;

  // 国家来自 Cloudflare 的边缘信息。IP 本身既不读也不存
  const country = (req.cf && req.cf.country) || null;

  const now = Date.now();
  const rows = [];
  for (const e of b.e.slice(0, MAX_EVENTS)) {
    if (!Array.isArray(e)) continue;
    const name = String(e[0] || "");
    if (!NAMES.has(name)) continue;                    // 白名单之外的一律丢掉
    const v = e[1] == null ? null : String(e[1]).slice(0, 40);
    rows.push([now, sid, name, v, w, country]);
  }
  if (!rows.length) return no("nothing valid");

  const stmt = env.DB.prepare(
    "INSERT INTO ev (ts, sid, name, v, w, country) VALUES (?, ?, ?, ?, ?, ?)"
  );
  await env.DB.batch(rows.map((r) => stmt.bind(...r)));
  return ok(rows.length);
}

async function stats(url, env) {
  const json = (o, s = 200) =>
    new Response(JSON.stringify(o, null, 1), {
      status: s,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });

  if (!env.TOKEN || url.searchParams.get("k") !== env.TOKEN) {
    return json({ error: "nope" }, 401);
  }
  const days = Math.min(Math.max(parseInt(url.searchParams.get("d") || "14", 10) || 14, 1), 90);
  const since = Date.now() - days * DAY;

  const byDay = await env.DB.prepare(
    `SELECT date(ts/1000, 'unixepoch') AS dia,
            COUNT(DISTINCT sid)                                   AS sesiones,
            COUNT(DISTINCT CASE WHEN name='staff' THEN sid END)   AS al_camarero
     FROM ev WHERE ts > ? GROUP BY dia ORDER BY dia DESC`
  ).bind(since).all();

  // 初始语言：每个会话的第一个 open 事件
  const byLang = await env.DB.prepare(
    `SELECT v AS idioma, COUNT(DISTINCT sid) AS sesiones
     FROM ev WHERE ts > ? AND name='open' AND v IS NOT NULL
     GROUP BY v ORDER BY sesiones DESC`
  ).bind(since).all();

  const switches = await env.DB.prepare(
    `SELECT v AS a_idioma, COUNT(*) AS veces
     FROM ev WHERE ts > ? AND name='lang' GROUP BY v ORDER BY veces DESC`
  ).bind(since).all();

  const byCountry = await env.DB.prepare(
    `SELECT COALESCE(country,'??') AS pais, COUNT(DISTINCT sid) AS sesiones
     FROM ev WHERE ts > ? GROUP BY pais ORDER BY sesiones DESC LIMIT 15`
  ).bind(since).all();

  // 菜品漏斗：看到 → 点开 → 加进清单。三层都按「多少个会话」算，不是按次数，
  // 所以同一个人反复点同一道菜不会把分子撑大，相除才是真的转化率。
  const platos = await env.DB.prepare(
    `SELECT v AS plato,
            COUNT(DISTINCT CASE WHEN name='imp'  THEN sid END) AS visto,
            COUNT(DISTINCT CASE WHEN name='det'  THEN sid END) AS abierto,
            COUNT(DISTINCT CASE WHEN name='add'  THEN sid END) AS anadido,
            COUNT(DISTINCT CASE WHEN name='pair' THEN sid END) AS por_sugerencia
     FROM ev
     WHERE ts > ? AND v IS NOT NULL AND name IN ('imp','det','add','pair')
     GROUP BY v
     ORDER BY anadido DESC, visto DESC
     LIMIT 80`
  ).bind(since).all();

  const packs = await env.DB.prepare(
    `SELECT v AS pack, COUNT(DISTINCT sid) AS sesiones
     FROM ev WHERE ts > ? AND name='combo' AND v IS NOT NULL
     GROUP BY v ORDER BY sesiones DESC`
  ).bind(since).all();

  const bebidas = await env.DB.prepare(
    `SELECT v AS bebida, COUNT(DISTINCT sid) AS sesiones
     FROM ev WHERE ts > ? AND name='drink' AND v IS NOT NULL
     GROUP BY v ORDER BY sesiones DESC LIMIT 20`
  ).bind(since).all();

  const tot = await env.DB.prepare(
    `SELECT COUNT(DISTINCT sid)                                 AS sesiones,
            COUNT(DISTINCT CASE WHEN name='staff' THEN sid END) AS al_camarero,
            COUNT(*)                                            AS eventos
     FROM ev WHERE ts > ?`
  ).bind(since).first();

  const conv = tot && tot.sesiones ? +(tot.al_camarero / tot.sesiones * 100).toFixed(1) : 0;

  return json({
    dias: days,
    total: { ...tot, al_camarero_pct: conv },
    por_dia: byDay.results,
    idioma_inicial: byLang.results,
    cambios_de_idioma: switches.results,
    paises: byCountry.results,
    platos: platos.results,
    packs: packs.results,
    bebidas: bebidas.results,
  });
}
