#!/usr/bin/env python3
"""Dream — "Everyone's dreams" aggregate server.

Stores only anonymous summaries (keywords, feelings, day, country, optional age band / gender)
under a random install ID. Never stores dream text. Every number it returns is computed over
at least K different people; smaller groups are withheld.

Standard library only. Listens on 127.0.0.1; put Caddy or nginx in front for HTTPS.
"""
import csv, hashlib, hmac, io, json, os, re, sqlite3, threading, time, uuid
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DB = os.environ.get("DREAM_DB", "/var/lib/dream-server/dream.db")
PORT = int(os.environ.get("DREAM_PORT", "8787"))
K = int(os.environ.get("DREAM_MIN_PEOPLE", "10"))
ADMIN_TOKEN = os.environ.get("DREAM_ADMIN_TOKEN", "")
ADMIN_ORIGIN = os.environ.get("DREAM_ADMIN_ORIGIN", "https://iwakeupeverymorninginordertodream.com")

AGES = {"", "10s", "20s", "30s", "40s", "50s+"}
GENDERS = {"", "f", "m", "x"}
FEELINGS = {"uneasy", "fear", "sad", "nostalgic", "calm", "joy", "anger", "love", "surprise"}

_lock = threading.Lock()
_rate = {}


def db():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    return c


