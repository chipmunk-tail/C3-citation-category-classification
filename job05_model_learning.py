import numpy as np
import matplotlib.pyplot as plt
from Tools.i18n.makelocalealias import optimize
from attr.setters import validate
from keras.models import *
from keras.layers import *
from keras.callbacks import EarlyStopping



# Load train
X_train = np.load('./train_test_split/paper_title_data_X_train_wordsize_62892_max_54.npy', allow_pickle = True)
X_test = np.load('./train_test_split/paper_title_data_X_test_wordsize_62892_max_54.npy', allow_pickle = True)
Y_train = np.load('./train_test_split/paper_title_data_Y_train_wordsize_62892_max54.npy', allow_pickle = True)
Y_test = np.load('./train_test_split/paper_title_data_Y_test_wordsize_62892_max_54.npy', allow_pickle = True)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)


model = Sequential()
model.add(Embedding(62892, 1000))                                                # makes token to vector
model.build(input_shape = (None, 54))
model.add(Conv1D(64, kernel_size = 5, padding = 'same', activation = 'relu'))
model.add(MaxPool1D(pool_size = 1))                                             # actually not working (Conv & MaxPool set)
model.add(LSTM(256, activation = 'tanh', return_sequences = True))
model.add(Dropout(0.3))
model.add(LSTM(128, activation = 'tanh', return_sequences = True))
model.add(Dropout(0.3))
model.add(LSTM(128, activation = 'tanh', return_sequences = True))
model.add(Dropout(0.3))
model.add(LSTM(128, activation = 'tanh', return_sequences = True))
model.add(Dropout(0.3))
model.add(LSTM(128, activation = 'tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(8, activation = 'softmax'))                                     # len(category), multi classifier == softmax
model.summary()


model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
early_stopping = EarlyStopping(monitor = 'val_accuracy', patience = 5)          # if accuracy does not rise for 5 epochs
fit_hist = model.fit(X_train, Y_train, batch_size = 256,
                     epochs = 10, validation_data = (X_test, Y_test))


score = model.evaluate(X_test, Y_test, verbose = 0)
print('Final test set accuracy', score[1])
model.save('./models/paper_main_category_classification_model_set05_{}.h5'.format(
    fit_hist.history['val_accuracy'][-1]))

plt.plot(fit_hist.history['accuracy'], label = 'accuracy')
plt.plot(fit_hist.history['val_accuracy'], label = 'val_accuracy')
plt.legend()
plt.show()
