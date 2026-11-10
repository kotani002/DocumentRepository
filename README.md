# 資料置き場

学習メモや資料を HTML でまとめ、GitHub Pages で公開するためのリポジトリです。
資料はすべて `document_git` ブランチに置きます。

## フォルダ構成

```
.
├─ index.html              資料トップ(資料の一覧)
├─ .nojekyll               GitHub Pages でそのまま HTML を表示する設定
├─ assets/
│  └─ css/style.css        全資料で共通のスタイル(青・白・黄色)
├─ templates/
│  └─ doc-template.html    新しい資料のひな形
├─ tools/
│  └─ md2html.py           Markdown を HTML に変換するスクリプト
└─ docs/
   └─ git/                 資料1つにつきフォルダ1つ
      ├─ index.html        資料の本体
      ├─ git-study.md      元の Markdown(編集用)
      └─ images/           その資料で使う画像
```

## 新しい資料を追加する手順

1. `docs/` の下に、資料名のフォルダを作る(例: `docs/unity-webgl/`)
2. `templates/doc-template.html` を、そのフォルダに `index.html` としてコピーする
3. 中身を書き換え、画像は同じフォルダの `images/` に置く
4. 資料トップ `index.html` の資料一覧に、`<li class="card">` を1つ追加する
5. `git add .` → `git commit` → `git push` で公開される

## Markdown から HTML を作る

資料を Markdown で書いた場合は、変換スクリプトで共通スタイルの HTML にできます。
`:::note` 記法(補足・注意・警告のボックス)にも対応しています。

```bash
pip install markdown
python tools/md2html.py docs/git/git-study.md docs/git/index.html
```

| 書き方 | 表示 | 使いどころ |
|---|---|---|
| `:::note info` | 青のボックス(補足) | 補足説明、豆知識 |
| `:::note warn` | 黄のボックス(注意) | 間違えやすい点、消える操作 |
| `:::note alert` | 赤のボックス(警告) | 情報漏えいなど重大なこと |

内容は、前後を `:::note` と `:::` の行で挟みます。

## GitHub Pages の設定

1. リポジトリの Settings → Pages を開く
2. Branch に `document_git` を選び、フォルダは `/ (root)` にして保存する
3. 数分後に `https://ユーザー名.github.io/リポジトリ名/` で表示される

> 無料プランでは、リポジトリを public にすると Pages を使えます。
