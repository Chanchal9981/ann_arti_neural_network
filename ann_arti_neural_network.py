# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
!pip install pyyaml h5py

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
print(torch.__version__)

x1=r"https://drive.google.com/uc?export=download&id=1WH1809emdGOWmWZDlXbz6YR5Es3FJi9V"
x=pd.read_csv(x1)
x

X=x.drop("target",axis=1)
y=x["target"]
print("shape of X is=",X.shape)
print("shape of y is=",y.shape)

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_sc=sc.fit_transform(X)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X_sc,y,test_size=0.3,random_state=51)
print("shape of X_train is",X_train.shape)
print("shape of y_train is",y_train.shape)
print("shape of X_test is",X_test.shape)
print("shape of y_test is",y_test.shape)

"""**know build a deeplearning model**"""

import keras

model=keras.models.Sequential([
                         keras.layers.Flatten(input_dim=31),#where 31 is a independ variable
                         keras.layers.Dropout(0.3),# to remove the variance of dataset
                         keras.layers.Dense(units=16,activation='relu'), # where 16 is total number of nuerons which is used in Neural Network
                         keras.layers.Dropout(0.3),
                         keras.layers.Dense(units=1,activation='sigmoid') # where 1 is total numbers of output come
])
# when we work on regression type of data we have to use sigmoid
# whne we work categorical data we have to use softmax

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
# there we use binary_crossentropy because data is in regression format
# if data is in categorical format we use categorical_crossentropy

model.fit(X_train,y_train,batch_size=100,epochs=150)

model.summary()

model.evaluate(X_test,y_test)

y_pred=model.predict(X_test)
y_pred=(y_pred> 0.5)

from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred)
sns.heatmap(cm,annot=True,fmt="d")

model.save("ann.h5")

"""# K-fold in ANN"""

import keras
from sklearn.model_selection import cross_val_score
from keras.wrappers.scikit_learn import KerasClassifier
# we use k-fold validation to increase our model accuracy

def classfication_data():
  model=keras.models.Sequential([
                                 keras.layers.Flatten(input_dim=31),
                                 keras.layers.Dense(units=16,activation='relu'),
                                 keras.layers.Dense(units=1,activation='sigmoid')])
  model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
  return model

model=KerasClassifier(build_fn=classfication_data,batch_size=100,epochs=100)
accuries=cross_val_score(estimator=model,X=X_train,y=y_train,cv=10,n_jobs=-1)

accuries

accuries.mean()

"""# Hyperperamitre tunnning"""

# we use hyperperamitre tunnning to increase a model performence
import keras
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

def classfication_data(optimizer='adam'):
  model=keras.models.Sequential([
                                 keras.layers.Flatten(input_dim=31),
                                 keras.layers.Dense(units=16,activation='relu'),
                                 keras.layers.Dense(units=1,activation='sigmoid')])
  model.compile(optimizer=optimizer,loss='binary_crossentropy',metrics=['accuracy'])
  return model

model=KerasClassifier(build_fn=classfication_data)
peramitres={'batch_size':[100,150],'epochs':[100,200],'optimizer':['adam','rmsprop']}
grid_search=GridSearchCV(estimator=model,param_grid=peramitres,scoring='accuracy',cv=10)
grid_search=grid_search.fit(X_train,y_train)
best_peramitre=grid_search.best_perams_
best_score=grid_search.best_score_
accuries=cross_val_score(estimator=model,X=X_train,y=y_train,cv=10,n_jobs=-1)





