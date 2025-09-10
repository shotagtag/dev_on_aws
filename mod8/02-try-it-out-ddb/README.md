# 🚀SDKでDynamoDBを触ってみましょう

適宜マネジメントコンソールでDynamoDBの画面も確認しつつ進めると理解が深まっておすすめです👍

### 準備

1. **ラボ3**環境のvscode serverにログインします。手順書の「LabWorkspaceURL」を確認し、ブラウザでアクセスしましょう。
[参考](https://github.com/shotagtag/dev_on_aws/tree/main/mod3/01-try-it-out-awstools#%E3%83%A9%E3%83%9C1%E7%92%B0%E5%A2%83%E3%81%A7-vscode-server-%E3%81%AB%E6%8E%A5%E7%B6%9A%E3%81%97%E3%81%BE%E3%81%97%E3%82%87%E3%81%86)

1. サンプルコードを取得し、ディレクトリに移動します。
```
git clone https://github.com/shotagtag/dev_on_aws
cd dev_on_aws/mod8/02-try-it-out-ddb/
```

### テーブル作成

```shell
python create_table.py
```

下記のエラーが発生した場合は

```
Traceback (most recent call last):
  File "create_table.py", line 2, in <module>
    import boto3
ModuleNotFoundError: No module named 'boto3'
```

こちらのコマンドを実行して boto3 をインストールしてください

```shell
python3 -m pip install boto3
```

### データ登録

```shell
python put_item.py
```

### GetItemで1件取得

```shell
python get_item.py
```

### Scanしてデータを全取得

```shell
python scan.py
```

### Queryで条件を指定してデータを取得

```shell
python query.py
```

### Scanしてデータをページングで取得

```shell
python pagenate.py
```

### データ追加・更新・条件付き更新

```shell
python update_item.py
```


### テーブル削除

```shell
python delete_table.py
```

### Documentation

[Boto3 Docs for DynamoDB](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)
