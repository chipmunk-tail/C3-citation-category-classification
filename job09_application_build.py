import icon_rc
import sys
import numpy as np
import pandas as pd
#from tabnanny import format_witnesses
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
#from keras.models import load_model
from PIL import Image

import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


# ui를 class로 만들어주는 것 = uic
form_window = uic.loadUiType('./search.ui')[0]


# Exam이란 클래스 생성, QWidget,
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()                          # super == 조상 클래스 / 조상클래스는 자손클래스의 첫줄에 있어야 한다.
        self.setupUi(self)
        self.label_2.setPixmap(QPixmap('./writing_agenda_document_pencil_paper_notes_icon_262803 (1).png'))
        self.model_main = load_model('./models/paper_main_category_classification_model_set_B_0.5791409015655518.h5')
        self.model_sub = load_model('./models/paper_sub_category_classification_model_B_0.6480162739753723.h5')
        self.stopwords_kor = pd.read_csv('format_files/stopwords_kor.csv', index_col=0)
        self.stopwords_eng = pd.read_csv('format_files/stopwords_eng.csv', index_col=0)
        self.lineEdit.setText("")
        self.load_main_encoder()
        self.load_main_token()


        # self.lineEdit = QLineEdit(self)
        self.Search.clicked.connect(self.get_text)    # Qt = signal slot
         # 버튼 이름.버튼이 눌리면.실행해라(함수를)

    def load_main_encoder(self):
        with open('format_files/encoder.pickle', 'rb') as f:  # rb = read binary
            self.encoder = pickle.load(f)

    def load_main_token(self):
        with open('format_files/paper_title_token_max_51.pickle', 'rb') as f:
            self.token = pickle.load(f)

    def get_text(self):
        input_text = self.lineEdit.text()
        print(input_text)

        df = pd.DataFrame([input_text, 0])
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x, axis=0)
        df.replace('', pd.NA, inplace=True)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)  # Remove duplicate
        df.reset_index(drop=True, inplace=True)  # Drop default index
        print(df.head())
        df.info()
        print(df.category.value_counts())

        # Makes Dataframe
        X = df['titles']
        Y = df['category']

        encoder = self.encoder
        label = encoder.classes_
        print(label)

        # onehot encode
        labeled_y = encoder.transform(Y)
        onehot_Y = to_categorical(labeled_y)
        print(onehot_Y)

        # X : morpheme separation
        okt = Okt()
        for i in range(len(X)):
            X[i] = okt.morphs(X[i], stem=True)
            X[i] = [word for word in X[i] if len(word) > 1]  # 길이가 1인 단어 제거
        print(X)

        # Replace stopword to ' '
        for sentence in range(len(X)):
            words = []
            for word in range(len(X[sentence])):
                if len(X[sentence][word]) > 1:  # drop useless word
                    if X[sentence][word] not in (
                            list(self.stopwords_kor['stopword_kor']) or list(self.stopwords_eng['stopword_eng'])):
                        if (X[sentence][word] >= 'a' and X[sentence][word] <= 'z'):
                            if len(X[sentence][word]) <= 2:
                                continue
                        words.append(X[sentence][word])

            X[sentence] = ' '.join(words)
        print(X[:5])

        # new token not in model = 0

        token = self.token

        tokened_X = token.texts_to_sequences(X)
        print(tokened_X[:5])

        # if token over 43
        for i in range(len(tokened_X)):
            if len(tokened_X[i]) > 51:
                tokened_X[i] = tokened_X[i][:51]
        X_pad = pad_sequences(tokened_X, 51)

        print(X_pad[:5])


        preds = self.model_main.predict(X_pad)

        predictsA = []
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
            predictsA.append([first, second, third, fourth, fifth, sixth, seventh, eighth])


        if predictsA[0] == '자연과학':

            df = pd.DataFrame([input_text, 0])
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x, axis=0)
            df.replace('', pd.NA, inplace=True)
            df.dropna(inplace=True)
            df.drop_duplicates(inplace=True)  # Remove duplicate
            df.reset_index(drop=True, inplace=True)  # Drop default index
            print(df.head())
            df.info()
            print(df.category.value_counts())

            with open('format_files/encoder_sub.pickle', 'rb') as f:  # rb = read binary
                encoder = pickle.load(f)

            label = encoder.classes_
            print(label)

            # onehot encode
            labeled_y = encoder.transform(Y)
            onehot_Y = to_categorical(labeled_y)
            print(onehot_Y)

            # X : morpheme separation
            okt = Okt()
            for i in range(len(X)):
                X[i] = okt.morphs(X[i], stem=True)
                X[i] = [word for word in X[i] if len(word) > 1]  # 길이가 1인 단어 제거
            print(X)

            # Replace stopword to ' '
            for sentence in range(len(X)):
                words = []
                for word in range(len(X[sentence])):
                    if len(X[sentence][word]) > 1:  # drop useless word
                        if X[sentence][word] not in (
                                list(stopwords_kor['stopword_kor']) or list(stopwords_eng['stopword_eng'])):
                            if (X[sentence][word] >= 'a' and X[sentence][word] <= 'z'):
                                if len(X[sentence][word]) <= 2:
                                    continue
                            words.append(X[sentence][word])

                X[sentence] = ' '.join(words)
            print(X[:5])

            # new token not in model = 0

            with open('format_files/paper_sub_title_token_max_30.pickle', 'rb') as f:
                token = pickle.load(f)

            tokened_X = token.texts_to_sequences(X)
            print(tokened_X[:5])

            # if token over 43
            for i in range(len(tokened_X)):
                if len(tokened_X[i]) > 51:
                    tokened_X[i] = tokened_X[i][:51]
            X_pad = pad_sequences(tokened_X, 51)

            print(X_pad[:5])

            preds = self.model_sub.predict(X_pad)

            predictsB = []
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
                pred[np.argmax(pred)] = 0
                ninth = label[np.argmax(pred)]
                pred[np.argmax(pred)] = 0
                tenth = label[np.argmax(pred)]
                predictsB.append([first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth])

            df['predict'] = predictsB



        self.pushButton_01.setText(predictsA[0])
        self.pushButton_02.setText(predictsA[1])
        self.pushButton_03.setText(predictsA[2])
        self.pushButton_04.setText(predictsA[3])
        self.pushButton_05.setText(predictsA[4])
        self.pushButton_06.setText(predictsA[5])
        self.pushButton_07.setText(predictsA[6])
        self.pushButton_08.setText(predictsA[7])

        self.pushButton_nature_01.setText(predictsB[0])
        self.pushButton_nature_02.setText(predictsB[1])
        self.pushButton_nature_03.setText(predictsB[2])
        self.pushButton_nature_04.setText(predictsB[3])
        self.pushButton_nature_05.setText(predictsB[4])
        self.pushButton_nature_06.setText(predictsB[5])
        self.pushButton_nature_07.setText(predictsB[6])
        self.pushButton_nature_08.setText(predictsB[7])
        self.pushButton_nature_09.setText(predictsB[8])
        self.pushButton_nature_10.setText(predictsB[9])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())












































