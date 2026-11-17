#!/usr/bin/env python3
"""Build docs/index.html (GitHub Pages one-pager) from PAPER.md + ascii.rest."""
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
    # Drop the first H1 — we replace it with an ascii-banner hero
    text = re.sub(r"^# .+\n+", "", text, count=1)
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"],
        output_format="html5",
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>When Better Agent Behavior Does Not Improve Accuracy — Moran Zavdi</title>
  <meta name="description" content="Evidence-first retrospective: Gemma 4 code-repair agent, 1,350 paired episodes. Better process behavior (Think-1024) did not raise working-tree accuracy (48/150 = 48/150)." />
  <meta name="author" content="Moran Zavdi" />
  <meta name="keywords" content="Gemma 4, software engineering agents, SWE, evaluation, virtual clock, Kaggle, code repair, LoRA, ForgeSWE, working-tree pass, Moran Zavdi" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="googlebot" content="index, follow" />
  <link rel="canonical" href="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/" />
  <link rel="alternate" type="text/markdown" href="article.md" title="Article Markdown" />
  <link rel="alternate" type="text/plain" href="llms.txt" title="llms.txt" />
  <link rel="author" href="humans.txt" />
  <link rel="license" href="https://www.apache.org/licenses/LICENSE-2.0" />
  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Aeterna Data AI/ML Research" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:url" content="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/" />
  <meta property="og:title" content="When Better Agent Behavior Does Not Improve Accuracy" />
  <meta property="og:description" content="1,350-episode calibration of a Gemma 4 autonomous code-repair agent. Shorter reasoning and earlier submits changed behavior, not WT accuracy." />
  <meta property="og:image" content="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/figures/hero_evidence_first_study.jpg" />
  <meta property="og:image:alt" content="Evidence-first study summary figure" />
  <meta property="article:author" content="Moran Zavdi" />
  <meta property="article:published_time" content="2026-11-17" />
  <meta property="article:section" content="Machine Learning" />
  <meta property="article:tag" content="Gemma 4" />
  <meta property="article:tag" content="software engineering agents" />
  <meta property="article:tag" content="evaluation" />
  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="When Better Agent Behavior Does Not Improve Accuracy" />
  <meta name="twitter:description" content="Evidence-first Gemma 4 agent study by Moran Zavdi. Think-1024 changed behavior, not accuracy." />
  <meta name="twitter:image" content="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/figures/hero_evidence_first_study.jpg" />
  <!-- AEO / GEO discovery -->
  <link rel="describedby" href="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/llms.txt" />
  <meta name="citation_title" content="When Better Agent Behavior Does Not Improve Accuracy" />
  <meta name="citation_author" content="Zavdi, Moran" />
  <meta name="citation_publication_date" content="2026-11-17" />
  <meta name="citation_online_date" content="2026-11-17" />
  <meta name="citation_fulltext_html_url" content="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/" />
  <meta name="citation_pdf_url" content="https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition/blob/main/PAPER.md" />
  <meta name="citation_license" content="https://www.apache.org/licenses/LICENSE-2.0" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "ScholarlyArticle",
        "@id": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/#article",
        "headline": "When Better Agent Behavior Does Not Improve Accuracy",
        "name": "When Better Agent Behavior Does Not Improve Accuracy",
        "description": "Evidence-first retrospective on a Gemma 4 autonomous code-repair agent under a 420s virtual clock. 1,350 paired episodes; Think-1024 changed behavior but not working-tree accuracy.",
        "datePublished": "2026-11-17",
        "dateModified": "2026-11-17",
        "inLanguage": "en",
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "author": {{
          "@type": "Person",
          "name": "Moran Zavdi",
          "url": "https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "Aeterna Data AI/ML Research",
          "url": "https://github.com/Aeterna-Data-AI-ML-Research"
        }},
        "image": [
          "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/figures/hero_evidence_first_study.jpg",
          "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/figures/hero_agent_workbench.jpg"
        ],
        "mainEntityOfPage": {{
          "@type": "WebPage",
          "@id": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/"
        }},
        "isBasedOn": "https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition",
        "keywords": [
          "Gemma 4",
          "software engineering agents",
          "evaluation",
          "virtual clock",
          "SWE",
          "code repair"
        ],
        "about": [
          {{"@type": "Thing", "name": "Autonomous software engineering agents"}},
          {{
            "@type": "Thing",
            "name": "Google — The Gemma 4 Developer Agent Competition",
            "url": "https://www.kaggle.com/competitions/gemma-4-developer-agent",
            "sameAs": "https://www.kaggle.com/competitions/gemma-4-developer-agent"
          }}
        ],
        "isPartOf": {{
          "@type": "WebPage",
          "name": "Google — The Gemma 4 Developer Agent Competition",
          "url": "https://www.kaggle.com/competitions/gemma-4-developer-agent"
        }}
      }},
      {{
        "@type": "WebSite",
        "@id": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/#website",
        "url": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/",
        "name": "When Better Agent Behavior Does Not Improve Accuracy",
        "publisher": {{"@id": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/#org"}},
        "inLanguage": "en"
      }},
      {{
        "@type": "Organization",
        "@id": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/#org",
        "name": "Aeterna Data AI/ML Research",
        "url": "https://github.com/Aeterna-Data-AI-ML-Research"
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Aeterna Data AI/ML Research",
            "item": "https://github.com/Aeterna-Data-AI-ML-Research"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "When Better Agent Behavior Does Not Improve Accuracy",
            "item": "https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/"
          }}
        ]
      }}
    ]
  }}
  </script>
  <script type="module" src="https://ascii.rest/ascii.js"></script>
  <style>
    :root {{
      --bg: #0b0d10;
      --panel: #141820;
      --text: #e8eaed;
      --muted: #9aa0a6;
      --accent: #7cb3ff;
      --border: #2a3140;
      --code: #1a2030;
      --glow: #f97316;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background:
        radial-gradient(1200px 600px at 10% -10%, #1a2235 0%, transparent 55%),
        radial-gradient(900px 500px at 90% 0%, #2a1810 0%, transparent 50%),
        var(--bg);
      color: var(--text);
      font: 18px/1.65 "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
    }}
    .wrap {{
      max-width: 860px;
      margin: 0 auto;
      padding: 1.5rem 1.25rem 4rem;
    }}
    .topbar {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "ascii.rest mono", monospace;
      font-size: 0.78rem;
      color: var(--muted);
      margin-bottom: 1rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1.25rem;
      align-items: center;
    }}
    .topbar a {{ color: var(--accent); text-decoration: none; }}
    .topbar a:hover {{ text-decoration: underline; }}
    .hero {{
      border: 1px solid var(--border);
      border-radius: 12px;
      background: linear-gradient(180deg, #12161f 0%, #0d1016 100%);
      padding: 1rem 1rem 1.25rem;
      margin-bottom: 1.5rem;
      overflow: hidden;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 1rem;
      align-items: center;
    }}
    @media (max-width: 720px) {{
      .hero-grid {{ grid-template-columns: 1fr; }}
    }}
    .art, ascii-art, ascii-banner, .hero canvas, .hero pre {{
      margin: 0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", "ascii.rest mono", monospace;
      font-size: 11px;
      line-height: 1.2;
      letter-spacing: 0;
      white-space: pre;
      font-variant-ligatures: none;
    }}
    .hero ascii-banner, .hero .banner-wrap {{
      display: block;
      overflow-x: auto;
      max-width: 100%;
    }}
    .hero-scene {{
      width: 100%;
      max-width: 340px;
      margin-left: auto;
      margin-right: auto;
    }}
    .hero-scene ascii-art, .hero-scene canvas {{
      width: 100% !important;
      max-width: 340px;
    }}
    .strip {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.75rem;
      margin: 1.25rem 0 1.75rem;
    }}
    @media (max-width: 720px) {{
      .strip {{ grid-template-columns: 1fr; }}
    }}
    .strip-card {{
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--panel);
      padding: 0.75rem;
      min-height: 120px;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}
    .strip-card .label {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.7rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .strip-card .art-slot {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    h1, h2, h3, h4 {{
      font-family: "Avenir Next", "Segoe UI", system-ui, sans-serif;
      line-height: 1.25;
      letter-spacing: -0.02em;
    }}
    h1 {{ font-size: 2.0rem; margin: 0.6rem 0 0.35rem; }}
    h2 {{
      font-size: 1.4rem;
      margin-top: 2.4rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.35rem;
    }}
    h3 {{ font-size: 1.12rem; margin-top: 1.6rem; color: #d7dbe3; }}
    p {{ margin: 0.9rem 0; }}
    a {{ color: var(--accent); }}
    img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 1.25rem auto;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #000;
    }}
    em {{ color: var(--muted); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      font-family: "Avenir Next", "Segoe UI", system-ui, sans-serif;
      margin: 1.2rem 0;
      overflow-x: auto;
      display: block;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.45rem 0.6rem;
      text-align: left;
      background: var(--panel);
    }}
    th {{ background: #1c2330; }}
    code, pre {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.86rem;
    }}
    code {{ background: var(--code); padding: 0.1rem 0.35rem; border-radius: 4px; }}
    pre {{
      background: var(--code);
      padding: 0.9rem 1rem;
      border-radius: 8px;
      overflow-x: auto;
      border: 1px solid var(--border);
    }}
    pre code {{ background: none; padding: 0; }}
    ul, ol {{ padding-left: 1.3rem; }}
    li {{ margin: 0.25rem 0; }}
    hr {{ border: 0; border-top: 1px solid var(--border); margin: 2rem 0; }}
    .credit {{
      margin-top: 3rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.75rem;
      color: var(--muted);
    }}
    @media (max-width: 640px) {{
      body {{ font-size: 16px; }}
      h1 {{ font-size: 1.55rem; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <div class="topbar">
      <a href="https://www.kaggle.com/competitions/gemma-4-developer-agent">Kaggle</a>
      <a href="https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy">Dataset</a>
      <a href="https://www.kaggle.com/code/moranzavdi/reproduce-gemma4-agent-behavior-study">Notebook</a>
      <a href="https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition">GitHub</a>
      <a href="https://aeterna-data-ai-ml-research.github.io/Kaggle-Gemma-4-Developer-Agent-Competition/">Pages</a>
      <a href="article.md">Markdown</a>
      <a href="llms.txt">llms.txt</a>
      <a href="sitemap.xml">Sitemap</a>
      <span>Author: Moran Zavdi</span>
      <span>Apache-2.0 · evidence-first Gemma 4 agent study</span>
    </div>

    <section class="hero" aria-label="ascii.rest hero">
      <div class="hero-grid">
        <div>
          <div class="banner-wrap">
            <ascii-banner text="BETTER BEHAVIOR" color="#f97316,#f778ba,#7cb3ff" shadow="rounded"></ascii-banner>
          </div>
          <div class="banner-wrap" style="margin-top:0.35rem">
            <ascii-banner text="≠ ACCURACY" color="#7cb3ff,#f97316" shadow="rounded"></ascii-banner>
          </div>
          <p style="font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.78rem;color:var(--muted);margin:0.75rem 0 0">
            animated hero via <a href="https://ascii.rest/">ascii.rest</a> · 1,350 paired episodes · virtual clock 420s
          </p>
        </div>
        <div class="hero-scene">
          <ascii-art piece="night-coast" label="night coast ascii scene"></ascii-art>
        </div>
      </div>
    </section>

    <section class="strip" aria-label="ascii.rest accents">
      <div class="strip-card">
        <div class="label">matrix rain</div>
        <div class="art-slot"><ascii-art piece="matrix-rain" mono label="matrix rain"></ascii-art></div>
      </div>
      <div class="strip-card">
        <div class="label">file tree</div>
        <div class="art-slot"><ascii-art piece="file-tree" mono label="file tree"></ascii-art></div>
      </div>
      <div class="strip-card">
        <div class="label">python</div>
        <div class="art-slot"><ascii-art piece="python" label="python logo"></ascii-art></div>
      </div>
    </section>

    <article>
{body}
    </article>

    <p class="credit">
      Written by <strong>Moran Zavdi</strong>.
      Decorative animations by <a href="https://ascii.rest/">ascii.rest</a> (MIT).
      SEO / AEO / GEO: <a href="robots.txt">robots.txt</a> ·
      <a href="sitemap.xml">sitemap.xml</a> ·
      <a href="llms.txt">llms.txt</a> ·
      <a href="ai.txt">ai.txt</a> ·
      <a href="humans.txt">humans.txt</a>.
      Rebuild with <code>python scripts/build_pages.py</code>.
    </p>
  </main>
</body>
</html>
"""
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(html)
    (docs / ".nojekyll").write_text("")
    (docs / "article.md").write_text((ROOT / "PAPER.md").read_text())
    imgs = re.findall(r'src="([^"]+)"', html)
    missing = [i for i in imgs if not i.startswith("http") and not (docs / i).exists()]
    if missing:
        print("missing images:", missing, file=sys.stderr)
        return 1
    print(f"wrote docs/index.html ({(docs / 'index.html').stat().st_size} bytes) with ascii.rest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
