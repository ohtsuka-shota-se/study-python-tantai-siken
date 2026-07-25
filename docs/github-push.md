# GitHubへのpush手順

このプロジェクトを GitHub リポジトリ
[ohtsuka-shota-se/study-python-tantai-siken](https://github.com/ohtsuka-shota-se/study-python-tantai-siken)
にpushするための手順です。

## 前提

- Git for Windows がインストール済み（`git --version` で確認可能）
- GitHubアカウントを持っている
- 認証には Git for Windows に同梱されている **Git Credential Manager** を使う。
  初回pushの際にブラウザが開き、GitHubへのログインを求められる（gh CLI等の追加インストールは不要）

## 初回セットアップ（このリポジトリで一度だけ）

```bash
# 1. ローカルにGitリポジトリを作成
git init

# 2. コミットしたいファイルをステージング
#    .venv/, __pycache__/, .pytest_cache/ などは .gitignore で除外済み
git add .gitignore lambda_function.py tests/ .vscode/ docs/

# 3. 最初のコミット
git commit -m "Initial commit"

# 4. リモートリポジトリを登録
git remote add origin https://github.com/ohtsuka-shota-se/study-python-tantai-siken

# 5. ブランチ名を main に統一
git branch -M main

# 6. push（初回はブラウザでGitHubログインを求められる）
git push -u origin main
```

`git push` を実行するとブラウザが自動で開くので、GitHubアカウントでログインして認証を許可すれば
push が完了します。一度認証すれば、次回以降は再ログイン不要です。

## 2回目以降のpush

初回セットアップ後は、変更を加えるたびに以下を実行するだけです。

```bash
git add <変更したファイル>
git commit -m "変更内容が分かるメッセージ"
git push
```

## 除外しているファイル

`.gitignore` で以下を除外しています。

| パス | 理由 |
|---|---|
| `.venv/` | 仮想環境。各自の環境で作り直せば良いためコミット不要 |
| `__pycache__/`, `*.pyc` | Pythonの自動生成キャッシュ |
| `.pytest_cache/` | pytestの自動生成キャッシュ |
| `.claude/settings.local.json` | Claude Codeのローカル権限設定。個人環境ごとの設定のため |
