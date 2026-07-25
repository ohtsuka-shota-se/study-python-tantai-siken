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

計測エンジンは [`coverage`](https://coverage.readthedocs.io/) というパッケージで、以下の2通りの使い方があります。

- **方法A**: `coverage` コマンドで `pytest` をラップして実行する
- **方法B**: `pytest-cov`（`coverage` を使う pytest プラグイン）を使い、`pytest` コマンドに `--cov` オプションを足すだけで済ませる（おすすめ）

どちらも中身は同じ `coverage` エンジンなので結果は変わりません。`pytest-cov` の方がコマンドが短く、
`--cov=lambda_function` で計測対象を指定できて `tests/` 自身のカバレッジが結果に混ざらないぶん見やすいため、
迷ったら方法Bで問題ありません。

### 方法A: `coverage` コマンドを使う

#### 1. `coverage` パッケージをインストールする

`requirements.txt` には含まれていない（開発時にだけ使うツールのため）ので、仮想環境を有効化した状態で
個別にインストールします。

```bash
pip install coverage
```

#### 2. カバレッジ計測付きでテストを実行する

```bash
python -m coverage run -m pytest tests/test_lambda_function.py -v
```

`pytest` を直接呼ぶ代わりに `python -m coverage run -m pytest ...` とすることで、テスト実行中に
どの行が通ったかを裏で記録します（同じフォルダに `.coverage` という記録用ファイルが作られます。
Gitの追跡対象外です）。

#### 3. 結果をレポート表示する

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

### 方法B: `pytest-cov` を使う（おすすめ）

#### 1. `pytest-cov` パッケージをインストールする

こちらも `requirements.txt` には含まれていないので、仮想環境を有効化した状態で個別にインストールします。
（内部で `coverage` に依存しているため、`coverage` も一緒にインストールされます）

```bash
pip install pytest-cov
```

#### 2. `--cov` オプション付きで `pytest` を実行する

```bash
pytest tests/test_lambda_function.py --cov=lambda_function --cov-report=term-missing -v
```

`--cov=lambda_function` で「カバレッジを見たいモジュール」を指定します。省略すると `tests/` 自身も
含めた全体が対象になり、結果が見づらくなるので基本的には指定してください。
`--cov-report=term-missing` を付けると、方法Aと同じく未実行行がターミナルに表示されます。

出力例:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
lambda_function.py      13      0   100%
--------------------------------------------------
TOTAL                   13      0   100%
```

`coverage report -m` を別途叩く必要がなく、`pytest` の実行結果とカバレッジがまとめて出るのが方法Aとの違いです。

### HTML形式で見たい場合（任意）

行単位で色分けされたレポートをブラウザで見たい場合は以下のコマンドで `htmlcov/index.html` が生成されます。

```bash
python -m coverage html
```
