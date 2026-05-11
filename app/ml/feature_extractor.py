import json

def extract_features(log_file_path):
    ip_stats = {}

    with open(log_file_path, "r") as f:
        for line in f:
            log = json.loads(line)

            ip = log["ip"]

            if ip not in ip_stats:
                ip_stats[ip] = {
                    "repeated_401": 0,
                    "total_requests": 0,
                    "unknown_paths": 0
                }

            ip_stats[ip]["total_requests"] += 1

            if log["status"] == 401:
                ip_stats[ip]["repeated_401"] += 1

            if log["status"] == 404:
                ip_stats[ip]["unknown_paths"] += 1

    return ip_stats