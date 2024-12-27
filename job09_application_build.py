import icon_rc
import sys
import numpy as np
#from tabnanny import format_witnesses
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
#from keras.models import load_model
from PIL import Image

# ui를 class로 만들어주는 것 = uic
form_window = uic.loadUiType('./search.ui')[0]

# Exam이란 클래스 생성, QWidget,
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()                          # super == 조상 클래스 / 조상클래스는 자손클래스의 첫줄에 있어야 한다.
        self.setupUi(self)
        self.label_2.setPixmap(QPixmap('./writing_agenda_document_pencil_paper_notes_icon_262803 (1).png'))
        self.model = load_model('./models/paper_main_category_classification_model_set_B_0.5791409015655518.h5')
        self.model = load_model('./models/paper_sub_category_classification_model_B_0.6480162739753723.h5')

        preds = model.predict(X_pad)

        predicts = []
        for pred in preds:
            first = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            second = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            third = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            fourth = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            fifth = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            sixth = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            seventh = label[np.argmax(pred)]
            pred[np.argmax(pred)] = 0
            eighth = label[np.argmax(pred)]
            predicts.append([first, second, third, fourth, fifth, sixth, seventh, eighth])

        self.btn_select.clicked.connect(self.btn_clicked_slot)    # Qt = signal slot
         # 버튼 이름.버튼이 눌리면.실행해라(함수를)

     # Qt에서 제공되는게 아닌 Windows에서 제공되는 기능
    def Search(self):
         old_path = self.path

         self.path = QFileDialog.getOpenFileName(self, 'Open file',
                                                 '../datasets')
#         # 실행시, 윈도우 탐색기가 뜬다 => 캡션 : 파일탐색기 제목 / 디렉토리 : 시작 디렉토리 / 필터 : 파일 필터
#         # 필터는 이미지 파일(*.포멧1; *.포멧2);; 텍스트 파일(*.포멧3; *.포멧4: *.포멧5)

#         # 결과 출력
         #대분류 주제
         str['인문학','사회과학','자연과학','공학','의약학','농수해안','예술체육','복합학']
         #중분류 주제
         str['생물학','생활과학','물리학','화학','수학','자연과학일반','통계학','기타자연과학','지구과학','지질학']
#일조 모델과 측정을 통한 도시 지역 건물의 일조 시간과 표면 온도 분석
         if pred < 0.5:
              self.pushButton_01.setText('1.%s',#dfdf#)
              self.pushButton_02.setText('2.%s',#dfdf#)
              self.pushButton_03.setText('3.%s',#dfdf#)
              self.pushButton_04.setText('4.%s',#dfdf#)
              self.pushButton_05.setText('5.%s',#dfdf#)
              self.pushButton_06.setText('6.%s',#dfdf#)
              self.pushButton_07.setText('7.%s',#dfdf#)
              self.pushButton_08.setText('8.%s',#dfdf#)

            if else
              def pushButton_01(self):
                  old_path = self.path

                  self.path = QFileDialog.getOpenFileName(self, 'Open file',
                                                          '../datasets')

         if pred < 0.5:
              self.pushButton_nature_01.setText('1.%s',#dfdf#)
              self.pushButton_nature_02.setText('2.%s',#dfdf#)
              self.pushButton_nature_03.setText('3.%s',#dfdf#)
              self.pushButton_nature_04.setText('4.%s',#dfdf#)
              self.pushButton_nature_05.setText('5.%s',#dfdf#)
              self.pushButton_nature_06.setText('6.%s',#dfdf#)
              self.pushButton_nature_07.setText('7.%s',#dfdf#)
              self.pushButton_nature_08.setText('8.%s',#dfdf#)
              self.pushButton_nature_09.setText('9.%s',#dfdf#)
              self.pushButton_nature_10.setText('10.%s',#dfdf#)

#             self.lbl_predict.setText('강아지 입니다. ' + str(round(pred[0][0] * 100, 2)) + '%')
#         # setText는 print문이 아니다. 고로 문자열로 변형해서 콤마 대신 +를 붙힌다.








#        # self.path = ('E:/AISW/pyCh/Cat_and_Dog_classfication/datasets/test/doji.jpg',
#        #              'Image Files(*.jpg; *.png')    # 절대 경로는 Windows 시스템에서 \를 쓰는 걸 /로 변경한다.
#        # self.model = load_model('E:/AISW/pyCh/Cat_and_Dog_classfication/models-20241218T112011Z-001/models/cat_and_dog_binary_classfication_0.8583999872207642.h5')
#
#         # 디자이너앱에서 이미지 스케일드 컨텐츠 옵션을 줌으로써
#         # pixmap = QPixmap(self.path[0])              # pixmap으로 변경한다
#         # self.lbl_image.setPixmap(pixmap)            # lbl 라벨에 Pixmap을 Set
#
#        # self.btn_select.clicked.connect(self.btn_clicked_slot)    # Qt = signal slot
#         # 버튼 이름.버튼이 눌리면.실행해라(함수를)
#
#     # Qt에서 제공되는게 아닌 Windows에서 제공되는 기능
#   #  def btn_clicked_slot(self):
#    #     old_path = self.path
#
#     #    self.path = QFileDialog.getOpenFileName(self, 'Open file',
#                                                 '../datasets', 'Image Files(*.jpg; *.png);;All File(*.*')
#         # 실행시, 윈도우 탐색기가 뜬다 => 캡션 : 파일탐색기 제목 / 디렉토리 : 시작 디렉토리 / 필터 : 파일 필터
#         # 필터는 이미지 파일(*.포멧1; *.포멧2);; 텍스트 파일(*.포멧3; *.포멧4: *.포멧5)
#
#         # 아무것도 선택 안하고 취소할 때, 이전 이미지를 출력하여 에러방지를 한다.
#         if self.path[0] == '':
#             self.path = old_path
#
#         # 라벨에 선택한 이미지 띄우기
#         print(self.path)                            # 파일을 선택하면 경로만 리턴된다.
#         pixmap = QPixmap(self.path[0])              # pixmap으로 변경한다
#         self.lbl_image.setPixmap(pixmap)            # lbl 라벨에 Pixmap을 Set
#
#         img = Image.open(self.path[0])
#         img = img.convert('RGB')
#         img = img.resize((64, 64))
#         data = np.asarray(img)
#         data = data / 255                           # remix 스케일링
#         data = data.reshape(1, 64, 64, 3)
#         pred = self.model.predict(data)
#         print(pred)
#
#         # 결과 출력
#         if pred < 0.5:
#             # self.lbl_predict.setText('고양이 입니다. ' + str(pred[0][0]))
#             # self.lbl_predict.setText('강아지 입니다. ' + str(round(pred[0][0], 2)) + '%')
#
#             self.lbl_predict.setText('고양이 입니다. ' + str(round(100 -(pred[0][0] * 100), 2)) + '%')
#         else:
#             self.lbl_predict.setText('강아지 입니다. ' + str(round(pred[0][0] * 100, 2)) + '%')
#         # setText는 print문이 아니다. 고로 문자열로 변형해서 콤마 대신 +를 붙힌다.
#
# #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())


# 파일 탐색기에서 아무것도 안고르고 취소 버튼을 누르면 어플리케이션이 꺼진다.
# 선택을 안하면 ('', '') == Null 을 리턴한다.











































