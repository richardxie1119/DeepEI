# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 14:46:55 2020

@author: hcji
"""

import numpy as np
import tensorflow.keras.backend as K
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Flatten, Conv1D, MaxPooling1D
from tensorflow.keras import optimizers
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

class CNN:
    def __init__(self, X, Y):
        X = np.expand_dims(X, -1)
        self.X = X
        self.Y = Y
        self.X_tr, self.X_ts, self.Y_tr, self.Y_ts = train_test_split(X, Y, test_size=0.1)
        
        inp = Input(shape=(X.shape[1:3]))
        hid = inp
        n = X.shape[1]
        for j in range(3):
            hid = Conv1D(n, kernel_size=3, activation='relu')(hid)
            hid = MaxPooling1D(pool_size=2)(hid)
            n = int(n * 0.5)
        hid = Flatten()(hid)
        prd = Dense(2, activation="softmax")(hid)
        opt = optimizers.Adam(lr=0.001)
        model = Model(inp, prd)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['acc'])
        self.model = model
    
    def train(self, epochs=5):
        self.model.fit(self.X_tr, self.Y_tr, epochs=epochs)
    
    def test(self):
        Y_pred = np.round(self.model.predict(self.X_ts))
        f1 = f1_score(self.Y_ts[:,0], Y_pred[:,0])
        precision = precision_score(self.Y_ts[:,0], Y_pred[:,0])
        recall = recall_score(self.Y_ts[:,0], Y_pred[:,0])
        accuracy = accuracy_score(self.Y_ts[:,0], Y_pred[:,0])
        return accuracy, precision, recall, f1
    
    def save(self, path):
        model_json = self.model.to_json()
        with open('Fingerprint/cnn_models/model.json', "w") as js:  
            js.write(model_json)
        self.model.save_weights(path)
        K.clear_session()    
    