import time
import requests
from typing import List, Dict, Any
from .config import AuditConfig, TargetRequest, Role

class Finding(BaseModel):
    url: str
    method: str
    baseline_role: str
    tested_role: str
    baseline_status: int
    tested_status: int
    baseline_len: int
    tested_len: int
    potential_vulnerability: str
    evidence: str

class AuditEngine:
    def __init__(self, config: AuditConfig, requests_list: List[TargetRequest]):
        self.config = config
        self.requests_list = requests_list

    def _structural_similarity(self, text1: str, text2: str) -> float:
        # Simple token/key set Jaccard similarity for JSON responses
        try:
            d1 = set(requests.utils.default_headers() if not text1 else text1[:100])
            d2 = set(requests.utils.default_headers() if not text2 else text2[:100])
            intersection = len(d1.intersection(d2))
            union = len(d1.union(d2))
            return intersection / union if union > 0 else 1.0
        except Exception:
            return 1.0

    def run(self) -> List[Finding]:
        findings: List[Finding] = []
        session = requests.Session()

        for req in self.requests_list:
            # Check exclusions
            if any(exc in req.url for exc in self.config.exclude_paths):
                continue

            # Establish baseline using first role or original request headers
            baseline_role = self.config.roles[0]
            base_headers = {**req.headers, **baseline_role.headers}
            
            try:
                base_resp = session.request(
                    method=req.method,
                    url=req.url,
                    headers=base_headers,
                    data=req.body,
                    cookies=baseline_role.cookies,
                    timeout=self.config.timeout,
                    allow_redirects=False
                )
            except Exception:
                continue

            # Replay across all other roles
            for test_role in self.config.roles[1:]:
                test_headers = {**req.headers, **test_role.headers}
                try:
                    test_resp = session.request(
                        method=req.method,
                        url=req.url,
                        headers=test_headers,
                        data=req.body,
                        cookies=test_role.cookies,
                        timeout=self.config.timeout,
                        allow_redirects=False
                    )
                except Exception:
                    continue

                # Analysis logic for BOLA / IDOR / Privilege Escalation
                vuln_type = None
                evidence = ""

                # If unauthorized role gets 200 OK while baseline got 200 OK and responses match structurally
                if base_resp.status_code == 200 and test_resp.status_code == 200:
                    similarity = self._structural_similarity(base_resp.text, test_resp.text)
                    if similarity >= self.config.similarity_threshold:
                        vuln_type = "Potential BOLA / IDOR (Unauthorized Access)"
                        evidence = f"Role '{test_role.name}' received HTTP 200 OK matching baseline '{baseline_role.name}' response structure."

                elif base_resp.status_code in [200, 201] and test_resp.status_code in [401, 403]:
                    # Properly secured
                    pass
                elif base_resp.status_code in [200, 201] and test_resp.status_code == 500:
                    vuln_type = "Potential Server Error on Role Switch (Logic Flaw)"
                    evidence = f"Role '{test_role.name}' triggered HTTP 500."

                if vuln_type:
                    findings.append(Finding(
                        url=req.url,
                        method=req.method,
                        baseline_role=baseline_role.name,
                        tested_role=test_role.name,
                        baseline_status=base_resp.status_code,
                        tested_status=test_resp.status_code,
                        baseline_len=len(base_resp.content),
                        tested_len=len(test_resp.content),
                        potential_vulnerability=vuln_type,
                        evidence=evidence
                    ))

                time.sleep(0.05) # Polite pacing

        return findings