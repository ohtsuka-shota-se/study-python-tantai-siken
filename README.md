# study-python-tantai-siken

S3からオブジェクトを取得して内容を返すAWS Lambda関数と、そのユニットテストです。

公開ページ（GitHub Pages）: https://ohtsuka-shota-se.github.io/study-python-tantai-siken/

## 構成

```
lambda_function.py   # Lambdaハンドラ本体
tests/
  test_lambda_function.py  # ユニットテスト
  README.md                 # テストの方針・対応表
docs/
  index.html                 # GitHub Pages用ドキュメント
  github-push.md             # GitHubへのpush手順
  debugging.md                # VSCodeデバッグ用語集
requirements.txt
```

## `lambda_handler` の仕様

`event` に `bucket` と `key` を渡すと、対象のS3オブジェクトの中身を文字列として返します。

| 条件 | レスポンス |
|---|---|
| `bucket` または `key` が無い | `{"statusCode": 400}` |
| S3から正常に取得できた | `{"statusCode": 200, "body": "<オブジェクトの中身>"}` |
| S3アクセス時に例外が発生した | `{"statusCode": 500, "body": "<エラー内容>"}` |

## ローカル環境構築

前提: Python 3.12系がインストール済み（`python --version` で確認）

```bash
# 1. リポジトリを取得
git clone https://github.com/ohtsuka-shota-se/study-python-tantai-siken.git
cd study-python-tantai-siken

# 2. 仮想環境を作成
python -m venv .venv

# 3. 仮想環境を有効化
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (コマンドプロンプト)
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate

# 4. 依存パッケージをインストール
pip install -r requirements.txt
```

## テストの実行

### コマンドラインから実行する場合

```bash
pytest tests/test_lambda_function.py -v
```

### VSCodeから実行する場合

このリポジトリの `.vscode/settings.json` で pytest がテストランナーとして設定済みのため、
追加設定なしで以下の手順で実行できます。

1. 左側のアクティビティバーから「テスト」（フラスコのアイコン）を開く
2. `tests/test_lambda_function.py` 配下にテスト関数が自動で一覧表示される
   （表示されない場合は仮想環境を有効化した状態でVSCodeを開き直し、
   コマンドパレットから `Python: Configure Tests` を実行）
3. テスト名の横にある ▷ ボタンで実行、🐞 ボタンでデバッグ実行ができる
4. ファイル名やルート（`tests`）の横のボタンから、まとめて実行することも可能

デバッグ実行時の用語（ブレークポイント・ステップオーバー等）は
[`docs/debugging.md`](docs/debugging.md) を参照してください。

テストの内容や `lambda_handler` との対応関係は [`tests/README.md`](tests/README.md) を参照してください。

## 関連ドキュメント

- [`tests/README.md`](tests/README.md) — テストの方針・テストケースの対応表
- [`docs/pytest-flow.md`](docs/pytest-flow.md) — pytest実行時にどのPythonファイルが呼ばれるかのフロー図
- [`docs/debugging.md`](docs/debugging.md) — VSCodeデバッグ用語集（ブレークポイント・ステップ実行など）
- [`docs/github-push.md`](docs/github-push.md) — GitHubへのpush手順・GitHub Pagesの有効化手順

## AWSへのデプロイについて

このリポジトリはLambda関数のコードのみを管理しています。デプロイ用のIaC（SAM/CDK/Terraform等）は含まれていないため、
実際にAWS上で動かす場合は `lambda_function.py` を手動でLambda関数としてアップロードするか、
別途デプロイの仕組みを用意してください。
