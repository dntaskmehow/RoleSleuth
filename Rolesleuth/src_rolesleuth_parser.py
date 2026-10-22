import json
from pathlib import Path
from typing import List
from .config import TargetRequest

class HARParser:
    @staticmethod
    def parse_file(file_path: str, target_domain: str = None) -> List[TargetRequest]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"HAR file not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        requests_list = []
        entries = data.get("log", {}).get("entries", [])
        
        for entry in entries:
            req = entry.get("request", {})
            url = req.get("url", "")
            
            if target_domain and target_domain not in url:
                continue

            method = req.get("method", "GET")
            
            headers = {h["name"]: h["value"] for h in req.get("headers", []) if not h["name"].startswith(":")}
            
            body = None
            post_data = req.get("postData")
            if post_data:
                body = post_data.get("text")

            requests_list.append(TargetRequest(
                method=method,
                url=url,
                headers=headers,
                body=body
            ))

        return requests_list