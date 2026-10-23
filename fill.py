#!/usr/bin/env python3
"""One job: when your Osmind patient portal goes live, put its URL below
and run this script once (python3 fill.py). It swaps every Book button
and booking link across the whole site, then re-upload to Netlify."""

PORTAL_URL = ""   # e.g. "https://sevenrivers.osmind.org"

import glob, os

def main():
    if not PORTAL_URL:
        print("Set PORTAL_URL at the top of this file first.")
        return
    here = os.path.dirname(os.path.abspath(__file__))
    total = 0
    for path in glob.glob(os.path.join(here, "**", "*.html"), recursive=True):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if "/contact.html#book" in text:
            text = text.replace('href="/contact.html#book"', f'href="{PORTAL_URL}"')
            text = text.replace("href='/contact.html#book'", f"href='{PORTAL_URL}'")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            total += 1
            print("updated", os.path.relpath(path, here))
    print(f"Done. {total} file(s) now point at the portal.")
    print("Tip: also update the contact page booking card text, which still says the portal is coming soon.")

if __name__ == "__main__":
    main()
