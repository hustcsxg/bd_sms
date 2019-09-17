# 一.环境说明
## 1. python版本

python 2.7 

## 2. 安装依赖包
a. 安装xlrd模块 pip install xlrd

b. 安装百度云smssdk  

    安装指导：https://cloud.baidu.com/doc/SMS/s/2jwvxrnpm/
    安装步骤
    1. 在[官方网站](!https://cloud.baidu.com/doc/Developer/index.html)下载Python SDK工具包。
    
    2. 解压后，进入下载目录。
    
    3. 在脚本文件中添加以下代码，即可以使用SDK包：
    
    4. python setup.py install

## 3. 使用说明
sender.py 短信发送模块
sms_conf.py SMS配置信息
to_be_send_msg.py 待发送短信信息

步骤：
1. 配置sms_conf中的ak, sk
2. receivers.xls 第一列写入待发送人手机号
3. 修改to_be_send_msg中的 签名id, 模板id及模板参数

4.运行发送代码 python sender.py

