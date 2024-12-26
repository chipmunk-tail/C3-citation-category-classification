import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt                                  # Open korea tokenizer / need install Java jdk21
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Notice
#
# Please install java jdk21
#


# Open CSV
df = pd.read_csv('crawling_data/KCL_titles_total_20241226.csv')
df.drop_duplicates(inplace = True)                          # Remove duplicate
df.reset_index(drop = True, inplace = True)                 # Drop default index
print(df.head())
df.info()
print(df.category.value_counts())


# Makes Dataframe
X = df['titles']
Y = df['category']
print(X[0])


# Y : labeling
encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)                        # fit_transform = only use first time transform
print(labeled_y[:3])

label = encoder.classes_
print(label)


# save encoder
with open('format_files/encoder.pickle', 'wb') as f:            # wb = write binary
    pickle.dump(encoder, f)


# onehot encode
onehot_Y = to_categorical(labeled_y)
print(onehot_Y)



# X : morpheme separation
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem = True)
print(X)


# Open korean stopword
stopwords_kor = pd.read_csv('format_files/stopwords_kor.csv', index_col = 0)
stopwords_eng = pd.read_csv('format_files/stopwords_eng.csv', index_col = 0)


# Drop stopword
for sentence in range(len(X)):
    words = []
    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:              # drop useless word
            if X[sentence][word] not in (list(stopwords_kor['stopword_kor']) or list(stopwords_eng['stopword_eng'])):
                if (X[sentence][word] >= 'a' and X[sentence][word] <= 'z'):
                    if len(X[sentence][word]) < 1:
                        word = ' '
                words.append(X[sentence][word])

    X[sentence] = ' '.join(words)
# print(X[:5])
print(X)


#
token = Tokenizer()                                 # labeling natural language
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1                # max length + ' '

print(wordsize)
print(tokened_X[:5])


# find max length
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max)               # keras package, padding == fill '0'
print(X_pad)
print(len(X_pad[0]))


#
X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size = 0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)


# Save token
with open('./format_files/paper_title_token_max_{}.pickle'.format(max), 'wb') as f:
    pickle.dump(token, f)

# Save
np.save('./train_test_split/paper_title_data_b_X_train_wordsize_{}_max_{}'.format(wordsize, max), X_train)      # .npy
np.save('./train_test_split/paper_title_data_b_X_test_wordsize_{}_max_{}'.format(wordsize, max), X_test)
np.save('./train_test_split/paper_title_data_b_Y_train_wordsize_{}_max{}'.format(wordsize, max), Y_train)
np.save('./train_test_split/paper_title_data_b_Y_test_wordsize_{}_max_{}'.format(wordsize, max), Y_test)
