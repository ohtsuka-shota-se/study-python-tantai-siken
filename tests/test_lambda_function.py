import sys
import types
import importlib
from unittest.mock import patch, MagicMock

# ── ① 本物のimportより前に、偽の boto3 を sys.modules に登録 ──
fake_boto3 = types.ModuleType("boto3") # 「boto3」という名前の空のモジュールオブジェクトを生成
fake_boto3.client = MagicMock() # boto3.client() の呼び出しをモック化（偽物に置き換え）
sys.modules.setdefault("boto3", fake_boto3) # すでにboto3がロードされていなければ、sys.modulesに偽物を登録

# ── ② ここで初めて lambda_function をimport ──
lambda_function = importlib.import_module("lambda_function") # 


# ── ③ 各テストケース ──

# ③-1
def test_returns_200_with_object_content():
    # Amazon S3の実際のレスポンス構造を再現する
    fake_body = MagicMock()
    fake_body.read.return_value = b"hello world"

    # S3クライアント自体を模したモックを作成し、
    # get_object() が呼ばれたら実際のS3同様 {"Body": ...} という辞書形式で
    # レスポンスを返すように設定する
    fake_s3_client = MagicMock()
    fake_s3_client.get_object.return_value = {"Body": fake_body}

    # boto3.client("s3") の呼び出しを fake_s3_client に差し替えて
    # Lambda関数を実行する（with を抜けると自動的に元に戻る）
    with patch.object(lambda_function.boto3, "client", return_value=fake_s3_client):
        result = lambda_function.lambda_handler(
            {"bucket": "my-bucket", "key": "my-key.txt"}, None
        )

    # ステータスコードとレスポンスボディが期待通りかを検証
    assert result["statusCode"] == 200
    assert result["body"] == "hello world"
    # get_object() が想定通りの引数で1回だけ呼ばれたことを検証
    fake_s3_client.get_object.assert_called_once_with(
        Bucket="my-bucket", Key="my-key.txt"
    )

# ③-2
def test_returns_500_when_connection_fails():
    # S3クライアントを模したモックを作成し、
    # get_object() が呼ばれた際に接続エラー（例外）を発生させるよう設定する
    fake_s3_client = MagicMock()
    fake_s3_client.get_object.side_effect = Exception("connection timeout")

    # boto3.client("s3") の呼び出しを fake_s3_client に差し替えて
    # 例外発生時のLambda関数の挙動を実行・検証する
    with patch.object(lambda_function.boto3, "client", return_value=fake_s3_client):
        result = lambda_function.lambda_handler(
            {"bucket": "my-bucket", "key": "my-key.txt"}, None
        )

    # S3への接続失敗時に、Lambda関数が500エラーを返すことを検証
    assert result["statusCode"] == 500

# ③-3
def test_returns_400_when_bucket_or_key_missing():
    # bucket が無い場合
    result = lambda_function.lambda_handler({"key": "my-key.txt"}, None)
    assert result["statusCode"] == 400

    # key が無い場合
    result = lambda_function.lambda_handler({"bucket": "my-bucket"}, None)
    assert result["statusCode"] == 400

    # 両方とも無い場合
    result = lambda_function.lambda_handler({}, None)
    assert result["statusCode"] == 400
