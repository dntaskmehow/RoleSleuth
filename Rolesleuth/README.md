# RoleSleuth 🕵️‍♂️🛡️

**Multi-Role Authorization Matrix & IDOR Verification Engine**

RoleSleuth is a high-speed CLI tool designed for bug bounty hunters and penetration testers to automatically audit multi-role authorization matrices and detect Broken Object Level Authorization (BOLA) and IDOR vulnerabilities from recorded HTTP traffic (HAR).

## Features
- **HAR Ingestion:** Automatically parses recorded traffic exports from Burp Suite, OWASP ZAP, or browser devtools.
- **Multi-Role Replaying:** Replays requests across Admin, User, and Guest session contexts concurrently.
- **Differential Structural Analysis:** Compares response status codes and structural keys while discounting dynamic timestamps.
- **Rich Terminal Output & JSON Reports:** Clean tabular CLI output with full JSON artifact logging for HackerOne reports.

## Installation
```bash
git clone [https://github.com/professor-bug/rolesleuth.git](https://github.com/professor-bug/rolesleuth.git)
cd rolesleuth
pip install -e .

# 1. Clone or navigate to project directory
cd rolesleuth

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install in editable mode with dependencies
pip install --upgrade pip
pip install -e .

# 4. Run unit tests
python3 -m unittest discover tests

Bash
rolesleuth --har traffic.har \
           --admin-cookie "session_admin=abc123xyz" \
           --user-cookie "session_user=def456uvw" \
           --domain "api.target.com" \
           --output findings.json
F. GITHUB RELEASE & LAUNCH PACKAGES
1. README.md
Markdown
# RoleSleuth 🕵️‍♂️🛡️

**Multi-Role Authorization Matrix & IDOR Verification Engine**

RoleSleuth is a high-speed CLI tool designed for bug bounty hunters and penetration testers to automatically audit multi-role authorization matrices and detect Broken Object Level Authorization (BOLA) and IDOR vulnerabilities from recorded HTTP traffic (HAR).

## Features
- **HAR Ingestion:** Automatically parses recorded traffic exports from Burp Suite, OWASP ZAP, or browser devtools.
- **Multi-Role Replaying:** Replays requests across Admin, User, and Guest session contexts concurrently.
- **Differential Structural Analysis:** Compares response status codes and structural keys while discounting dynamic timestamps.
- **Rich Terminal Output & JSON Reports:** Clean tabular CLI output with full JSON artifact logging for HackerOne reports.

## Installation
```bash
git clone [https://github.com/professor-bug/rolesleuth.git](https://github.com/professor-bug/rolesleuth.git)
cd rolesleuth
pip install -e .
Usage
Bash
rolesleuth --har export.har --admin-cookie "admin_token" --user-cookie "user_token" --domain "target.com"

### 2. `SECURITY.md`
```markdown
# Security Policy

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability
If you discover a security vulnerability within RoleSleuth, please report it via private GitHub advisory or direct contact. Do not open public issues for security vulnerabilities.
3. CONTRIBUTING.md
Markdown
# Contributing to RoleSleuth

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git origin push feature/amazing-feature`).
5. Open a Pull Request. Ensure all `pytest` suites pass successfully.
4. CHANGELOG.md
Markdown
# Changelog

## [1.0.0] - 2026-10-22
- Initial public release of RoleSleuth.
- HAR parsing support for Burp Suite & ZAP traffic exports.
- Multi-role session differential engine.
- Rich CLI tables and JSON report generation.