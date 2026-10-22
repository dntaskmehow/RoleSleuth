import json
from typing import List
from rich.console import Console
from rich.table import Table
from .engine import Finding

console = Console()

class Reporter:
    @staticmethod
    def print_terminal_report(findings: List[Finding]):
        if not findings:
            console.print("[green]✔ No authorization bypasses or anomalies detected.[/green]")
            return

        table = Table(title="[bold red]RoleSleuth Authorization Audit Findings[/bold red]")
        table.add_column("Method", style="cyan", no_wrap=True)
        table.add_column("URL", style="magenta")
        table.add_column("Baseline", style="green")
        table.add_column("Tested Role", style="yellow")
        table.add_column("Status", style="bold red")
        table.add_column("Vulnerability", style="bold white")

        for f in findings:
            table.add_row(
                f.method,
                f.url,
                f.baseline_role,
                f.tested_role,
                f"{f.baseline_status} -> {f.tested_status}",
                f.potential_vulnerability
            )

        console.print(table)

    @staticmethod
    def save_json_report(findings: List[Finding], filepath: str):
        data = [f.model_dump() for f in findings]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        console.print(f"[bold green]✔ JSON report saved to {filepath}[/bold green]")