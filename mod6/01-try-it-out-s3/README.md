# 🚀ラボの開発環境でS3を触ってみましょう

適宜マネジメントコンソールでS3の画面も確認しつつ進めると理解が深まっておすすめです👍

**ラボ2**環境のvscode serverにログインします。
[参考](https://github.com/shotagtag/dev_on_aws/tree/main/mod3/01-try-it-out-awstools#%E3%83%A9%E3%83%9C1%E7%92%B0%E5%A2%83%E3%81%A7-vscode-server-%E3%81%AB%E6%8E%A5%E7%B6%9A%E3%81%97%E3%81%BE%E3%81%97%E3%82%87%E3%81%86)

### 参考ドキュメント：S3 api

[AWS CLI での高レベル (S3) コマンドの使用 - AWS Command Line Interface](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-services-s3-commands.html)

[AWS CLI での API レベル (s3api) コマンドの使用 - AWS Command Line Interface](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-services-s3-apicommands.html)

### 準備

1. サンプルコードを取得し、ディレクトリに移動します。
```
git clone https://github.com/shotagtag/dev_on_aws
cd dev_on_aws/mod6/01-try-it-out-s3/
```

### リージョンを取得

```shell
REGION=`aws configure get region`
echo $REGION
```

## s3コマンド(高レベルAPI)

最小限の結果がよしなに返却されます

どんなコマンドがあるかはhelpコマンドを実行してみましょう。マニュアルページが開きます。「q」キーを押すと、マニュアルページを閉じることができます。

```shell
aws s3 help
```

### S3バケット一覧を取得

```shell
aws s3 ls
```

### S3バケットを作成

好きなバケット名を設定します。このとき下記に注意してください

- 全てのAWSアカウントで一つしか無い名前であること
- 全て小文字であること

※下記の「被らなそうな適当な文字列」箇所をご自身で変更して好きなバケット名へ変更しましょう。`notes-bucket-minilab`は消さないでください。

```shell
BUCKET_NAME=notes-bucket-minilab-被らなそうな適当な文字列
```

mb(make bucket)コマンドでバケットを作成します

```shell
aws s3 mb s3://$BUCKET_NAME --region $REGION
```

### S3バケットへアップロード

準備で `git clone` 済みの画像データをS3バケットへアップロードします

```shell
aws s3 cp ~/environment/dev_on_aws/mod6/01-try-it-out-s3/AWS.jpg s3://$BUCKET_NAME
```

### S3バケットからダウンロード

同じcpコマンドですが引数の順序が異なります、AWS-2.jpgという名前でサーバー上にダウンロードします。

```shell
aws s3 cp s3://$BUCKET_NAME/AWS.jpg ~/environment/dev_on_aws/mod6/01-try-it-out-s3/AWS-2.jpg
```

### S3へアップロード(マルチパートアップロード)

高レベルコマンドのためcpコマンドでもよしなにマルチアップロードしてくれます

```shell
dd if=/dev/zero of=50MB.dummy bs=1M count=50 # 50MBのダミーファイル作成
aws s3 cp 50MB.dummy s3://$BUCKET_NAME --debug
```

### S3へsyncで一括アップロード

dataフォルダをまるごとアップロードしています。

```shell
aws s3 sync ~/environment/dev_on_aws/mod6/01-try-it-out-s3/data/ s3://$BUCKET_NAME/data/
```

### 静的Webサイトホスティング

静的Webサイトホスティング設定の有効化します。

```shell
aws s3 website s3://$BUCKET_NAME --index-document index.html --error-document error.html
```

静的Webサイトの資材が入ったフォルダをアップロードします

```shell
aws s3 sync ~/environment/dev_on_aws/mod6/01-try-it-out-s3/sample-site/ s3://$BUCKET_NAME
```

公開ウェブサイトに必要なバケットポリシーを設定します。しかし、ブロックパブリックアクセスが有効化されているため、このままではバケットを公開するためのバケットポリシーを設定しようとしても拒否されてしまいます。そこでブロックパブリックアクセスを無効化します。

```
aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration "BlockPublicPolicy=false,RestrictPublicBuckets=
false"
```

バケットポリシーを設定

```shell
sed -i "s/\[BUCKET\]/$BUCKET_NAME/" ~/environment/dev_on_aws/mod6/01-try-it-out-s3/policy.json 
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://~/environment/dev_on_aws/mod6/01-try-it-out-s3/policy.json 
```

静的WebサイトホスティングのURLを出力してアクセス

```shell
echo http://$BUCKET_NAME.s3-website.$REGION.amazonaws.com/
```

## s3apiコマンド(低レベルコマンド)

低レベルコマンドなのでレスポンスがそのまま返却されます

どんなコマンドがあるかはhelpコマンドを実行してみましょう

```shell
aws s3api help
```

### S3バケット一覧を取得

低レベルコマンドのレスポンスがどのような内容か確認します

```shell
aws s3api list-buckets
```

これだと使いづらいのでqueryオプションでフィルタリングします

```shell
aws s3api list-buckets --query 'Buckets[].Name'
```

### S3バケットを作成

```shell
aws s3api create-bucket --bucket ${BUCKET_NAME}-s3api --region $REGION --create-bucket-configuration LocationConstraint=$REGION
```

### S3バケットへアップロード

```shell
aws s3api put-object --bucket ${BUCKET_NAME}-s3api --key AWS.jpg --body ~/environment/dev_on_aws/mod6/01-try-it-out-s3/AWS.jpg
```

### S3バケットからダウンロード

--bodyオプションが無いことに注意

```shell
aws s3api get-object --bucket ${BUCKET_NAME}-s3api --key AWS.jpg ~/environment/dev_on_aws/mod6/01-try-it-out-s3/s3api-download_AWS.jpg
```

### S3へアップロード(マルチパートアップロード)

低コマンドAPIのため自分たちでマルチパートアップロードの開始や、何を送信するかなど完全に制御する必要があります

* 50MBのダミーファイル作成
```shell
dd if=/dev/zero of=50MB.dummy bs=1M count=50
```

* 20MB単位で3つのファイルに分割
```
split -b 20MB 50MB.dummy -d
```

* マルチパートアップロード開始
```
aws s3api create-multipart-upload --bucket ${BUCKET_NAME}-s3api --key 50MB_s3api.dummy
```

* 返却されるUploadIdを控えておきます
```
UPLOAD_ID=${返却されたUploadId}
```

* splitした各ファイルを各パートとして送信

パート1の送信
```
aws s3api upload-part --bucket ${BUCKET_NAME}-s3api --key 50MB_s3api.dummy --part-number 1 --body x00 --upload-id ${UPLOAD_ID}
```
パート2の送信
```
aws s3api upload-part --bucket ${BUCKET_NAME}-s3api --key 50MB_s3api.dummy --part-number 2 --body x01 --upload-id ${UPLOAD_ID}
```
パート3の送信
```
aws s3api upload-part --bucket ${BUCKET_NAME}-s3api --key 50MB_s3api.dummy --part-number 3 --body x02 --upload-id ${UPLOAD_ID}
```

* 各パートを送信したときに返却されるETagを情報として `environment/dev_on_aws/mod6/01-try-it-out-s3/part.json` の xxxxxxx に反映し、マルチパートアップロードの完了指示ファイルを完成させる(viやvscodeの編集機能を使ってください)

part.json 完成サンプル(バッククォートに注意！)

```json
{
  "Parts": [
    {
      "ETag": "\"10e4462c9d0b08e7f0b304c4fbfeafa3\"",
      "PartNumber": 1
    },
    {
      "ETag": "\"10e4462c9d0b08e7f0b304c4fbfeafa3\"",
      "PartNumber": 2
    },
    {
      "ETag": "\"c77168e1fe31a482eb8dfdaae061e846\"",
      "PartNumber": 3
    }
  ]
}
```

* マルチパートアップロードの完了指示を行い、S3側でpartファイルを結合します。
```
aws s3api complete-multipart-upload --bucket ${BUCKET_NAME}-s3api --key 50MB_s3api.dummy --upload-id ${UPLOAD_ID} --multipart-upload file://~/environment/dev_on_aws/mod6/01-try-it-out-s3/part.json 
```

