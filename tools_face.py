import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
import base64
import json


'''
PyQt5有5种布局方式，分别是绝对布局、水平布局、垂直布局、网格布局、表单布局
本程序只采用网格布局。
'''

header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        }

#4.获取调用接口所需的Access Token
def get_access_token():
    client_id = 'Bq3IaXG2RpOq4WNHAEHa0oW1' #API Key
    client_secret = 'PfWjbNsUX7IboDXDGY2t5LaW9soUVejX' #Secret Key
    url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
        'client_id={0}&client_secret={1}'.format(client_id,client_secret)
    data=requests.get(url, headers=header)
    access_token=json.loads(data.text)['access_token']
    return access_token

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("颜值识别工具")
        self.setWindowIcon(QIcon('图标.jpg'))#再为该窗口添加标题和图标
        self.layout = QGridLayout()
        self.setLayout(self.layout)  # 局部布局

        #1、用QTextBrowser创建选择图片、浏览标签，分别设置大小。
        self.fileText = QTextBrowser()
        self.fileText.setText('请选择图片路径')
        self.fileText.setFixedSize(110, 25)
        self.layout.addWidget(self.fileText, 0, 0, Qt.AlignCenter)#addWidget函数，4个参数分别代表放置内容、放置行数、放置的列数、放的位置。

        self.pathText = QLineEdit(self)
        self.pathText.setFixedSize(210, 25)
        self.layout.addWidget(self.pathText, 0, 1, Qt.AlignCenter)

        #1、用QpushButton创建浏览、开始分析按钮，并绑定setBrowerPath和start函数
        self.pathPushButton = QPushButton("浏览")
        self.pathPushButton.setFixedSize(60, 40)
        self.pathPushButton.clicked.connect(self.setBrowerPath)
        self.layout.addWidget(self.pathPushButton, 0, 2, Qt.AlignCenter)


        self.startPushButton = QPushButton("开始识别")
        self.startPushButton.setFixedSize(60, 40)
        self.startPushButton.clicked.connect(self.start)
        self.layout.addWidget(self.startPushButton, 1, 1, Qt.AlignCenter)

        #2、放置性别、年龄、颜值标签，分别放置在第4，5，6行的1和2列位置
        self.genderText = QTextBrowser()
        self.genderText.setText('性别')
        self.genderText.setFixedSize(60, 25)
        self.layout.addWidget(self.genderText, 3, 0)

        self.genderLine = QLineEdit(self)
        self.genderLine.setFixedSize(60, 25)
        self.layout.addWidget(self.genderLine, 3, 1)

        self.ageText = QTextBrowser()
        self.ageText.setText('年龄')
        self.ageText.setFixedSize(60, 25)
        self.layout.addWidget(self.ageText, 4, 0)

        self.ageLine = QLineEdit(self)
        self.ageLine.setFixedSize(60, 25)
        self.layout.addWidget(self.ageLine, 4, 1)

        self.beautyText = QTextBrowser()
        self.beautyText.setText('颜值')
        self.beautyText.setFixedSize(60, 25)
        self.layout.addWidget(self.beautyText, 5, 0)

        self.beautyLine = QLineEdit(self)
        self.beautyLine.setFixedSize(60, 25)
        self.layout.addWidget(self.beautyLine, 5, 1)

    #绑定“浏览”、“开始分析”信号槽
    def setBrowerPath(self):
        dig=QFileDialog() #首先是绑定“浏览”信号，先实例化QfileDialoog
        dig.setFileMode(QFileDialog.AnyFile)  # 设置可以打开任何文件
        dig.setFilter(QDir.Files) # 文件过滤
        if dig.exec_():
            # 接受选中文件的路径，默认为列表
            filenames = dig.selectedFiles()
            self.picfile=filenames[0]
            self.pathText.setText(self.picfile)
            # 列表中的第一个元素即是文件路径，以只读的方式打开文件
    
    def start(self):
        print(11111)
        with open('{0}'.format(self.picfile), 'rb') as f:#5.打开图片路径，并转换成BASE64格式
            base = base64.b64encode(f.read())
            img = str(base, encoding='utf-8')
        params = {#构造识图请求参数，获得返回结果
            'image': img, #img是图片信息
            'image_type': 'BASE64', #image_type是图片格式
            'face_field': 'age,beauty,gender,face_type,face_shape,expression,landmark' #face_field是返回的识别信息，包括年龄、颜值、性别等信息，
                                                                                        #我们只取颜值、性别、年龄3类信息
        }

        url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={0}'.format(get_access_token())
        results = requests.post(url, data=params, headers=header)
        results = json.loads(results.text)

        if results['error_msg'] == "SUCCESS":
            self.beauty = results['result']['face_list'][0]['beauty']
            self.gender = results['result']['face_list'][0]['gender']['type']
            self.age = results['result']['face_list'][0]['age']
            print(self.beauty, self.gender, self.age)
            if self.gender=='male':
                self.gender='男'
            elif self.gender=='female':
                self.gender='女'
            self.genderLine.setText(self.gender) #将返回结果放入上述文本显示框内
            self.ageLine.setText(str(self.age))
            self.beautyLine.setText(str(self.beauty))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
app = QApplication(sys.argv)#创建应用程序对象，参数sys.argv是命令行参数
show = Window()  # 主窗口的类，window（）是识别工具的类，窗口大小500*200
show.setFixedSize(500, 200)
show.show()
sys.exit(app.exec_())#进入消息循环等待退出
