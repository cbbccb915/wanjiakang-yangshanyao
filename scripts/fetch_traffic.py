import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "traffic.json"
TZ = ZoneInfo("Asia/Shanghai")
PAGES = {
    "home": "首页",
    "guide-family": "家庭药箱",
    "guide-storage": "药品储存",
    "guide-bp": "测血压",
    "guide-elderly": "老人用药清单",
    "guide-expired": "过期药",
    "guide-community": "附近药店怎么选",
}
DAYS = 14
BASE = "https://api.visitorbadge.io/api/visitors?path={path}&label=visits&countColor=%230b7a4b"
PATTERN = re.compile(r"VISITS:\s*([0-9]+)")

today = datetime.now(TZ).date()
today_s = today.isoformat()
days = [(today - timedelta(days=i)).isoformat() for i in range(DAYS - 1, -1, -1)]

old = {}
if OUT.exists():
    try:
        old = json.loads(OUT.read_text(encoding="utf-8"))
    except Exception:
        old = {}

counts = old.get("counts", {})
offsets = old.get("fetch_offsets", {})
for page in PAGES:
    counts.setdefault(page, {})
    for day in days:
        counts[page].setdefault(day, 0)
    for day in list(counts[page].keys()):
        if day not in days:
            del counts[page][day]


def fetch_count(path: str) -> int:
    url = BASE.format(path=urllib.parse.quote(path, safe=""))
    req = urllib.request.Request(url, headers={"User-Agent": "wanjiakang-traffic/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = resp.read().decode("utf-8", "ignore")
    match = PATTERN.search(text)
    return int(match.group(1)) if match else 0


errors = 0
# 只更新今天；历史日期保留已记录值，避免重复读取把计数器抬高
for page in PAGES:
    key = f"wjk2-{page}-{today_s.replace('-', '')}"
    try:
        raw = fetch_count(key)
        prev = int(offsets.get(key, 0))
        actual = max(0, raw - prev - 1)  # 减掉本次读取本身
        counts[page][today_s] = actual
        offsets[key] = prev + 1
    except Exception:
        counts[page][today_s] = counts[page].get(today_s, 0)
        errors += 1

payload = {
    "updated": datetime.now(TZ).isoformat(timespec="seconds"),
    "timezone": "Asia/Shanghai",
    "start_date": days[0],
    "days": days,
    "pages": PAGES,
    "counts": counts,
    "fetch_offsets": offsets,
    "errors": errors,
    "note": "页面加载计数，包含刷新；不是独立访客(UV)。每次读取会先扣掉读取本身造成的 +1。",
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT} errors={errors} today={today_s}")
