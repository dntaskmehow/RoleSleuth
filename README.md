<div align="center">
  <h1>RoleSleuth</h1>
      <img src="https://readme-typing-svg.demolab.com?font=Orbitron&size=28&pause=1000&color=FF3131&center=true&vCenter=true&width=900&lines=Researcher+:+dontaskmehow;High+Speed+CLI;Consumes+Recorded+HTTP+Traffic+From+Burp+Suite;For+BOLA+Or+IDOR+Vulnerabilities" alt="MARABUSE banner" />
  <p>
    <strong>Multi-role authorization auditing for bug bounty hunters and pentesters.</strong>
  </p>
  <p>
    Replay HAR traffic across different session contexts, compare responses, and surface potential Broken Object Level Authorization (BOLA) and IDOR issues before they become public findings.
  </p>
  <p>
    <a href="#quick-start">Quick start</a> ·
    <a href="#how-it-works">How it works</a> ·
    <a href="#usage">Usage</a>
  </p>
</div>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CLI](https://img.shields.io/badge/Interface-CLI-0E7490)](https://github.com/dntaskmehow/RoleSleuth)
[![HAR](https://img.shields.io/badge/Input-HAR-111827)](https://en.wikipedia.org/wiki/HAR_(file_format))

RoleSleuth is a high-speed CLI tool built for security research and web app testing. It consumes recorded HTTP traffic from Burp Suite, OWASP ZAP, or browser developer tools, replays the same request set under different role contexts, and looks for authorization mismatches that suggest BOLA or IDOR vulnerabilities.

## Why it exists

Authorization bugs are often discovered in the gap between what an application allows for one role and what it allows for another. In real-world testing, the challenge is not just finding the vulnerable endpoint — it is comparing the same behavior across Admin, User, and Guest contexts without missing the patterns that indicate privilege escalation or object-level access control mistakes.

RoleSleuth helps security researchers automate that comparison. By replaying requests from a HAR export, it compares responses across roles, filters out noisy differences, and highlights suspicious cases that deserve manual validation.

## At a glance

| Capability | What it does |
| --- | --- |
| HAR ingestion | Parses recorded request traffic from exported HAR files. |
| Multi-role replay | Replays requests under different session/cookie contexts. |
| Differential analysis | Compares response status codes and structure to find suspicious matches. |
| Reporting | Produces terminal output and JSON artifacts for follow-up investigation. |

## Key capabilities

- Parses HTTP Archive exports from Burp Suite, OWASP ZAP, and browser devtools.
- Replays requests across multiple role contexts such as Admin, User, and Guest.
- Uses per-role cookies or tokens to simulate authorization boundaries.
- Compares responses for structural similarity and status-code anomalies.
- Flags likely access-control issues such as BOLA / IDOR and role-switch logic flaws.
- Outputs results in a machine-readable JSON report and a concise CLI summary.

## How it works

```text
HAR export
   ↓
Request parser
   ↓
Role-aware replay matrix
   ↓
Response comparison and anomaly checks
   ↓
Findings report
```

1. Import a HAR file containing recorded application traffic.
2. Filter the target domain if needed.
3. Provide the session material for the baseline and comparison roles.
4. Replay each request under those contexts.
5. Compare outcomes and identify patterns where an unauthorized role receives the same or structurally similar response as an authorized one.

## Installation

From a local checkout of the repository:

```bash
git clone https://github.com/dntaskmehow/RoleSleuth.git
cd RoleSleuth
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

If your environment already has the project dependencies available, the core workflow is still the same: prepare a HAR file, define the role cookies, and run the CLI against the target domain.

## Quick start

```bash
rolesleuth \
  --har traffic.har \
  --admin-cookie "session_admin=abc123xyz" \
  --user-cookie "session_user=def456uvw" \
  --domain "api.target.com" \
  --output findings.json
```

This loads the HAR file, replays the requests under the configured role contexts, and writes a JSON report to `findings.json`.

## Usage

```bash
rolesleuth --help
```

### Supported arguments

- `--har`: Path to the HAR file to analyze.
- `--admin-cookie`: Session cookie or token for the Admin role.
- `--user-cookie`: Session cookie or token for the standard User role.
- `--guest-cookie`: Optional session cookie or token for a Guest/Unauthenticated role.
- `--domain`: Optional target domain filter to narrow the replay set.
- `--output`: Output path for the JSON findings report.

## What RoleSleuth looks for

The current engine is designed to highlight suspicious authorization behavior such as:

- unexpected access for a lower-privilege role when the baseline role succeeds;
- structurally similar responses between roles with different session contexts;
- server-side logic flaws that manifest as HTTP 500 responses during role switching;
- object-level access checks that do not enforce proper role separation.

This is a triage and validation tool for security research. It does not replace manual verification or a full application security review.

## Example output

```text
[*] Loaded 128 requests from HAR.
[*] Executing multi-role authorization audit matrix...
URL: https://api.target.com/v1/users/42
Method: GET
Baseline role: Admin
Tested role: User
Status: 200 -> 200
Potential vulnerability: Potential BOLA / IDOR (Unauthorized Access)
Evidence: Role 'User' received HTTP 200 OK matching baseline 'Admin' response structure.
```

## Security and responsible use

Use RoleSleuth only against systems you own, are authorized to test, or have explicit permission to assess. The tool is intended for security research, authorized penetration testing, and controlled vulnerability validation.

## Contributing

Contributions are welcome. If you want to improve parsing behavior, expand role analysis, or tighten the reporting workflow, fork the repository, create a feature branch, and open a pull request with a clear explanation of the change.

## Project status

RoleSleuth is a focused authorization-audit utility for CLI-based security testing. It is designed to help researchers prioritize likely privilege-escalation and object-level access control issues in HAR-driven workflows.

## Repository layout

```text
RoleSleuth/
├── README.md
├── Rolesleuth/
│   ├── src_rolesleuth_cli.py
│   ├── src_rolesleuth_config.py
│   ├── src_rolesleuth_engine.py
│   ├── src_rolesleuth_parser.py
│   ├── src_rolesleuth_reporter.py
│   ├── src_rolesleuth__init__.py
│   ├── tests_test_engine.py
│   └── tests_test_parser.py
└── docs/
    └── assets/
        └── role-sleuth-mark.svg
```

---

<div align="center">
  <p><em>Built for authorized security testing and thoughtful, evidence-based review.</em></p>
</div>
