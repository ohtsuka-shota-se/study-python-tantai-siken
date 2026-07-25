# tests/

`lambda_function.py` の `lambda_handler` に対するユニットテストです。

## 実行方法

```bash
pytest tests/test_lambda_function.py -v
```

## モックの方針

AWS SDK (`boto3`) には実際にはネットワーク越しにS3へアクセスしますが、テストでは通信させたくありません。
そのため `test_lambda_function.py` は、`lambda_function` を import する **前** に偽の `boto3` モジュールを
`sys.modules` に登録しています。これにより `lambda_function.py` 内の `import boto3` は本物ではなく偽物を掴みます。

各テストではさらに `patch.object(lambda_function.boto3, "client", ...)` で `boto3.client("s3")` の戻り値を
差し替え、`get_object` の返り値や例外を自由にコントロールしています。

## テストケースと検証対象の対応

`lambda_handler` には3つの分岐があり、それぞれに対応するテストがあります。

| lambda_function.py の分岐 | テスト関数 | 内容 |
|---|---|---|
| `bucket` / `key` が無い → 400 | `test_returns_400_when_bucket_or_key_missing` | `bucket`のみ欠落・`key`のみ欠落・両方欠落の3パターンで400が返ることを確認 |
| S3から正常に取得 → 200 | `test_returns_200_with_object_content` | `get_object` の戻り値をモックし、本文が正しくデコードされ200で返ることを確認。`get_object`が正しい引数で呼ばれたかも検証 |
| `get_object` が例外を送出 → 500 | `test_returns_500_when_connection_fails` | `get_object.side_effect` で接続エラーを再現し、500が返ることを確認 |

## テストを追加するとき

- `lambda_handler` に新しい分岐を足したら、上の対応表にも行を追加してください。
- S3以外の外部サービスを呼ぶようになった場合も、実際には接続せずモックで代替する方針を踏襲してください。
