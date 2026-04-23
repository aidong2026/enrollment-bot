from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

STUDENTS = ['张三', '李四', '王五']
enrollment_list = []

def extract_student_name(nickname):
    suffixes = ['妈妈', '爸爸', '家长', '妈', '爸']
    for suffix in suffixes:
        if nickname.endswith(suffix):
            return nickname[:-len(suffix)]
    return None

@app.route('/wechat', methods=['GET', 'POST'])
def wechat_callback():
    if request.method == 'GET':
        return request.args.get('echostr', '')
    elif request.method == 'POST':
        try:
            xml_data = request.data.decode('utf-8')
            root = ET.fromstring(xml_data)
            content = root.find('Content').text if root.find('Content') is not None else ''
            from_user = root.find('FromUserName').text if root.find('FromUserName') is not None else ''
            
            sender_name = from_user
            
            if content.strip() == '1':
                student_name = extract_student_name(sender_name)
                if student_name:
                    if student_name not in enrollment_list:
                        enrollment_list.append(student_name)
                        reply = f"报名成功！学员：{student_name}"
                    else:
                        reply = f"{student_name} 已报名"
                else:
                    reply = "无法识别您的昵称"
            elif content.strip() == '2':
                student_name = extract_student_name(sender_name)
                if student_name and student_name in enrollment_list:
                    enrollment_list.remove(student_name)
                    reply = f"已取消：{student_name}"
                else:
                    reply = "您还未报名"
            else:
                reply = "回复1=报名，回复2=取消"
            
            return f'<xml><ToUserName><![CDATA[{from_user}]]></ToUserName><FromUserName><![CDATA[bot]]></FromUserName><CreateTime>0</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{reply}]]></Content></xml>'
        except Exception as e:
            return 'success'

@app.route('/')
def index():
    return '接龙机器人运行中'
