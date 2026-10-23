#!/usr/bin/env python3
"""Idempotent: ensures every page (and the blog templates) carries favicon,
canonical, Open Graph / Twitter tags. Run after adding a new page:
    python3 tools/patch_head.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://sevenriverspsychiatry.com"
MARK = "<!-- srp-head -->"

def rel_prefix(path):
    depth = os.path.relpath(path, ROOT).count(os.sep)
    return "../" * depth

def canonical_for(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return SITE + "/"
    if rel.startswith("tools/"):
        return "{{canonical}}"
    return f"{SITE}/{rel}"

def block(path, title, desc):
    pre = rel_prefix(path)
    canon = canonical_for(path)
    og_type = "article" if "/blog/" in canon or "tools/post" in path else "website"
    return f"""{MARK}
  <link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{pre}assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Seven Rivers Psychiatry">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <!-- /srp-head -->"""

def patch(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"\n  " + re.escape(MARK) + r".*?<!-- /srp-head -->", "", s, flags=re.S)
    # drop any stray standalone canonical (older template)
    s = re.sub(r'\n  <link rel="canonical" href="[^"]*">', "", s)
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    s = s.replace("</head>", "  " + block(path, title, desc) + "\n</head>", 1)
    open(path, "w", encoding="utf-8").write(s)
    print("patched", os.path.relpath(path, ROOT))

if __name__ == "__main__":
    files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "blog", "*.html")) \
        + [os.path.join(ROOT, "tools", "post_template.html"), os.path.join(ROOT, "tools", "index_template.html")]
    for f in files:
        patch(f)
