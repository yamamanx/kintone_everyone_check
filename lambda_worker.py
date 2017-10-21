# -*- coding: utf-8 -*-

import requests
import json
import os
import logging
import traceback
import base64


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
        logger.debug(event)

        kintone_domain = os.environ['KINTONE_DOMAIN']
        kintone_id = os.environ['KINTONE_ID']
        kintone_password = os.environ['KINTONE_PASSWORD']

        headers = {
            'X-Cybozu-Authorization': base64.b64encode(
                '{id}:{password}'.format(
                    id=kintone_id,
                    password=kintone_password
                ).encode('utf-8')
            )
        }

        response = requests.get(
            'https://{domain}/k/v1/app/acl.json?app={id}'.format(
                domain=kintone_domain,
                id=event['appId']
            ),
            headers=headers
        )
        logger.debug(response.text)

        message = []

        response_dict = json.loads(response.text)

        if 'rights' in response_dict:
            rights = response_dict['rights']
            for acl in rights:
                logger.debug(acl)
                if 'entity' in acl:
                    logger.debug(acl['entity'])
                    if acl['entity']['code'] == 'everyone':
                        logger.debug(acl['entity']['code'])
                        if acl['appEditable']:
                            message.append(u'管理者')
                        if acl['recordViewable']:
                            message.append(u'閲覧')
                        if acl['recordAddable']:
                            message.append(u'追加')
                        if acl['recordEditable']:
                            message.append(u'編集')
                        if acl['recordDeletable']:
                            message.append(u'削除')
                        if acl['recordImportable']:
                            message.append(u'読み出し')
                        if acl['recordExportable']:
                            message.append(u'書き出し')

                        logger.debug(message)

                        if len(message) > 0:
                            send_message(
                                u':fearful:Everyoneが有効なアプリがありました。\n{id}:{name}\n更新者:{modifier}\n{acl}'.format(
                                    id=event['appId'],
                                    name=event['name'],
                                    modifier=event['modifier']['name'],
                                    acl=','.join(message)
                                ),
                                channel
                            )

    except Exception as e:
        send_message(traceback.format_exc(), channel)
        logger.error(traceback.format_exc())
        raise(traceback.format_exc())
