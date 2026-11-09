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

## GitHub Pages の設定

1. リポジトリの Settings → Pages を開く
2. Branch に `document_git` を選び、フォルダは `/ (root)` にして保存する
3. 数分後に `https://ユーザー名.github.io/リポジトリ名/` で表示される

> 無料プランでは、リポジトリを public にすると Pages を使えます。
