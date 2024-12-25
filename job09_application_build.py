
import sys
import numpy as np
from tabnanny import format_witnesses
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from keras.models import load_model
from PIL import Image

# ui를 class로 만들어주는 것 = uic
form_window = uic.loadUiType('./mainWidget.ui')[0]

# Exam이란 클래스 생성, QWidget,
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()                          # super == 조상 클래스 / 조상클래스는 자손클래스의 첫줄에 있어야 한다.
        self.setupUi(self)
        self.path = ('E:/AISW/pyCh/Cat_and_Dog_classfication/datasets/test/doji.jpg',
                     'Image Files(*.jpg; *.png')    # 절대 경로는 Windows 시스템에서 \를 쓰는 걸 /로 변경한다.
        self.model = load_model('E:/AISW/pyCh/Cat_and_Dog_classfication/models-20241218T112011Z-001/models/cat_and_dog_binary_classfication_0.8583999872207642.h5')

        # 디자이너앱에서 이미지 스케일드 컨텐츠 옵션을 줌으로써
        # pixmap = QPixmap(self.path[0])              # pixmap으로 변경한다
        # self.lbl_image.setPixmap(pixmap)            # lbl 라벨에 Pixmap을 Set

        self.btn_select.clicked.connect(self.btn_clicked_slot)    # Qt = signal slot
        # 버튼 이름.버튼이 눌리면.실행해라(함수를)

    # Qt에서 제공되는게 아닌 Windows에서 제공되는 기능
    def btn_clicked_slot(self):
        old_path = self.path

        self.path = QFileDialog.getOpenFileName(self, 'Open file',
                                                '../datasets', 'Image Files(*.jpg; *.png);;All File(*.*')
        # 실행시, 윈도우 탐색기가 뜬다 => 캡션 : 파일탐색기 제목 / 디렉토리 : 시작 디렉토리 / 필터 : 파일 필터
        # 필터는 이미지 파일(*.포멧1; *.포멧2);; 텍스트 파일(*.포멧3; *.포멧4: *.포멧5)

        # 아무것도 선택 안하고 취소할 때, 이전 이미지를 출력하여 에러방지를 한다.
        if self.path[0] == '':
            self.path = old_path

        # 라벨에 선택한 이미지 띄우기
        print(self.path)                            # 파일을 선택하면 경로만 리턴된다.
        pixmap = QPixmap(self.path[0])              # pixmap으로 변경한다
        self.lbl_image.setPixmap(pixmap)            # lbl 라벨에 Pixmap을 Set

        img = Image.open(self.path[0])
        img = img.convert('RGB')
        img = img.resize((64, 64))
        data = np.asarray(img)
        data = data / 255                           # remix 스케일링
        data = data.reshape(1, 64, 64, 3)
        pred = self.model.predict(data)
        print(pred)

        # 결과 출력
        if pred < 0.5:
            # self.lbl_predict.setText('고양이 입니다. ' + str(pred[0][0]))
            # self.lbl_predict.setText('강아지 입니다. ' + str(round(pred[0][0], 2)) + '%')

            self.lbl_predict.setText('고양이 입니다. ' + str(round(100 -(pred[0][0] * 100), 2)) + '%')
        else:
            self.lbl_predict.setText('강아지 입니다. ' + str(round(pred[0][0] * 100, 2)) + '%')
        # setText는 print문이 아니다. 고로 문자열로 변형해서 콤마 대신 +를 붙힌다.

#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())


# 파일 탐색기에서 아무것도 안고르고 취소 버튼을 누르면 어플리케이션이 꺼진다.
# 선택을 안하면 ('', '') == Null 을 리턴한다.











































