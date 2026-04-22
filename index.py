{\rtf1\ansi\ansicpg936\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # \uc0\u20225 \u19994 \u24494 \u20449 \u32676 \u25509 \u40857 \u26426 \u22120 \u20154 \
from flask import Flask, request\
import hashlib\
import xml.etree.ElementTree as ET\
import os\
\
app = Flask(__name__)\
\
STUDENTS = ['\uc0\u24352 \u19977 ', '\u26446 \u22235 ', '\u29579 \u20116 ']\
enrollment_list = []\
\
def extract_student_name(nickname):\
    suffixes = ['\uc0\u22920 \u22920 ', '\u29240 \u29240 ', '\u23478 \u38271 ', '\u22920 ', '\u29240 ']\
    for suffix in suffixes:\
        if nickname.endswith(suffix):\
            return nickname[:-len(suffix)]\
    return None\
\
@app.route('/wechat', methods=['GET', 'POST'])\
def wechat_callback():\
    if request.method == 'GET':\
        return request.args.get('echostr', '')\
    elif request.method == 'POST':\
        try:\
            xml_data = request.data.decode('utf-8')\
            root = ET.fromstring(xml_data)\
            content = root.find('Content').text if root.find('Content') is not None else ''\
            from_user = root.find('FromUserName').text if root.find('FromUserName') is not None else ''\
            sender_name = from_user\
            \
            if content.strip() == '1':\
                student_name = extract_student_name(sender_name)\
                if student_name:\
                    if student_name not in enrollment_list:\
                        enrollment_list.append(student_name)\
                        reply = f"\uc0\u25509 \u40857 \u25104 \u21151 \u65281 \u23398 \u21592 \u65306 \{student_name\}"\
                    else:\
                        reply = f"\{student_name\} \uc0\u24050 \u25253 \u21517 "\
                else:\
                    reply = "\uc0\u26080 \u27861 \u35782 \u21035 "\
            elif content.strip() == '2':\
                student_name = extract_student_name(sender_name)\
                if student_name and student_name in enrollment_list:\
                    enrollment_list.remove(student_name)\
                    reply = f"\uc0\u24050 \u21462 \u28040 \u65306 \{student_name\}"\
                else:\
                    reply = "\uc0\u24744 \u36824 \u26410 \u25253 \u21517 "\
            else:\
                reply = "\uc0\u22238 \u22797 1=\u25253 \u21517 \u65292 \u22238 \u22797 2=\u21462 \u28040 "\
            \
            return f'<xml><ToUserName><![CDATA[\{from_user\}]]></ToUserName><FromUserName><![CDATA[bot]]></FromUserName><CreateTime>0</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[\{reply\}]]></Content></xml>'\
        except:\
            return 'success'\
\
@app.route('/')\
def index():\
    return '\uc0\u25509 \u40857 \u26426 \u22120 \u20154 \u36816 \u34892 \u20013 '\
\
if __name__ == '__main__':\
    app.run(host='0.0.0.0', port=5000)}