# Git入門:ブランチ・コミットと巻き戻し

> 図は `images/` フォルダに置いています。

> **図の色の見方**
> **青** = 基本の流れ・安定した状態(`main`、コマンド、ポイント)
> **黄** = 作業中・新しく作られるもの・注意が必要なところ
> **白** = 補足・リモートなど外側の状態

## 目次

1. コミットとは
2. ブランチとは
3. ブランチ汚染とは
4. 過去のコミットに巻き戻す方法
5. 安全に試すコツ
6. GUIツール(GitHub Desktop・SourceTree・TortoiseGit)の用語集
7. 練習問題(わざと汚染して巻き戻す)

---

## 1. コミットとは

コミットは、ある時点のプロジェクト全体のスナップショットです。それぞれにハッシュ(例: `a1b2c3d`)が付き、1つ前のコミットを指しています。この連なりが「履歴」です。

変更は次の4つの場所を通ります。

![Gitの流れ](images/git_flow.svg)

```bash
git status                  # 今の状態を確認
git add ファイル名           # コミット対象にする(ステージに載せる)
git commit -m "メッセージ"    # 手元の履歴に記録する
git push                    # リモートへ送る
git log --oneline           # 履歴を一覧で見る
```

---

## 2. ブランチとは

ブランチは、特定のコミットを指す名前付きのポインタです。コピーを作るわけではないので、作成は一瞬で軽く済みます。`HEAD` は「今自分がいるブランチ」を示します。

使い方の基本は、`main` を安定版として保ち、作業は別ブランチで行い、完成したら `main` に統合することです。

![ブランチとマージ](images/git_branch.svg)

```bash
git branch                    # ブランチ一覧
git switch -c feature/timer   # 新規作成して移動
git switch main               # 移動
git merge feature/timer       # 今のブランチに統合
git branch -d feature/timer   # 統合済みブランチを削除
```

---

## 3. ブランチ汚染とは

ブランチ汚染は、本来入れたくないものがブランチに混ざった状態です。よくある例は次のとおりです。

- `main` に直接、作りかけの変更をコミットしてしまった
- `.vs/` や `Library/` などの不要ファイルをコミットした
- パスワードやAPIキーなどの秘密情報をコミットした
- 別の作業のコミットが混ざったままマージした

**予防策**

- 作業は必ずブランチを切って行う
- `.gitignore` を最初に用意する
- コミット前に `git status` と `git diff --staged` で中身を確認する
- **プルリクエスト(推奨)**: `main` へ直接 push せず、作業ブランチを push してプルリクエスト(PR)を作り、差分を確認してからマージする。不要ファイルや秘密情報、別作業のコミットの混入をマージ前に見つけられる。GitHubの設定(ブランチ保護)で `main` への直接 push を禁止すると、より確実に防げる

```bash
git switch -c feature/timer          # 作業ブランチを作る
git push -u origin feature/timer     # ブランチを push
# GitHub上でプルリクエストを作成 → 差分を確認 → マージ
```

プルリクエストの流れは次の図のとおりです。

![プルリクエストの流れ](images/git_pr.svg)

---

## 4. 過去のコミットに巻き戻す方法

状況によって使うコマンドが変わります。

### A. まだコミットしていない変更を捨てる

```bash
git restore ファイル名           # ファイルの変更を破棄
git restore --staged ファイル名   # git add を取り消す(変更は残る)
git clean -fd                    # 追跡されていないファイルを削除
```

> **注意**: `git clean` で消えたファイルは戻せません。事前に `git clean -nd` で削除対象を確認してください。

### B. コミット済みだが、まだ push していない

`git reset` で、ブランチの指す位置を過去のコミットまで戻します。

```bash
git log --oneline               # 戻りたいコミットのハッシュを調べる
git reset --soft HEAD~1         # 1つ前に戻る。変更はステージに残る
git reset --mixed HEAD~1        # 1つ前に戻る。変更は作業ディレクトリに残る(既定)
git reset --hard a1b2c3d        # 指定コミットに戻る。以降の変更は消える
```

| オプション | コミット | ステージ | ファイルの中身 |
|---|---|---|---|
| `--soft` | 取り消す | 残る | 残る |
| `--mixed` | 取り消す | 取り消す | 残る |
| `--hard` | 取り消す | 取り消す | 消える |

