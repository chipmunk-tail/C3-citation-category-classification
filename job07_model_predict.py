import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


df = pd.read_csv('crawling_data/KCL_titles_total_predict_20241226.csv')
df.drop_duplicates(inplace = True)                          # Remove duplicate
df.reset_index(drop = True, inplace = True)                 # Drop default index
print(df.head())
df.info()
print(df.category.value_counts())


# Makes Dataframe
X = df['titles']
Y = df['category']

with open('format_files/encoder.pickle', 'rb') as f:            # rb = read binary
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
    X[i] = okt.morphs(X[i], stem = True)
print(X)


# open korean stopword
stopwords_kor = pd.read_csv('format_files/stopwords_kor.csv', index_col = 0)
stopwords_eng = pd.read_csv('format_files/stopwords_eng.csv', index_col = 0)


# Replace stopword to ' '
for sentence in range(len(X)):
    words = []
    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:              # drop useless word
            if X[sentence][word] not in (list(stopwords_kor['stopword_kor']) or list(stopwords_eng['stopword_eng'])):
                if (X[sentence][word] >= 'a' and X[sentence][word] <= 'z'):
                    if len(X[sentence][word]) <= 2:
                        X[sentence][word] = ''
                words.append(X[sentence][word])

    X[sentence] = ' '.join(words)
print(X[:5])


# new token not in model = 0

with open('format_files/paper_title_token_max_51.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])

# if token over 43
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 51:
        tokened_X[i] = tokened_X[i][:51]
X_pad = pad_sequences(tokened_X, 51)


print(X_pad[:5])




model = load_model('./models/paper_main_category_classification_model_set_0.5980924367904663.h5')
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


df['predict'] = predicts
print(df.head(30))


score = model.evaluate(X_pad, onehot_Y)
print(score[1])

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 1

print(df.OX.mean())
