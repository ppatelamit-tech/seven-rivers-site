# Seven Rivers Psychiatry — sevenriverspsychiatry.com

Plain HTML/CSS site, deployed by Netlify from the `main` branch of this repo. No build step; `netlify.toml` publishes the repo root.

- Pages: `*.html`, styles in `css/styles.css`, behavior in `js/main.js`.
- Blog: write Markdown in `posts/`, run `python3 tools/build_blog.py`, commit. Drafts awaiting review live in `drafts/`.
- Voice, rules, and topic queue: `tools/WRITING_GUIDE.md`.
- When the Osmind portal goes live: set its URL in `fill.py`, run it once, commit.