### C. すでに push 済み(共同作業中)

履歴を書き換えずに、「打ち消すコミット」を新しく作る `git revert` を使います。

```bash
git revert a1b2c3d              # そのコミットの変更を打ち消すコミットを作る
git push
```

`reset` と `revert` の違いは次の図のとおりです。

![resetとrevertの違い](images/git_reset_revert.svg)

`git reset --hard` の後に `git push --force` で履歴を書き換える方法もあります。ただし、他の人の履歴と食い違って混乱を招くので、共有ブランチでは避けるのが基本です。自分専用のブランチでやむを得ない場合は、`--force` より安全な `git push --force-with-lease` を使います。

### D. 間違えて `reset --hard` してしまった

`git reflog` は、HEADが動いた記録をすべて残しています。消えたように見えるコミットも、多くの場合ここから戻せます。

```bash
git reflog                      # 操作履歴を見る
git reset --hard HEAD@{2}       # 戻りたい時点に復帰
```

> **注意**: reflog の記録は一定期間(既定では約90日)で消えます。

### E. 秘密情報をコミットしてしまった

> **注意**: 履歴から消しても、一度 push したものは漏れた前提で考えます。先にパスワードやキーを無効化(再発行)してください。そのうえで、`git filter-repo` などで履歴から削除します。

### 迷ったときの選び方

| やりたいこと | 使うコマンド |
|---|---|
| コミット前の変更を捨てたい | `git restore` |
| 自分だけのローカルコミットをやり直したい | `git reset` |
| push 済みの変更を取り消したい | `git revert` |
| 消してしまった履歴を探したい | `git reflog` |

---

## 5. 安全に試すコツ

巻き戻しの前に、今の状態にバックアップ用のブランチを作っておくと安心です。失敗してもすぐ元に戻せます。

```bash
git branch backup-before-reset
```

---

## 6. GUIツールの用語集

GUIツールのボタンやメニューは、どれもGitのコマンド(CUI)と同じことをしています。

| 意味 | Git(CUI) | GitHub Desktop | SourceTree | TortoiseGit |
|---|---|---|---|---|
| コミット対象に選ぶ | `git add` | 変更ファイルのチェック | Stage | Add |
| 変更を記録する | `git commit` | Commit | Commit | Git Commit |
| リモートへ送る | `git push` | Push origin | Push | Git Push |
| 更新情報だけ取得する | `git fetch` | Fetch origin | Fetch | Git Fetch |
| 取得して取り込む | `git pull` | Pull origin | Pull | Git Pull |
| ブランチを作る | `git switch -c` | New Branch | Branch | Create Branch |
| ブランチを切り替える | `git switch` | Current Branch で選ぶ | Checkout | Switch/Checkout |
| ブランチを統合する | `git merge` | Merge into Current Branch | Merge | Merge |
| 未コミットの変更を破棄する | `git restore` | Discard Changes | Discard | Revert |
| 過去に戻す | `git reset` | なし | Reset current branch to this commit | Reset to this |
| 打ち消しコミットを作る | `git revert` | Revert Changes in Commit | Reverse commit | Revert change by this commit |

> **注意**: メニュー名はバージョンや表示言語で変わることがあります。

---

## 7. 練習問題(わざと汚染して巻き戻す)

練習用の新しいフォルダで試します。本物のプロジェクトでは行わないでください。

```bash
mkdir git-practice && cd git-practice
git init
echo "A" > a.txt && git add a.txt && git commit -m "A"
echo "B" > b.txt && git add b.txt && git commit -m "B"
echo "C" > c.txt && git add c.txt && git commit -m "C(間違い)"
git log --oneline
```

1. `git reset --soft HEAD~1` を実行し、`git status` で c.txt がステージに残っていることを確認する
2. `git commit -m "C"` でコミットし直す
3. `git reset --hard HEAD~1` を実行し、c.txt が消えることを確認する
4. `git reflog` で消えたコミットを探し、`git reset --hard` で復元する
5. `git revert HEAD` で「打ち消しコミット」が増えることを `git log --oneline` で確認する
