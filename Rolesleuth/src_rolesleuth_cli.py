import argparse
import sys
from pathlib import Path
from .config import AuditConfig, Role
from .parser import HARParser
from .engine import AuditEngine
from .reporter import Reporter

def main():
    parser = argparse.ArgumentParser(description="RoleSleuth: Multi-role authorization audit & IDOR detection engine.")
    parser.add_argument("--har", required=True, help="Path to HTTP Archive (HAR) file.")
    parser.add_argument("--admin-cookie", required=True, help="Session cookie or token for Admin role.")
    parser.add_argument("--user-cookie", required=True, help="Session cookie or token for standard User role.")
    parser.add_argument("--guest-cookie", default="", help="Session cookie or token for Guest/Unauth role.")
    parser.add_argument("--domain", default="", help="Target domain filter.")
    parser.add_argument("--output", default="rolesleuth_report.json", help="Output JSON report path.")

    args = parser.parse_args()

    try:
        requests_list = HARParser.parse_file(args.har, target_domain=args.domain)
        print(f"[*] Loaded {len(requests_list)} requests from HAR.")

        roles = [
            Role(name="Admin", cookies={"session": args.admin_cookie}),
            Role(name="User", cookies={"session": args.user_cookie}),
        ]
        if args.guest_cookie:
            roles.append(Role(name="Guest", cookies={"session": args.guest_cookie}))

        config = AuditConfig(
            target_base_url=args.domain,
            roles=roles
        )

        engine = AuditEngine(config, requests_list)
        print("[*] Executing multi-role authorization audit matrix...")
        findings = engine.run()

        Reporter.print_terminal_report(findings)
        Reporter.save_json_report(findings, args.output)

    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()