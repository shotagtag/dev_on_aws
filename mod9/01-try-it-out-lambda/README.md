# 🚀ラボの開発環境でLambdaを触ってみましょう

### 準備

1. **ラボ4**環境のマネジメントコンソールを開きます(リージョンは変更しないでください。)

### Hello World するシンプルな Lambda 関数をマネジメントコンソールで作成してみよう

1. マネジメントコンソールから Lambda 関数を作成

    - 関数名は `dictate-function` を入力(処理内容と関数名の一貫性がありませんが、ラボ権限の関係です。ご了承ください)
    - Python 3.9 を選択
    - 実行ロールに `lambdaPollyRole` を使用します
    - ラボ環境の都合上、指定しないと進めないため指定します

2. Lambda 関数のコードに以下のソースコードを転記

```python
import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        })
    }
```

3. `Deploy` ボタンでソースコードをデプロイします

4. 上部のテストタブをクリックし、`テスト` ボタンで Lambda 関数を実行します
      - テストが完了すると、結果が出力されます

----

### Lambda 関数をマネジメントコンソールで作成してみよう

1. マネジメントコンソールから Lambda 関数を作成

    - 関数名は `search-function` を入力(処理内容と関数名の一貫性がありませんが、ラボ権限の関係です。ご了承ください)
    - Python 3.9 を選択
    - 実行ロールは既存の `lambdaPollyRole`  ロールを選択
      - ラボでも `lambdaPollyRole` を使用します。どんな権限がついているか確認しておきましょう

2. Lambda 関数のコードに以下のソースコードを転記

```python
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamoDBResource = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    # Log debug information
    print(event)
    
#    UserId = event["UserId"]
    UserId = "testuser"
    # ddbTable = os.environ['TABLE_NAME']
    ddbTable = "Notes"
    
    table = dynamoDBResource.Table(ddbTable)
    records = table.query(KeyConditionExpression=Key('UserId').eq(UserId))
    
    return records
```

3. `Deploy` ボタンでソースコードをデプロイします

4. `Test` ボタンで Lambda 関数を実行します

    - 最初は新しいイベントを作成してください
    - イベント名は `mytest01` を入力
    - イベントJSONはそのままで大丈夫です
    - `保存` して、作成したイベントを指定してテストを実行してみましょう
    - `testuser` のデータが取得できれば成功です
      - DynamoDB の `Notes` テーブルの中身を確認してみましょう

5. Lambda 関数のソースコードを見ると `Notes` テーブルを検索する `UserId` がハードコーディングされています

    - `UserId` をイベントで渡せるようにしてみましょう
      - Lambda 関数のソースコードを編集します
        - `UserId = "testuser"` を削除します
        - `# UserId = event["UserId"]` のコメントを外します。(Python では `#` があるとその先はコメントになります)
      - 更新を反映するために `Deploy` します
    - `UserId` をテストイベントで渡してみましょう
      - `Test` ボタンの▼を押して、 `Configure test event` を開きます
      - イベント JSON に `{ "UserId": "testuser" }` を指定して保存、実行してみましょう
      - `UserId` をハードコーディングしなくてもOKになりました

6. Lambda 関数のソースコードを見ると `Notes` テーブル名がハードコーディングされています

    - テーブル名を環境変数を参照するようにしてみましょう
      - Lambda 関数の `コード` で
        - `ddbTable = "Notes"` を削除します
        - `# ddbTable = os.environ['TABLE_NAME']` のコメントを外します
      - 更新を反映するために `Deploy` します
    - `設定` → `環境変数` でテーブル名を設定してみましょう
      - `キー` : `TABLE_NAME`
      - `値` : `Notes`
    - テストを実行してみましょう
