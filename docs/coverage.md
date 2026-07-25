# カバレッジ（コードカバレッジ）とは

## 概念

**カバレッジ**とは、テストを実行したときに「ソースコードの行のうち何%が実際に実行されたか」を表す指標です。

- 100%に近いほど「テストで通っていないコード（=バグが潜んでいても気づけない箇所）」が少ないことを意味します。
- ただし100%であっても「実行はされたが、想定外の入力に対する検証まではしていない」というケースはあり得るため、
  カバレッジは**テストの網羅性の目安**であって、テストの質そのものを保証するものではありません。

このリポジトリの `lambda_function.py` の場合、`lambda_handler` には

1. `bucket`/`key` が無い → 400
2. S3から正常に取得 → 200
3. `get_object` が例外を送出 → 500

の3つの分岐があり（[`tests/README.md`](../tests/README.md) の対応表を参照）、これに対応する3つのテストが
`tests/test_lambda_function.py` にあります。3分岐すべてを通るテストがあるため、`lambda_function.py` は
カバレッジ100%になります。

## 確認方法

### 1. `coverage` パッケージをインストールする

`requirements.txt` には含まれていない（開発時にだけ使うツールのため）ので、仮想環境を有効化した状態で
個別にインストールします。

```bash
pip install coverage
```

### 2. カバレッジ計測付きでテストを実行する

```bash
python -m coverage run -m pytest tests/test_lambda_function.py -v
```

`pytest` を直接呼ぶ代わりに `python -m coverage run -m pytest ...` とすることで、テスト実行中に
どの行が通ったかを裏で記録します（同じフォルダに `.coverage` という記録用ファイルが作られます。
Gitの追跡対象外です）。

### 3. 結果をレポート表示する

```bash
python -m coverage report -m
```

出力例:

```
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
lambda_function.py                 13      0   100%
tests\test_lambda_function.py      31      0   100%
-------------------------------------------------------------
TOTAL                              44      0   100%
```

| 列 | 意味 |
|---|---|
| `Stmts` | そのファイルの実行可能な行数 |
| `Miss` | 一度も実行されなかった行数 |
| `Cover` | カバレッジ率（`(Stmts - Miss) / Stmts`） |
| `Missing` | 未実行の行番号（`Miss` が0でない場合に表示される） |

`lambda_function.py` に分岐を追加したのに `Missing` に行番号が出た場合は、その分岐を通すテストが
まだ無いということなので、[`tests/README.md`](../tests/README.md) の対応表に沿ってテストを追加してください。

### HTML形式で見たい場合（任意）

行単位で色分けされたレポートをブラウザで見たい場合は以下のコマンドで `htmlcov/index.html` が生成されます。

```bash
python -m coverage html
```
