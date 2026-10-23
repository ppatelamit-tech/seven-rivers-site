#!/usr/bin/env python3
"""Render posts/*.md into blog/<slug>.html and rebuild blog/index.html.

No dependencies. Run from anywhere: python3 tools/build_blog.py

Post format (posts/<slug>.md):

    ---
    title: When healing becomes *identity*      # *word* becomes the display-em span
    date: 2026-07-14
    category: On the two currents
    summary: One or two sentences shown on the Writing index.
    ---
    Body in light Markdown: paragraphs separated by blank lines,
    > blockquote lines, ## subheadings, *italic*, **bold**, [text](url).

Drafts live in drafts/<slug>.md with the same format; they are not built.
To publish a draft, move it to posts/ and run this script.
"""
import glob, html, os, re, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "posts")
BLOG = os.path.join(ROOT, "blog")
TEMPLATE = os.path.join(ROOT, "tools", "post_template.html")
INDEX_TEMPLATE = os.path.join(ROOT, "tools", "index_template.html")
SITE = "https://sevenriverspsychiatry.com"


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    for k in ("title", "date", "category", "summary"):
        if k not in meta:
            sys.exit(f"{path}: front matter needs '{k}'")
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["body"] = m.group(2).strip()
    meta["_date"] = date.fromisoformat(meta["date"])
    return meta


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s


def render_body(md):
    out = []
    for block in re.split(r"\n\s*\n", md.strip()):
        b = block.strip()
        if not b:
            continue
        if b.startswith("## "):
            out.append(f"<h2>{inline(b[3:])}</h2>")
        elif b.startswith(">"):
            q = " ".join(l.lstrip("> ").strip() for l in b.splitlines())
            out.append(f"<blockquote>{inline(q)}</blockquote>")
        else:
            out.append(f"<p>{inline(' '.join(l.strip() for l in b.splitlines()))}</p>")
    return "\n\n          ".join(out)


def title_html(t):
    return re.sub(r"\*(.+?)\*", r'<span class="display-em">\1</span>', html.escape(t, quote=False))


def title_plain(t):
    return t.replace("*", "")


def month_year(d):
    return d.strftime("%B %Y")


def fill(tpl, mapping):
    for k, v in mapping.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl


def main():
    posts = [parse(p) for p in glob.glob(os.path.join(POSTS, "*.md"))]
    posts.sort(key=lambda p: p["_date"], reverse=True)
    tpl = open(TEMPLATE, encoding="utf-8").read()
    for p in posts:
        words = len(re.findall(r"\w+", p["body"]))
        minutes = max(1, round(words / 180))
        page = fill(tpl, {
            "title_plain": html.escape(title_plain(p["title"]), quote=True),
            "title_html": title_html(p["title"]),
            "description": html.escape(p["summary"], quote=True),
            "category": html.escape(p["category"], quote=False),
            "month_year": month_year(p["_date"]),
            "minutes": str(minutes),
            "body": render_body(p["body"]),
            "canonical": f"{SITE}/blog/{p['slug']}.html",
        })
        with open(os.path.join(BLOG, p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
        print("built", p["slug"] + ".html", f"({minutes} min)")

    cards = []
    for p in posts:
        cards.append(
            '          <div class="post-card">\n'
            f'            <p class="meta">{html.escape(p["category"], quote=False)} &middot; {month_year(p["_date"])}</p>\n'
            f'            <h3><a href="{p["slug"]}.html">{title_plain(html.escape(p["title"], quote=False))}</a></h3>\n'
            f'            <p>{inline(p["summary"])}</p>\n'
            '          </div>'
        )
    idx = fill(open(INDEX_TEMPLATE, encoding="utf-8").read(), {"cards": "\n".join(cards)})
    with open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx)
    print("built index.html with", len(posts), "posts")


if __name__ == "__main__":
    main()


def build_sitemap():
    """Regenerate sitemap.xml from every served page."""
    pages = ["index.html", "home.html", "about.html", "philosophy.html", "services.html",
             "fees.html", "telehealth.html", "faq.html", "contact.html", "blog/index.html"]
    pages += sorted("blog/" + os.path.basename(p) for p in glob.glob(os.path.join(BLOG, "*.html"))
                    if os.path.basename(p) != "index.html")
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        loc = SITE + "/" if p == "index.html" else f"{SITE}/{p}"
        prio = "1.0" if p in ("index.html", "home.html") else ("0.6" if p.startswith("blog/") else "0.8")
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("built sitemap.xml with", len(pages), "urls")


if __name__ == "__main__":
    build_sitemap()
