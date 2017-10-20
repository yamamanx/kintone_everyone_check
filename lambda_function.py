import requests
import json
import os
import logging
import traceback
import base64
import boto3


def logger_level(level):
    if level == 'CRITICAL':
        return 50
    elif level == 'ERROR':
        return 40
    elif level == 'WARNING':
        return 30
    elif level == 'INFO':
        return 20
    elif level == 'DEBUG':
        return 10
    else:
        return 0


slack_url = os.environ['SLACK_URL']
log_level = os.environ.get('LOG_LEVEL', 'INFO')
channel = os.environ.get('CHANNEL', '#general')

logger = logging.getLogger()
logger.setLevel(logger_level(log_level))


def send_message(content, channel):
    payload_dic = {
        "text": content,
        "channel": channel,
    }
    logger.debug(payload_dic)
    response = requests.post(slack_url, data=json.dumps(payload_dic))
    logger.debug(response.text)


def lambda_handler(event, context):

    try:
        kintone_domain = os.environ['KINTONE_DOMAIN']
        kintone_id = os.environ['KINTONE_ID']
        kintone_password = os.environ['KINTONE_PASSWORD']

        lambda_name = os.environ['LAMBDA_NAME']

        headers = {
            'X-Cybozu-Authorization': base64.b64encode(
                '{id}:{password}'.format(
                    id=kintone_id,
                    password=kintone_password
                ).encode('utf-8')
            )
        }

        count = 0

        for i in range(0,100000,100):

            response = requests.get(
                'https://{domain}/k/v1/apps.json?offset={offset}'.format(
                    domain=kintone_domain,
                    offset=str(i)
                ),
                headers=headers
            )

            response_dict = json.loads(response.text)

            if len(response_dict['apps']) == 0:
                send_message(
                    'kintone app count:{count}'.format(
                        count=str(count)
                    ),
                    channel
                )
                return {'count': count}

            client_lambda = boto3.client("lambda")

            for app in response_dict['apps']:
                client_lambda.invoke(
                    FunctionName=lambda_name,
                    InvocationType="Event",
                    Payload=json.dumps(app)
                )

            count += len(response_dict['apps'])

    except Exception as e:
        send_message(traceback.format_exc(), channel)
        logger.error(traceback.format_exc())
        raise(traceback.format_exc())
