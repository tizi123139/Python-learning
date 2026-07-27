import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv('./data/breast-cancer-wisconsin.csv')

data.replace('?', np.nan, inplace=True)
data.dropna(axis=0,inplace=True)

x=data.iloc[:,1:-1]
y=data.Class
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=23)
transfer = StandardScaler()
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)

estimator = LogisticRegression()
estimator.fit(x_train,y_train)
y_pred = estimator.predict(x_test)
accuracy = accuracy_score(y_test,y_pred)
print(accuracy)