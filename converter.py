#!/usr/bin/env python3
"""
Markdown <-> HTML converter with syntax highlighting (Pygments).
Auto-detects conversion direction based on file extensions.

Usage:
    # Markdown -> HTML
    python converter.py -i README.md -o out.html --embed-css
    python converter.py -i notes.md -o site/index.html --css-file style.css

    # HTML -> Markdown
    python converter.py -i page.html -o page.md
"""

import argparse
import pathlib
import sys
from markdown import markdown
from pygments.formatters import HtmlFormatter
from markdownify import markdownify as mdify

DEFAULT_CSS = """
/* basic page layout */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    max-width: 900px;
    margin: 40px auto;
    line-height: 1.6;
    padding: 0 20px;
    color: #111827;
    background: #ffffff;
}

/* headings */
h1, h2, h3, h4 { margin-top: 1.2em; }
h1 { font-size: 2.4rem; }

/* links */
a { color: #065f46; text-decoration: none; }
a:hover { text-decoration: underline; }

/* code blocks container (markdown extension codehilite uses .codehilite) */
.codehilite { padding: 0.8rem; border-radius: 6px; overflow: auto; }

/* inline code */
code { background:#f3f4f6; padding: 0.15rem 0.25rem; border-radius:4px; font-size:0.95em; }

img { max-width: 100%; height: auto; display:block; margin: 10px 0; }

/* small nice toc style if user adds one */
.toc { background: #f8fafc; padding: 12px; border-radius: 6px; margin-bottom: 18px; }
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title}</title>
<style>
{css}
{pygments_css}
</style>
</head>
<body>
<article>
{content}
</article>
</body>
</html>
"""

def generate_pygments_css():
    fmt = HtmlFormatter()
    return fmt.get_style_defs('.codehilite')

def md_to_html(md_text, extensions=None, extension_configs=None):
    if extensions is None:
        extensions = ['fenced_code', 'codehilite', 'toc']
    return markdown(md_text, extensions=extensions, extension_configs=extension_configs or {})

def html_to_md(html_text):
    return mdify(html_text, heading_style="ATX")

def main():
    p = argparse.ArgumentParser(description="Markdown <-> HTML converter (auto-detects direction)")
    p.add_argument('-i', '--input', required=True, help="Input file (.md or .html)")
    p.add_argument('-o', '--output', required=True, help="Output file (.html or .md)")
    p.add_argument('--embed-css', action='store_true', help="Embed default CSS directly into HTML")
    p.add_argument('--css-file', default=None, help="Path to custom CSS file to include")
    p.add_argument('--title', default=None, help="HTML title (defaults to input filename)")
    args = p.parse_args()

    in_path = pathlib.Path(args.input)
    out_path = pathlib.Path(args.output)

    if not in_path.exists():
        print("Input file not found:", in_path, file=sys.stderr)
        sys.exit(2)

    text = in_path.read_text(encoding='utf-8')

    in_ext, out_ext = in_path.suffix.lower(), out_path.suffix.lower()

    if in_ext == ".md" and out_ext == ".html":
        # Markdown -> HTML
        ext_cfg = {'codehilite': {'linenums': False, 'guess_lang': True}}
        html_body = md_to_html(text, extension_configs=ext_cfg)

        title = args.title or in_path.stem
        if args.css_file:
            css_text = pathlib.Path(args.css_file).read_text(encoding='utf-8')
        else:
            css_text = DEFAULT_CSS if args.embed_css or not args.css_file else ""

        pygments_css = generate_pygments_css()
        final = HTML_TEMPLATE.format(title=title, css=css_text, pygments_css=pygments_css, content=html_body)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final, encoding='utf-8')
        print(f"Converted {in_path} -> {out_path} (Markdown -> HTML)")

    elif in_ext == ".html" and out_ext == ".md":
        # HTML -> Markdown
        md_content = html_to_md(text)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md_content, encoding='utf-8')
        print(f"Converted {in_path} -> {out_path} (HTML -> Markdown)")

    else:
        print("❌ Unsupported conversion: input must be .md -> .html or .html -> .md", file=sys.stderr)
        sys.exit(3)

if __name__ == '__main__':
    main()