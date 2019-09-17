#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

HOST = b'sms.bj.baidubce.com'
AK = b'c1ed72fc708d472fb9b56797bd699xxxx'
SK = b'2836e493fc1a455e8a60130e9050xx'

logger = logging.getLogger('baidubce.services.sms.smsclient')
fh = logging.FileHandler('sms_sender.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
