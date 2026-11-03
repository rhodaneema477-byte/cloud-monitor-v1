import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

with open("targets.json", "r") as f:
    targets = json.load(f)["targets"]

results = []

for target in targets:
    url = target["url"]
    result = {
        "name": target["name"],
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "DOWN",
        "response_code": None
    }

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "CloudMonitor/4.0"}
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            result["response_code"] = response.status
            result["status"] = (
                "UP" if 200 <= response.status < 400 else "DOWN"
            )
    except Exception as error:
        result["error"] = str(error)[:200]

    results.append(result)

Path("status.json").write_text(
    json.dumps({
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "results": results
    }, indent=2)
)

print(json.dumps(results, indent=2))
