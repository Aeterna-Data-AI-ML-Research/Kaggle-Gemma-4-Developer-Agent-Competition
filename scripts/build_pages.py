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
    # Banner owns the original PAPER headline + subtitle; strip duplicates from body.
    body = re.sub(
        r"<h1[^>]*>When Better Agent Behavior Does Not Improve Accuracy</h1>\s*",
        "",
        body,
        count=1,
    )
    body = re.sub(
        r"<h2[^>]*>An evidence-first retrospective on building and evaluating a code-repair agent for the Gemma 4 Developer Agent Competition</h2>\s*",
        "",
        body,
        count=1,
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
  <style>
    :root {{
      --bg: #f7f6f3;
      --panel: #ffffff;
      --text: #1a1d23;
      --muted: #5c6570;
      --accent: #1d4ed8;
      --border: #e2e5ea;
      --code: #f0f2f5;
      --hero: #0f172a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 18px/1.7 "Source Serif 4", "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    }}
    .wrap {{
      max-width: 820px;
      margin: 0 auto;
      padding: 1.25rem 1.25rem 4rem;
    }}
    .topbar {{
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 1.5rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem 1.1rem;
      align-items: center;
      padding-bottom: 0.85rem;
      border-bottom: 1px solid var(--border);
    }}
    .topbar a {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 500;
    }}
    .topbar a:hover {{ text-decoration: underline; }}
    .hero {{
      margin: 0 0 2rem;
      padding: 1.75rem 0 0.25rem;
    }}
    .hero h1 {{
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      font-size: clamp(1.85rem, 4vw, 2.45rem);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin: 0 0 0.85rem;
      color: var(--hero);
      font-weight: 650;
    }}
    .hero .lede {{
      margin: 0;
      max-width: 40rem;
      color: var(--muted);
      font-size: 1.08rem;
      line-height: 1.5;
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
    }}
    .hero .meta {{
      margin: 1.1rem 0 0;
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      font-size: 0.88rem;
      color: var(--muted);
    }}
    h1, h2, h3, h4 {{
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      line-height: 1.25;
      letter-spacing: -0.02em;
      color: var(--hero);
    }}
    h2 {{
      font-size: 1.35rem;
      margin-top: 2.4rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.4rem;
    }}
    h3 {{ font-size: 1.1rem; margin-top: 1.6rem; }}
    p {{ margin: 0.9rem 0; }}
    a {{ color: var(--accent); }}
    img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 1.25rem auto;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #fff;
    }}
    em {{ color: var(--muted); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      margin: 1.2rem 0;
      overflow-x: auto;
      display: block;
      background: var(--panel);
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.5rem 0.65rem;
      text-align: left;
    }}
    th {{ background: #eef1f5; font-weight: 600; }}
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
    .resources {{
      margin-top: 2.5rem;
      padding: 1.25rem 1.25rem 0.5rem;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
    }}
    .resources h2 {{
      margin-top: 0;
      border-bottom: none;
      font-size: 1.15rem;
    }}
    .resources ul {{
      padding-left: 1.2rem;
      margin: 0.5rem 0 1rem;
    }}
    .resources li {{
      margin: 0.45rem 0;
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      font-size: 0.95rem;
    }}
    .credit {{
      margin-top: 2rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", system-ui, sans-serif;
      font-size: 0.78rem;
      color: var(--muted);
    }}
    @media (max-width: 640px) {{
      body {{ font-size: 16px; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <nav class="topbar" aria-label="Site">
      <a href="https://www.kaggle.com/competitions/gemma-4-developer-agent">Kaggle</a>
      <a href="https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy">Dataset</a>
      <a href="https://www.kaggle.com/code/moranzavdi/reproduce-gemma4-agent-behavior-study">Reproduce</a>
      <a href="https://www.kaggle.com/code/moranzavdi/gemma4-agent-lessons-for-competitors">Lessons</a>
      <a href="https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition">GitHub</a>
      <a href="article.md">Markdown</a>
      <a href="llms.txt">llms.txt</a>
      <span>Moran Zavdi · Apache-2.0</span>
    </nav>

    <header class="hero">
      <h1>When Better Agent Behavior Does Not Improve Accuracy</h1>
      <p class="lede">
        An evidence-first retrospective on building and evaluating a code-repair agent
        for the Gemma 4 Developer Agent Competition
      </p>
      <p class="meta">Moran Zavdi · 2026-11-17</p>
    </header>

    <article>
{body}
    </article>

    <section class="resources" aria-label="Additional resources">
      <h2>Additional resources</h2>
      <ul>
        <li><a href="https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/from-local-validation-to-live-evaluation">Kaggle paper writeup — From Local Validation to Live Evaluation</a></li>
        <li><a href="https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy">Kaggle dataset — Gemma4 Agent Behavior vs Accuracy</a></li>
        <li><a href="https://www.kaggle.com/code/moranzavdi/reproduce-gemma4-agent-behavior-study">Reproduce notebook</a> ·
            <a href="https://www.kaggle.com/code/moranzavdi/explore-gemma4-agent-calibration">Explore</a> ·
            <a href="https://www.kaggle.com/code/moranzavdi/gemma4-agent-lessons-for-competitors">Lessons</a></li>
        <li><a href="https://www.kaggle.com/datasets/moranzavdi/gemma4-soundness-and-punica-bench">Paper-track dataset</a> ·
            <a href="https://www.kaggle.com/code/moranzavdi/from-local-validation-to-live-evaluation">Paper-track notebook</a></li>
        <li><a href="https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition">GitHub evidence release</a></li>
        <li><a href="https://medium.com/@when1go2market">Medium</a></li>
        <li><a href="https://www.kaggle.com/competitions/gemma-4-developer-agent">Gemma 4 Developer Agent Competition</a></li>
      </ul>
    </section>

    <p class="credit">
      Written by <strong>Moran Zavdi</strong>.
      SEO / AEO / GEO:
      <a href="robots.txt">robots.txt</a> ·
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
    print(f"wrote docs/index.html ({(docs / 'index.html').stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
