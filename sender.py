# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import xlrd
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import sms_conf
from to_be_send_msg import Msg as ToBeSendMsg
from to_be_send_msg import Receivers as DemoReceivers
from baidubce.services.sms import sms_client as sms
from baidubce import exception as ex

logging.basicConfig(level=logging.DEBUG, filename='./senders.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = sms_conf
ReceiverFile = "./receivers.xls"
# 最大线程数
MAX_THREAD_WORKER = 100

# 每多少人一组
SplitNum = 20


def send_msg(receiver, msg_info, sms_client=None):
    """
    给某人发送带有签名的短信
    :param receiver: 18009090101
    :param msg_info: {"invoke_id":"签名id", "template_id":"短信模板id"，"content_var": "短信模板参数“}
    :param sms_client:
    :return:
    """
    request_id = None
    try:
        invoke_id = msg_info["invoke_id"]
        template_id = msg_info["template_id"]
        content_var = msg_info["content_var"]
    except Exception as e:
        LOG.error("send_msg传参错误,%s" % (str(e)))
        return request_id
    try:
        if sms_client is None:
            sms_client = sms.SmsClient(CONF.config)
        response = sms_client.send_message_2(invoke_id, template_id, receiver, content_var)
        request_id = response.request_id
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
    except Exception as e:
        LOG.error(str(e))
    return request_id


def send_msg_to_group(receivers, msg_info):
    """
    :param receivers: ['19098988778', '18978988767']
    :param msg_info: {"invoke_id":"签名id", "template_id":"短信模板id"，"content_var": "短信模板参数“}
    :return:
    """
    receivers = list(set(receivers))
    sms_client = sms.SmsClient(CONF.config)
    for phone in receivers:
        _ret = send_msg(phone, msg_info, sms_client)
        _success, _request_id = ('success', _ret) if _ret else ('failed', 0)
        _log_msg = "Send msg to %s,%s,requestId:%s" % (phone, _success, _request_id)
        LOG.info(_log_msg)


def exec_by_thread_pool(func, arg_list, max_worker=MAX_THREAD_WORKER):
    executor = ThreadPoolExecutor(max_workers=max_worker)
    all_task = [executor.submit(func, *i) for i in arg_list]
    for future in as_completed(all_task):
        data = future.result()


def split_receivers(users):
    split_num = SplitNum
    nums = len(users)
    ret = []
    for i in range(nums // split_num + 1):
        j = i * 20
        if j < nums:
            ret.append(users[j:j + 20])
    if len(ret) == 0:
        ret.append([])
    return ret


def send_msg_by_multi_thread(receivers, msg_info):
    user_list = split_receivers(receivers)
    exec_by_thread_pool(send_msg_to_group, [(i, msg_info) for i in user_list])


def get_receviers_from_xls(file_name):
    wb = xlrd.open_workbook(filename=file_name)
    sheet1 = wb.sheet_by_index(0)
    first_column = sheet1.col_values(0, 1)
    ret = [i if isinstance(i, str) else str(int(i)) for i in first_column]
    return ret


def test():
    """
    单线程给一组用户发送短信
    :return:
    """
    msg_info = ToBeSendMsg
    receivers = DemoReceivers
    send_msg_to_group(receivers, msg_info)


def test_multi_thread():
    """
    使用多线程给 一组用户发送短信
    :return:
    """
    msg_info = ToBeSendMsg
    receivers = DemoReceivers
    send_msg_by_multi_thread(receivers, msg_info)


def main():
    receviers = get_receviers_from_xls(ReceiverFile)
    msg_info = ToBeSendMsg
    send_msg_by_multi_thread(receviers, msg_info)


if __name__ == '__main__':
    main()
