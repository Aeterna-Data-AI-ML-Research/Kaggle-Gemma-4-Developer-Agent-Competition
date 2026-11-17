#!/usr/bin/env python3
"""Build docs/index.html (GitHub Pages one-pager) from PAPER.md."""
from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import markdown
except ImportError:
    print("pip install markdown", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    text = (ROOT / "PAPER.md").read_text()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].lstrip("\n")
    text = text.replace("](docs/figures/", "](figures/")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"],
        output_format="html5",
    )
    # reuse template from existing index if present style-wise — keep inline for one file
    page = (ROOT / "docs" / "index.html").read_text() if (ROOT / "docs" / "index.html").exists() else ""
    # Always rewrite full page for determinism
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>When Better Agent Behavior Does Not Improve Accuracy</title>
  <meta name="description" content="An evidence-first retrospective on building and evaluating a code-repair agent for the Gemma 4 Developer Agent Competition." />
  <link rel="canonical" href="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/" />
  <style>
    :root {{ --bg:#0f1115; --panel:#171a21; --text:#e8eaed; --muted:#9aa0a6; --accent:#7cb3ff; --border:#2a2f3a; --code:#1e2430; }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font:18px/1.65 "Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif; }}
    .wrap {{ max-width:820px; margin:0 auto; padding:2.5rem 1.25rem 4rem; }}
    h1,h2,h3,h4 {{ font-family:"Avenir Next","Segoe UI",system-ui,sans-serif; line-height:1.25; letter-spacing:-0.02em; }}
    h1 {{ font-size:2.1rem; margin:0 0 .4rem; }}
    h2 {{ font-size:1.45rem; margin-top:2.4rem; border-bottom:1px solid var(--border); padding-bottom:.35rem; }}
    h3 {{ font-size:1.15rem; margin-top:1.6rem; color:#d7dbe3; }}
    p {{ margin:.9rem 0; }}
    a {{ color:var(--accent); }}
    img {{ max-width:100%; height:auto; display:block; margin:1.25rem auto; border-radius:8px; border:1px solid var(--border); background:#000; }}
    em {{ color:var(--muted); }}
    table {{ width:100%; border-collapse:collapse; font-size:.92rem; font-family:"Avenir Next","Segoe UI",system-ui,sans-serif; margin:1.2rem 0; overflow-x:auto; display:block; }}
    th,td {{ border:1px solid var(--border); padding:.45rem .6rem; text-align:left; background:var(--panel); }}
    th {{ background:#1f2530; }}
    code,pre {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:.86rem; }}
    code {{ background:var(--code); padding:.1rem .35rem; border-radius:4px; }}
    pre {{ background:var(--code); padding:.9rem 1rem; border-radius:8px; overflow-x:auto; border:1px solid var(--border); }}
    pre code {{ background:none; padding:0; }}
    ul,ol {{ padding-left:1.3rem; }}
    li {{ margin:.25rem 0; }}
    hr {{ border:0; border-top:1px solid var(--border); margin:2rem 0; }}
    .topbar {{ font-family:"Avenir Next","Segoe UI",system-ui,sans-serif; font-size:.85rem; color:var(--muted); margin-bottom:1.5rem; }}
    .topbar a {{ text-decoration:none; }}
    @media (max-width:640px) {{ body {{ font-size:16px; }} h1 {{ font-size:1.7rem; }} }}
  </style>
</head>
<body>
  <main class="wrap">
    <div class="topbar">
      <a href="https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition">GitHub repository</a>
      · evidence-first Gemma 4 agent study · Apache-2.0
    </div>
    <article>
{body}
    </article>
  </main>
</body>
</html>
"""
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(html)
    (docs / ".nojekyll").write_text("")
    # also publish markdown copy for readers who want the source beside the page
    (docs / "article.md").write_text((ROOT / "PAPER.md").read_text())
    imgs = re.findall(r'src="([^"]+)"', html)
    missing = [i for i in imgs if not (docs / i).exists()]
    if missing:
        print("missing images:", missing, file=sys.stderr)
        return 1
    print(f"wrote docs/index.html ({(docs / 'index.html').stat().st_size} bytes) and docs/article.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
