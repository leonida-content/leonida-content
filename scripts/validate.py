"""Checks content.json before it goes live. Run: python3 scripts/validate.py [content.json] [--base old.json]"""
import json, sys

PS = {"CROSS", "CIRCLE", "SQUARE", "TRIANGLE", "X", "L1", "L2", "R1", "R2", "L3", "R3", "OPTIONS", "TOUCHPAD"}
XBOX = {"A", "B", "X", "Y", "LB", "LT", "RB", "RT", "LS", "RS", "MENU", "VIEW"}
DIRS = {"UP", "DOWN", "LEFT", "RIGHT"}
errors = []

def err(msg): errors.append(msg)

def need(obj, keys, where):
    for k in keys:
        if not isinstance(obj.get(k), str) or not obj[k].strip():
            err(f"{where}: missing or empty \"{k}\"")

args = sys.argv[1:]
path = next((a for a in args if not a.startswith("--") and (args.index(a) == 0 or args[args.index(a)-1] != "--base")), "content.json")
base = args[args.index("--base") + 1] if "--base" in args else None

try:
    data = json.load(open(path, encoding="utf-8"))
except json.JSONDecodeError as e:
    sys.exit(f"❌ {path} is not valid JSON: line {e.lineno}, column {e.colno}: {e.msg}")

if not isinstance(data.get("version"), int):
    err("top level: \"version\" must be a whole number")

seen = {}
def unique(kind, item_id, where):
    key = (kind, item_id)
    if key in seen:
        err(f"{where}: duplicate id \"{item_id}\" (also used at {seen[key]})")
    seen[key] = where

for i, n in enumerate(data.get("news", [])):
    w = f"news[{i}]"
    need(n, ["id", "title", "summary", "date"], w)
    if n.get("status") not in ("official", "rumor", "community"):
        err(f"{w}: status must be official, rumor or community")
    unique("news", n.get("id"), w)

for i, g in enumerate(data.get("guides", [])):
    w = f"guides[{i}] \"{g.get('title', '?')}\""
    need(g, ["id", "title", "body"], w)
    if g.get("section", "general") not in ("story", "online", "general"):
        err(f"{w}: section must be story, online or general")
    unique("guide", g.get("id"), w)

for i, m in enumerate(data.get("missions", [])):
    w = f"missions[{i}] \"{m.get('title', '?')}\""
    need(m, ["id", "title", "chapter"], w)
    if m.get("mode") not in ("story", "online"):
        err(f"{w}: mode must be story or online")
    if not isinstance(m.get("order"), int):
        err(f"{w}: order must be a whole number")
    if not isinstance(m.get("steps", []), list):
        err(f"{w}: steps must be a list")
    unique("mission", m.get("id"), w)

for i, c in enumerate(data.get("cheats", [])):
    w = f"cheats[{i}] \"{c.get('name', '?')}\""
    need(c, ["id", "name", "effect", "category"], w)
    for platform, allowed in (("playstation", PS | DIRS), ("xbox", XBOX | DIRS)):
        for b in c.get(platform, []):
            if str(b).upper() not in allowed:
                err(f"{w}: \"{b}\" isn't a valid {platform} button")
    if not c.get("playstation") and not c.get("xbox") and not c.get("phone"):
        err(f"{w}: needs button combos or a phone number")
    unique("cheat", c.get("id"), w)

for i, cl in enumerate(data.get("checklists", [])):
    w = f"checklists[{i}] \"{cl.get('title', '?')}\""
    need(cl, ["id", "title", "icon"], w)
    unique("checklist", cl.get("id"), w)
    for j, it in enumerate(cl.get("items", [])):
        need(it, ["id", "title"], f"{w} item {j}")
        unique("item", it.get("id"), f"{w} item {j}")

if base:
    try:
        old = json.load(open(base, encoding="utf-8"))
        if isinstance(data.get("version"), int) and data["version"] <= old.get("version", 0):
            err(f"version must go up: live is {old.get('version')}, this change has {data['version']}. Players won't get the update otherwise.")
        old_ids = {(m["id"]) for m in old.get("missions", [])} | {it["id"] for cl in old.get("checklists", []) for it in cl.get("items", [])}
        new_ids = {(m["id"]) for m in data.get("missions", [])} | {it["id"] for cl in data.get("checklists", []) for it in cl.get("items", [])}
        removed = old_ids - new_ids
        if removed:
            print(f"⚠️  Note: these ids were removed or renamed, so players lose progress on them: {sorted(removed)}")
    except (OSError, json.JSONDecodeError):
        pass

if errors:
    print(f"❌ {len(errors)} problem(s) in {path}:")
    for e in errors:
        print("  - " + e)
    sys.exit(1)

counts = {k: len(data.get(k, [])) for k in ("missions", "cheats", "guides", "checklists", "news")}
print(f"✅ {path} looks good (version {data['version']}): " + ", ".join(f"{v} {k}" for k, v in counts.items()))
