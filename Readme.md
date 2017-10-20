## kintoneでEveryoneに権限が設定されているアプリをAWS Lambdaで一括チェックする

AWS Lambda Python 3.6で動作します。

## 環境変数

* SLACK_URL : SLACKのWebhook URL
* CHANNEL : SLACKのチャンネル
* KINTONE_ID : kintoneの管理者ID
* KINTONE_PASSWORD : kintoneの管理者パスワード
* KINTONE_DOMAIN : kintoneのドメイン(xxx.cybozu.comまで全部)
* LOG_LEVEL : INFOとかDEBUGとか
* LAMBDA_NAME : アプリ一覧を取得する方のLambdaのみに設定、実処理をするLambdaの名前

## モジュール

```
pip install requests -t .
```

zipで一緒にかためてLambdaにアップロードしてください。

## Lambda

トリガーとなるLambdaはlambda_function.lambda_handler,
実処理をするLambdaにはlambda_worker.lambda_handlerを設定してください。


詳細は[kintoneでEveryoneに権限が設定されているアプリをAWS Lambdaで一括チェックする](https://www.yamamanx.com/kintone-everyone-aws-lambda/)をご参照ください。