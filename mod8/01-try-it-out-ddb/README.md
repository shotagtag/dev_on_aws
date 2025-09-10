# 🚀ラボの開発環境でDynamoDBを触ってみましょう

適宜マネジメントコンソールでDynamoDBの画面も確認しつつ進めると理解が深まっておすすめです👍

### 準備

1. **ラボ3**環境のvscode serverにログインします。手順書の「LabWorkspaceURL」を確認し、ブラウザでアクセスしましょう。
[参考](https://github.com/shotagtag/dev_on_aws/tree/main/mod3/01-try-it-out-awstools#%E3%83%A9%E3%83%9C1%E7%92%B0%E5%A2%83%E3%81%A7-vscode-server-%E3%81%AB%E6%8E%A5%E7%B6%9A%E3%81%97%E3%81%BE%E3%81%97%E3%82%87%E3%81%86)

1. サンプルコードを取得し、ディレクトリに移動します。
```
git clone https://github.com/shotagtag/dev_on_aws
cd dev_on_aws/mod8/01-try-it-out-ddb/
```

### Table作成

* 作成するテーブル定義ファイルを確認します。
  * テーブル名 : "Demo-Music"
  * プライマリキーは複合キーとして以下を設定
    * パーティションキー: `Singer`
    * ソートキー: `Title`
  * スループットモードは「プロビジョニングモード」
  * ローカルセカンダリインデックスを作成
    * パーティションキー : `Singer`
    * ソートキー : `ReleaseDate`

```
cat create_table.json
```

* テーブルを作成します。作成結果は「q」キーを押すと閉じることができます。

```shell
aws dynamodb create-table \
--cli-input-json file://create_table.json
```

### テストデータ投入

* put-itemを使用して4件の項目を作成します。
  
```shell
# 1件目
aws dynamodb put-item \
--table-name Demo-Music \
--item '{"Singer": {"S": "John"}, "Title": {"S": "ABC"}}'

# 2件目
aws dynamodb put-item \
--table-name Demo-Music \
--item '{"Singer": {"S": "John"}, "Title": {"S": "XYZ"}, "ReleaseDate": {"S": "20220610"}}'

# 3件目
aws dynamodb put-item \
--table-name Demo-Music \
--item '{"Singer": {"S": "Marry"}, "Title": {"S": "Hi"}}'

# 4件目
aws dynamodb put-item \
--table-name Demo-Music \
--item '{"Singer": {"S": "Bob"}, "Title": {"S": "Hello"}, "ReleaseDate": {"S": "20220610"}}'
```

次のデータが登録されていることを意識しておいてください。

| Singer | Title | ReleaseDate |
|--------|-------|-------------|
| John   | ABC   | -           |
| John   | XYZ   | 20220610    |
| Marry  | Hi    | -           |
| Bob    | Hello | 20220610    |


* プライマリキーが2件目のデータと重複している項目を登録してみましょう。エラーになることが確認できます。
```
aws dynamodb put-item \
--table-name Demo-Music \
--item '{"Singer": {"S": "John"}, "Title": {"S": "XYZ"}, "ReleaseDate": {"S": "20250910"}}'
```

### データ取得

* GetItemはキーを指定して項目を取得するオペレーションです。

```shell
aws dynamodb get-item --table-name Demo-Music \
--key '{"Singer": {"S": "John"}, "Title": {"S": "XYZ"}}' \
--return-consumed-capacity TOTAL
```

### データ確認(Scan)

* Scanはテーブルから全ての項目を取得するオペレーションです。

```shell
aws dynamodb scan \
--table-name Demo-Music \
```

### データ検索(Query)

* Queryはテーブルから項目を検索するオペレーションです。シンプルな検索を行ってみましょう。
  1. Demo-Music テーブルのパーティションキー`Singer`が`John`に一致する項目を検索しています。
  1. `key-condition-expression`で Singerが:v1と等しい、という条件を指定しています。`:v1`はプレースホルダー(仮の名前、値のようなもの)です。
  1. `expression-attribute-values`で プレースホルダー`:v1`の実際の値を指定します。この例ではString型の`John`を指定しています。

```shell
aws dynamodb query \
--table-name Demo-Music \
--key-condition-expression "Singer = :v1" \
--expression-attribute-values '{":v1": {"S": "John"}}' \
```

* 先ほどと同じくQueryを使っていますが、ソートキー`Title`の検索条件を追加し、さらに柔軟に指定しています。
  * `Singer = John`の曲のうち、タイトルが"A"で始まるものだけが返されます。
    1. `key-condition-expression`で `Singerが:v1と等しい かつ Titleが :v2 ではじまる` という条件を指定しています。
    1. `expression-attribute-values`で プレースホルダー`:v1`と`v2`の実際の値を指定します。

```
aws dynamodb query \
--table-name Demo-Music \
--key-condition-expression "Singer = :v1 AND begins_with(Title, :v2)" \
--expression-attribute-values '{
    ":v1": {"S": "John"},
    ":v2": {"S": "A"}
}'
```

* Queryで件数(Count)のみ取得することもできます。

```shell
aws dynamodb query \
--select COUNT \
--table-name Demo-Music \
--key-condition-expression "Singer = :v1" \
--expression-attribute-values '{":v1": {"S": "John"}}' \
```

### データ追加・更新(UpdateItem)

* UpdateItemは項目の更新に使用します。同一のパーティションキー＆ソートキーが存在しない場合は追加されます。
  1. `Singer="Bob", Title="Hello"`の項目の`ReleaseDate`を"20250101"に更新します。
  1. `update-expression` で実行したい更新操作を指定します。`SET`は属性の追加または更新を行う指定です。`SET ReleaseDate`とあるので、ReleaseDateを :newval(プレースホルダー)で更新
  1. `expression-attribute-values` で実際に更新する値を指定します。
  1. `return-values ALL_NEW` は更新後の全ての値を返す。という意味です。他にも更新された値だけを返す`UPDATED_NEW`などがあります。

```shell
aws dynamodb update-item --table-name Demo-Music \
--key '{"Singer": {"S": "Bob"}, "Title": {"S": "Hello"}}' \
--update-expression "SET ReleaseDate = :newval" \
--expression-attribute-values '{":newval":{"S": "20250101"}}' \
--return-values ALL_NEW
```

### データ削除(DeleteItem)

* DeleteItemは項目の削除を行うオペレーションです。

```shell
aws dynamodb delete-item \
--table-name Demo-Music \
--key '{"Singer": {"S": "Yan"}, "Title": {"S": "Super"}}'
```

### データ取得(GetItem:強い整合性)

1. DynamoDBの読み込みはデフォルトで結果整合性です。そのため最近完了した書き込みの結果が応答に反映されない場合があります。強い整合性の読み取り(--consistent-read)を行うことで確実に更新を反映した結果を受け取ることができます。ただし結果整合性よりも高コストなので必要に応じて使用します。

```shell
aws dynamodb get-item --table-name Demo-Music \
--key '{"Singer": {"S": "John"}, "Title": {"S": "XYZ"}}' \
--consistent-read \
--return-consumed-capacity TOTAL
```

### Table削除
```shell
aws dynamodb delete-table \
--table-name Demo-Music
```
