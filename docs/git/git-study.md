# Git入門:branch・commit と巻き戻し

## 目次

1. commit とは
2. branch とは
3. push とは
4. branch 汚染とは
5. 過去の commit に巻き戻す方法
6. 安全に試すコツ
7. GUIツール(GitHub Desktop・SourceTree・TortoiseGit)の用語集
8. 練習問題(わざと汚染して巻き戻す)

---

## 1. commit とは

commit は、ある時点のプロジェクト全体の snapshot です。それぞれに hash(例: `a1b2c3d`)が付き、1つ前の commit を指しています。この連なりが「履歴」です。

変更は次の4つの場所を通ります。

![Gitの流れ](images/git_flow.svg)

```bash
git status                  # 今の状態を確認
git add ファイル名           # commit 対象にする(stage に載せる)
git commit -m "message"     # 手元の履歴に記録する
git push                    # remote へ送る
git log --oneline           # 履歴を一覧で見る
```

:::note info
`git pull` は、`git fetch`(remote の更新を取得するだけ)と `git merge`(手元に取り込む)をまとめた操作です。取り込む前に内容を確認したいときは、先に `git fetch` だけを実行します。
:::

---

## 2. branch とは

branch は、特定の commit を指す名前付きの pointer です。コピーを作るわけではないので、作成は一瞬で軽く済みます。`HEAD` は「今自分がいる branch」を示します。

使い方の基本は、`main` を安定版として保ち、作業は別の branch で行い、完成したら `main` に merge することです。

![branchとmerge](images/git_branch.svg)

```bash
git branch                    # branch 一覧
git switch -c feature/timer   # 新規作成して移動
git switch main               # 移動
git merge feature/timer       # 今の branch に merge
git branch -d feature/timer   # merge 済みの branch を削除
```

:::note info
古い解説では、branch の移動に `git checkout` が使われています。現在は `git switch`(branch の移動)と `git restore`(ファイルの復元)に役割が分かれていて、こちらのほうが分かりやすいため、この資料ではこの2つを使っています。
:::

---

## 3. push とは

push は、手元(local)の commit を remote(GitHub など)に送ることです。送られるのは commit 済みの内容だけで、commit していない変更は送られません。送る単位は branch です。

![pushの流れ](images/git_push.svg)

```bash
git remote -v                       # 送り先(origin)の URL を確認
git push -u origin feature/timer    # 初めて送る branch。送り先を origin に設定する
git push                            # 2回目以降。今の branch を、設定済みの送り先へ送る
git push origin main                # branch を指定して送る
```

`origin` は、remote につけられる標準の名前です。`-u` を付けて1回 push すると、以降は `git push` だけで送れます。

:::note info
push のあとに `git status` を実行して、`up to date with 'origin/...'` と表示されれば、手元と remote が同じ状態です。
:::

:::note warn
remote のほうが先に進んでいる(他の人が先に push した)と、push は rejected(拒否)されます。その場合は、先に `git pull` で remote の変更を取り込んでから、もう一度 push します。`--force` で無理に上書きしないでください。
:::

---

## 4. branch 汚染とは

branch 汚染は、本来入れたくないものが branch に混ざった状態です。よくある例は次のとおりです。

- `main` に直接、作りかけの変更を commit してしまった
- `.vs/` や `Library/` などの不要ファイルを commit した
- パスワードやAPIキーなどの秘密情報を commit した
- 別の作業の commit が混ざったまま merge した

**予防策**

- 作業は必ず branch を切って行う
- `.gitignore` を最初に用意する
- commit 前に `git status` と `git diff --staged` で中身を確認する
- **Pull Request(推奨)**: `main` へ直接 push せず、作業 branch を push して Pull Request(PR)を作り、差分を確認してから merge する。不要ファイルや秘密情報、別作業の commit の混入を merge 前に見つけられる

```bash
git switch -c feature/timer          # 作業 branch を作る
git push -u origin feature/timer     # branch を push
# GitHub 上で Pull Request を作成 → 差分を確認 → merge
```

Pull Request の流れは次の図のとおりです。

![Pull Requestの流れ](images/git_pr.svg)

:::note info
GitHub の設定(branch 保護)で `main` への直接 push を禁止すると、Pull Request を必ず通すようにできます。うっかり `main` に push してしまう事故を、仕組みで防げます。
:::

:::note info
`.gitignore` に書いたファイルは、まだ追跡されていない場合に限って無視されます。すでに commit してしまったファイルは、`git rm --cached ファイル名` で追跡から外してから、commit し直します。
:::

---

## 5. 過去の commit に巻き戻す方法

状況によって使うコマンドが変わります。

### A. まだ commit していない変更を捨てる

```bash
git restore ファイル名           # ファイルの変更を破棄
git restore --staged ファイル名   # git add を取り消す(変更は残る)
git clean -fd                    # 追跡されていないファイルを削除
```

:::note warn
`git clean` で消えたファイルは戻せません。事前に `git clean -nd` で、削除される対象を確認してください。
:::

### B. commit 済みだが、まだ push していない

`git reset` で、branch の指す位置を過去の commit まで戻します。