def init():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS entries(
          device TEXT NOT NULL, day TEXT NOT NULL, country TEXT NOT NULL DEFAULT '',
          age TEXT NOT NULL DEFAULT '', gender TEXT NOT NULL DEFAULT '',
          words TEXT NOT NULL DEFAULT '[]', feelings TEXT NOT NULL DEFAULT '[]',
          created INTEGER NOT NULL, PRIMARY KEY(device, day));
        CREATE INDEX IF NOT EXISTS entries_day ON entries(day);
        CREATE TABLE IF NOT EXISTS events(
          day TEXT NOT NULL, scope TEXT NOT NULL, title_ja TEXT NOT NULL, title_en TEXT NOT NULL,
          PRIMARY KEY(day, scope, title_en));
        """)


def clean_word(w):
    w = re.sub(r"\s+", " ", str(w)).strip().lower()[:20]
    if not w or re.search(r"[@/\\]|\d{3,}|https?:", w):
        return ""
    return w


def limited(ip, n=60):
    now = int(time.time() // 60)
    with _lock:
        key = (ip, now)
        _rate[key] = _rate.get(key, 0) + 1
        if len(_rate) > 10000:
            for k in [k for k in _rate if k[1] < now]:
                _rate.pop(k, None)
        return _rate[key] > n


def summary(q):
    days = max(1, min(31, int((q.get("days") or ["7"])[0] or 7)))
    end = (q.get("day") or [date.today().isoformat()])[0]
    try:
        end_d = date.fromisoformat(end)
    except ValueError:
        end_d = date.today()
    start = (end_d - timedelta(days=days - 1)).isoformat()
    where, args = ["day BETWEEN ? AND ?"], [start, end_d.isoformat()]
    for key, col, allowed in (("country", "country", None), ("age", "age", AGES), ("gender", "gender", GENDERS)):
        v = (q.get(key) or [""])[0]
        if v and (allowed is None and re.fullmatch(r"[A-Z]{2}", v) or allowed and v in allowed):
            where.append(f"{col} = ?"); args.append(v)
    with db() as c:
        rows = c.execute(f"SELECT device, country, words, feelings FROM entries WHERE {' AND '.join(where)}", args).fetchall()
        events = [dict(r) for r in c.execute(
            "SELECT day, scope, title_ja, title_en FROM events WHERE day BETWEEN ? AND ? ORDER BY day DESC", (start, end_d.isoformat()))]
    people = {r["device"] for r in rows}
    out = {"k": K, "from": start, "to": end_d.isoformat(), "enough": len(people) >= K, "events": events}
    if len(people) < K:
        return out
    word_people, feel_people, country_people = {}, {}, {}
    for r in rows:
        for w in set(json.loads(r["words"])):
            word_people.setdefault(w, set()).add(r["device"])
        for f in set(json.loads(r["feelings"])):
            feel_people.setdefault(f, set()).add(r["device"])
        if r["country"]:
            country_people.setdefault(r["country"], set()).add(r["device"])
    n = len(people)
    out.update({
        "people": n,
        "dreams": len(rows),
        "words": [{"word": w, "people": len(p), "share": round(len(p) / n, 3)}
                  for w, p in sorted(word_people.items(), key=lambda kv: -len(kv[1])) if len(p) >= K][:10],
        "feelings": [{"feeling": f, "share": round(len(p) / n, 3)}
                     for f, p in sorted(feel_people.items(), key=lambda kv: -len(kv[1])) if len(p) >= K],
        "countries": [{"country": c_, "people": len(p)}
                      for c_, p in sorted(country_people.items(), key=lambda kv: -len(kv[1])) if len(p) >= K],
    })
    return out


# ---- Admin export (token required). Rows carry no dream text, names or IPs; the install ID is
# replaced by a one-way pseudonym so exported files can't be matched back to a device.
EXPORT_KINDS = ("entries", "daily", "words", "feelings", "countries", "demographics")


def pseudo(dev):
    return hmac.new(ADMIN_TOKEN.encode(), dev.encode(), hashlib.sha256).hexdigest()[:12]


def export_rows(kind, start, end):
    with db() as c:
        rows = c.execute("SELECT device, day, country, age, gender, words, feelings, created FROM entries "
                         "WHERE day BETWEEN ? AND ? ORDER BY day, device", (start, end)).fetchall()
    if kind == "entries":
        yield ["day", "person", "country", "age", "gender", "words", "feelings"]
        for r in rows:
            yield [r["day"], pseudo(r["device"]), r["country"], r["age"], r["gender"],
                   " / ".join(json.loads(r["words"])), " ".join(json.loads(r["feelings"]))]
        return
    if kind == "daily":
        first = {}
        with db() as c:
            for r in c.execute("SELECT device, MIN(day) AS d FROM entries GROUP BY device"):
                first[r["device"]] = r["d"]
        days = {}
        for r in rows:
            d = days.setdefault(r["day"], {"dreams": 0, "people": set()})
            d["dreams"] += 1; d["people"].add(r["device"])
        yield ["day", "dreams", "people", "new_people"]
        for day in sorted(days):
            ppl = days[day]["people"]
            yield [day, days[day]["dreams"], len(ppl), sum(1 for p in ppl if first.get(p) == day)]
        return
    if kind in ("words", "feelings", "countries"):
        people, dreams = {}, {}
        for r in rows:
            vals = (set(json.loads(r["words"])) if kind == "words" else
                    set(json.loads(r["feelings"])) if kind == "feelings" else
                    ({r["country"]} if r["country"] else set()))
            for v in vals:
                people.setdefault(v, set()).add(r["device"]); dreams[v] = dreams.get(v, 0) + 1
        total = len({r["device"] for r in rows}) or 1
        yield [{"words": "word", "feelings": "feeling", "countries": "country"}[kind], "people", "dreams", "share_of_people"]
        for v, p in sorted(people.items(), key=lambda kv: -len(kv[1])):
            yield [v, len(p), dreams[v], round(len(p) / total, 4)]
        return
    if kind == "demographics":
        groups = {}
        for r in rows:
            g = groups.setdefault((r["age"] or "-", r["gender"] or "-"), {"people": set(), "dreams": 0})
            g["people"].add(r["device"]); g["dreams"] += 1
        yield ["age", "gender", "people", "dreams"]
        for (a, g), v in sorted(groups.items()):
            yield [a, g, len(v["people"]), v["dreams"]]


def overview():
    with db() as c:
        r = c.execute("SELECT COUNT(*) AS dreams, COUNT(DISTINCT device) AS people, MIN(day) AS first, MAX(day) AS last FROM entries").fetchone()
        week = (date.today() - timedelta(days=6)).isoformat()
        w = c.execute("SELECT COUNT(*) AS dreams, COUNT(DISTINCT device) AS people FROM entries WHERE day >= ?", (week,)).fetchone()
    return {"dreams": r["dreams"], "people": r["people"], "first_day": r["first"], "last_day": r["last"],
            "last7_dreams": w["dreams"], "last7_people": w["people"], "k_public": K}


class H(BaseHTTPRequestHandler):
    server_version = "dream/1"

    def log_message(self, *a):  # no access logs: we don't keep IPs
        pass

    def send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def admin_ok(self):
        return bool(ADMIN_TOKEN) and hmac.compare_digest(self.headers.get("X-Admin-Token", ""), ADMIN_TOKEN)

    def cors(self):
        if self.headers.get("Origin") == ADMIN_ORIGIN:
            self.send_header("Access-Control-Allow-Origin", ADMIN_ORIGIN)
            self.send_header("Access-Control-Allow-Headers", "X-Admin-Token")
            self.send_header("Access-Control-Expose-Headers", "Content-Disposition")
            self.send_header("Vary", "Origin")

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors()
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def send_csv(self, name, rows):
        buf = io.StringIO()
        csv.writer(buf).writerows(rows)
        body = ("\ufeff" + buf.getvalue()).encode()
        self.send_response(200)
        self.cors()
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{name}"')
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 8192:
            raise ValueError("too large")
        return json.loads(self.rfile.read(n) or b"{}")

    def ip(self):
        return (self.headers.get("X-Forwarded-For") or self.client_address[0]).split(",")[0].strip()

    def device(self, v):
        try:
            return str(uuid.UUID(str(v)))
        except ValueError:
            return ""

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            return self.send(200, {"ok": True})
        if u.path == "/v1/summary":
            if limited(self.ip(), 120):
                return self.send(429, {"error": "slow down"})
            return self.send(200, summary(parse_qs(u.query)))
        if u.path.startswith("/v1/admin/"):
            if limited(self.ip(), 30):
                return self.send(429, {"error": "slow down"})
            if not self.admin_ok():
                return self.send(403, {"error": "forbidden"})
            if u.path == "/v1/admin/overview":
                return self.send(200, overview())
            if u.path == "/v1/admin/export":
                q = parse_qs(u.query)
                kind = (q.get("kind") or ["entries"])[0]
                if kind not in EXPORT_KINDS:
                    return self.send(400, {"error": "kind must be one of " + ", ".join(EXPORT_KINDS)})
                start = (q.get("from") or ["2000-01-01"])[0]
                end = (q.get("to") or [date.today().isoformat()])[0]
                if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", start) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", end)):
                    return self.send(400, {"error": "from/to must be YYYY-MM-DD"})
                return self.send_csv(f"dream-{kind}-{start}_{end}.csv", export_rows(kind, start, end))
        self.send(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path)
        if limited(self.ip()):
            return self.send(429, {"error": "slow down"})
        try:
            b = self.body()
        except Exception:
            return self.send(400, {"error": "bad json"})
        if u.path == "/v1/dreams":
            dev = self.device(b.get("device"))
            day = str(b.get("day", ""))
            if not dev or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
                return self.send(400, {"error": "device and day required"})
            country = str(b.get("country", "")).upper()
            country = country if re.fullmatch(r"[A-Z]{2}", country) else ""
            age = b.get("age", "") if b.get("age", "") in AGES else ""
            gender = b.get("gender", "") if b.get("gender", "") in GENDERS else ""
            words = [w for w in (clean_word(x) for x in (b.get("words") or [])[:8]) if w][:6]
            feelings = [f for f in (b.get("feelings") or [])[:5] if f in FEELINGS][:3]
            with db() as c:
                c.execute("INSERT OR REPLACE INTO entries VALUES(?,?,?,?,?,?,?,?)",
                          (dev, day, country, age, gender, json.dumps(words, ensure_ascii=False), json.dumps(feelings), int(time.time())))
            return self.send(200, {"ok": True})
        if u.path == "/v1/forget":
            dev = self.device(b.get("device"))
            if not dev:
                return self.send(400, {"error": "device required"})
            with db() as c:
                n = c.execute("DELETE FROM entries WHERE device = ?", (dev,)).rowcount
            return self.send(200, {"ok": True, "deleted": n})
        if u.path == "/v1/events":
            if not ADMIN_TOKEN or self.headers.get("X-Admin-Token") != ADMIN_TOKEN:
                return self.send(403, {"error": "forbidden"})
            items = b.get("events") or []
            with db() as c:
                for e in items[:50]:
                    c.execute("INSERT OR REPLACE INTO events VALUES(?,?,?,?)",
                              (str(e["day"])[:10], "japan" if e.get("scope") == "japan" else "world",
                               str(e.get("title_ja", ""))[:120], str(e.get("title_en", ""))[:120]))
            return self.send(200, {"ok": True, "saved": len(items[:50])})
        self.send(404, {"error": "not found"})


if __name__ == "__main__":
    init()
    print(f"dream-server on 127.0.0.1:{PORT}, K={K}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
