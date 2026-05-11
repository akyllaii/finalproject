import json
from datetime import datetime

def log(request, status):
    entry = {
        "time": str(datetime.utcnow()),
        "method": request.method,
        "path": request.url.path,
        "status": status,
        "ip": request.client.host
    }

    with open("logs/app.log", "a") as f:
        f.write(json.dumps(entry) + "\n")