```bash
git log --oneline               # 戻りたい commit の hash を調べる
git reset --soft HEAD~1         # 1つ前に戻る。変更は stage に残る
git reset --mixed HEAD~1        # 1つ前に戻る。変更は working directory に残る(既定)
git reset --hard a1b2c3d        # 指定した commit に戻る。以降の変更は消える
```

| オプション | commit | stage | ファイルの中身 |
|---|---|---|---|
| `--soft` | 取り消す | 残る | 残る |
| `--mixed` | 取り消す | 取り消す | 残る |
| `--hard` | 取り消す | 取り消す | 消える |

:::note info
`HEAD~1` は「今の commit の1つ前」という意味です。`HEAD~2` なら2つ前を指します。
:::

:::note warn
`--hard` は、working directory の変更も消します。迷ったときは、先に `--soft` か `--mixed` を使うか、バックアップ用の branch を作ってから実行してください。
:::

### C. すでに push 済み(共同作業中)

履歴を書き換えずに、「打ち消す commit」を新しく作る `git revert` を使います。

```bash
git revert a1b2c3d              # その commit の変更を打ち消す commit を作る
git push
```

`reset` と `revert` の違いは次の図のとおりです。

![resetとrevertの違い](images/git_reset_revert.svg)

:::note warn
`git reset --hard` の後に `git push --force` で履歴を書き換える方法もあります。ただし、他の人の履歴と食い違って混乱を招くので、共有 branch では避けるのが基本です。自分専用の branch でやむを得ない場合は、`--force` より安全な `git push --force-with-lease` を使います。
:::

### D. 間違えて `reset --hard` してしまった

`git reflog` は、HEAD が動いた記録をすべて残しています。消えたように見える commit も、多くの場合ここから戻せます。

```bash
git reflog                      # 操作履歴を見る
git reset --hard HEAD@{2}       # 戻りたい時点に復帰
```

:::note warn
reflog の記録は一定期間(既定では約90日)で消えます。復元は早めに行ってください。
:::

### E. 秘密情報を commit してしまった

:::note alert
履歴から消しても、一度 push したものは漏れた前提で考えます。先にパスワードやキーを無効化(再発行)してください。そのうえで、`git filter-repo` などで履歴から削除します。
:::

### 迷ったときの選び方

| やりたいこと | 使うコマンド |
|---|---|
| commit 前の変更を捨てたい | `git restore` |
| 自分だけの local の commit をやり直したい | `git reset` |
| push 済みの変更を取り消したい | `git revert` |
| 消してしまった履歴を探したい | `git reflog` |

---

## 6. 安全に試すコツ

巻き戻しの前に、今の状態にバックアップ用の branch を作っておくと安心です。失敗してもすぐ元に戻せます。

```bash
git branch backup-before-reset
```

:::note info
バックアップ用の branch は、巻き戻しがうまくいったことを確認してから `git branch -d backup-before-reset` で削除します。
:::

---

## 7. GUIツールの用語集

GUIツールのボタンやメニューは、どれも Git のコマンド(CUI)と同じことをしています。

| 意味 | Git(CUI) | GitHub Desktop | SourceTree | TortoiseGit |
|---|---|---|---|---|
| commit 対象に選ぶ | `git add` | 変更ファイルのチェック | Stage | Add |
| 変更を記録する | `git commit` | Commit | Commit | Git Commit |
| remote へ送る | `git push` | Push origin | Push | Git Push |
| 更新情報だけ取得する | `git fetch` | Fetch origin | Fetch | Git Fetch |
| 取得して取り込む | `git pull` | Pull origin | Pull | Git Pull |
| branch を作る | `git switch -c` | New Branch | Branch | Create Branch |
| branch を切り替える | `git switch` | Current Branch で選ぶ | Checkout | Switch/Checkout |
| branch を統合する | `git merge` | Merge into Current Branch | Merge | Merge |
| commit 前の変更を破棄する | `git restore` | Discard Changes | Discard | Revert |
| 過去に戻す | `git reset` | なし | Reset current branch to this commit | Reset to this |
| 打ち消しの commit を作る | `git revert` | Revert Changes in Commit | Reverse commit | Revert change by this commit |

:::note info
GitHub Desktop には、`git reset` に当たる標準機能がありません。履歴を巻き戻したいときは、コマンド(CUI)で行います。
:::

:::note warn
メニュー名は、バージョンや表示言語で変わることがあります。
:::

---

## 8. 練習問題(わざと汚染して巻き戻す)

:::note warn
練習用の新しいフォルダで試してください。本物のプロジェクトでは行わないでください。
:::

```bash
mkdir git-practice && cd git-practice
git init
echo "A" > a.txt && git add a.txt && git commit -m "A"
echo "B" > b.txt && git add b.txt && git commit -m "B"
echo "C" > c.txt && git add c.txt && git commit -m "C(間違い)"
git log --oneline
```

1. `git reset --soft HEAD~1` を実行し、`git status` で c.txt が stage に残っていることを確認する
2. `git commit -m "C"` で commit し直す
3. `git reset --hard HEAD~1` を実行し、c.txt が消えることを確認する
4. `git reflog` で消えた commit を探し、`git reset --hard` で復元する
5. `git revert HEAD` で「打ち消す commit」が増えることを `git log --oneline` で確認する
