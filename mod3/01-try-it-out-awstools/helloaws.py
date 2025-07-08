# boto3 ライブラリ(python用のAWS SDK)をインポート
import boto3

# S3クライアントを作成
s3_client = boto3.client('s3')

# S3バケット一覧を取得
response = s3_client.list_buckets()

# バケット名を1行ずつ出力
for bucket in response['Buckets']:
    print(bucket['Name'])