# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 23:27:24 2019

@author: kumar
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import statistics as sts
import pylab

dataset=pd.read_csv("C:\\Users\\kumar\\PythonAssign\\Linear\\Linear\\Datasets\\Salary_Data.csv")
dataset.columns
import statsmodels.formula.api as smf
model=smf.ols("Salary~YearsExperience",data=dataset).fit()
pred=model.predict(dataset)
dataset_binary = dataset[['YearsExperience', 'Salary']] 
X = np.array(dataset_binary['YearsExperience']).reshape(-1, 1) 
y = np.array(dataset_binary['Salary']).reshape(-1, 1) 
y=np.log(dataset_binary.Salary)
y=np.array(y).reshape(-1,1)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=42)
from sklearn import linear_model
regressor= linear_model.LinearRegression() 
regressor.fit(x_train,y_train)
import pickle
pickle.dump(regressor, open('model.pkl', 'wb'))
model=pickle.load(open('model.pkl','rb'))