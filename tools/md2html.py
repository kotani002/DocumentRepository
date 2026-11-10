#!/usr/bin/env python3
"""Markdown(:::note 記法つき)を、共通スタイルのHTMLに変換する。

使い方(リポジトリのルートで実行):
    python tools/md2html.py docs/git/git-study.md docs/git/index.html

必要なもの: pip install markdown
"""
import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE_LABELS = {"info": "補足", "warn": "注意", "alert": "警告"}


def convert_notes(src: str) -> str:
    """:::note [info|warn|alert] ... ::: を <div class="note ..."> に置き換える。"""
    pattern = re.compile(r"^:::note(?:[ \t]+(info|warn|alert))?[ \t]*\n(.*?)\n:::[ \t]*$",
                         re.M | re.S)

    def repl(m):
        kind = m.group(1) or "info"
        return (f'<div class="note note-{kind}" markdown="1">\n'
                f'<p class="note-title">{NOTE_LABELS[kind]}</p>\n\n'
                f'{m.group(2)}\n\n</div>')

    return pattern.sub(repl, src)


def main(md_path: str, out_path: str) -> None:
    src = open(md_path, encoding="utf-8").read()
    title = re.search(r"^# (.+)$", src, re.M).group(1).strip()
    src = re.sub(r"^# .+\n", "", src, count=1, flags=re.M)

    body = markdown.markdown(
        convert_notes(src),
        extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
    )

    # h2 に id を付け、目次(最初の h2 直後の番号付きリスト)をリンクにする
    n = {"i": -1}

    def h2(m):
        n["i"] += 1
        sid = "toc" if n["i"] == 0 else f"sec{n['i']}"
        return f'<h2 id="{sid}">{m.group(1)}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", h2, body)

    def link_toc(m):
        items = re.findall(r"<li>(.*?)</li>", m.group(0), flags=re.S)
        lis = "\n".join(f'<li><a href="#sec{i + 1}">{t}</a></li>' for i, t in enumerate(items))
        return f"<ol>\n{lis}\n</ol>"

    body = re.sub(r'(?<=<h2 id="toc">目次</h2>\n)<ol>.*?</ol>', link_toc, body, count=1, flags=re.S)

    out_dir = os.path.dirname(os.path.abspath(out_path))
    css = os.path.relpath(os.path.join(ROOT, "assets", "css", "style.css"), out_dir).replace(os.sep, "/")
    top = os.path.relpath(ROOT, out_dir).replace(os.sep, "/") + "/"

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<header><div class="inner"><h1>{title}</h1></div></header>
<nav class="breadcrumb"><a href="{top}">資料トップ</a> / {title}</nav>
<main>
{body}
</main>
<footer>資料置き場</footer>
</body>
</html>
"""
    open(out_path, "w", encoding="utf-8").write(html)
    print("wrote", out_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
