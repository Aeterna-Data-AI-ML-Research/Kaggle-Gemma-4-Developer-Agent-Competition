#!/usr/bin/env python3
"""Redact local paths / obvious secrets and fail on residual hits."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXT = {".md", ".txt", ".yml", ".yaml", ".json", ".jsonl", ".py", ".toml", ".cff", ".cfg", ".ini"}

PATH_RE = re.compile(r"/Users/[A-Za-z0-9._-]+|/Volumes/[A-Za-z0-9._-]+")
SECRET_RE = re.compile(
    r"(ssh_host|ssh_port|RUNPOD_API|BEGIN (RSA |OPENSSH )?PRIVATE|AKIA[0-9A-Z]{16}|"
    r"api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"])",
    re.I,
)


def main() -> int:
    changed = 0
    hits = []
    skip_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", "figures"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix in {".png", ".jpg", ".zip", ".whl"}:
            continue
        if path.suffix and path.suffix not in TEXT_EXT and path.name not in {"LICENSE", "NOTICE", "manifest.sha256"}:
            if path.suffix not in {".sha256"} and path.name != "LICENSE":
                continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        new = PATH_RE.sub("<REPO_ROOT>", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
            text = new
        # Skip this scanner's own regex source lines.
        if path.name != "redact_and_scan.py":
            for m in SECRET_RE.finditer(text):
                hits.append(f"{path.relative_to(ROOT)}: {m.group(0)[:40]}")
            if PATH_RE.search(text):
                hits.append(f"{path.relative_to(ROOT)}: residual path")
    print(f"redacted_files={changed}")
    if hits:
        print("SCAN_FAIL")
        for h in hits[:50]:
            print(" ", h)
        return 1
    print("REDACTION_SCAN_PASS = True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
