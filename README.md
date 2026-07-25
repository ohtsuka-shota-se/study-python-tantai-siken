# study-python-tantai-siken

S3からオブジェクトを取得して内容を返すAWS Lambda関数と、そのユニットテストです。

## 構成

```
lambda_function.py   # Lambdaハンドラ本体
tests/
  test_lambda_function.py  # ユニットテスト
  README.md                 # テストの方針・対応表
docs/
  github-push.md            # GitHubへのpush手順
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
# macOS / Linux
source .venv/bin/activate

# 4. 依存パッケージをインストール
pip install -r requirements.txt
```

## テストの実行

```bash
pytest tests/test_lambda_function.py -v
```

テストの内容や `lambda_handler` との対応関係は [`tests/README.md`](tests/README.md) を参照してください。

## AWSへのデプロイについて

このリポジトリはLambda関数のコードのみを管理しています。デプロイ用のIaC（SAM/CDK/Terraform等）は含まれていないため、
実際にAWS上で動かす場合は `lambda_function.py` を手動でLambda関数としてアップロードするか、
別途デプロイの仕組みを用意してください。
