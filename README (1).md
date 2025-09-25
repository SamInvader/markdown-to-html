# Markdown <-> HTML Converter

A simple Python script for converting between `Markdown` and `HTML` with syntax highlighting (via [Pygments](https://pygments.org/)).  
It auto-detects the conversion direction based on file extensions.

---

## Features
- Convert `Markdown → HTML` with:
  - Syntax highlighting
  - Optional embedded CSS
  - Custom CSS support
- Convert `HTML → Markdown`
- Clean, responsive default HTML template
- Auto-detects conversion direction

---

## Installation

```bash
pip install markdown markdownify pygments
```

---

## Usage

### Markdown → HTML
```bash
python converter.py -i README.md -o out.html --embed-css
python converter.py -i notes.md -o site/index.html --css-file style.css
```

### HTML → Markdown
```bash
python converter.py -i page.html -o page.md
```

---

## Options

| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `-i, --input`  | Input file (`.md` or `.html`)                                               |
| `-o, --output` | Output file (`.html` or `.md`)                                              |
| `--embed-css`  | Embed default CSS directly into HTML                                        |
| `--css-file`   | Path to custom CSS file (overrides `--embed-css` if provided)               |
| `--title`      | HTML title (defaults to input filename)                                     |

---

## Example Output

Markdown rendered to HTML includes:
- Syntax-highlighted code blocks  
- Styled inline code  
- Responsive images  
- Optional table of contents (if you add `[TOC]` in your Markdown)

---

## License
MIT
