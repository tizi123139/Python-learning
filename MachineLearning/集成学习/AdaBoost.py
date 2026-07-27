import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score

df_wine = pd.read_csv('./data/wine0501.csv')
df_wine = df_wine[df_wine['Class label']!=1]

x=df_wine[['Alcohol','Hue']]
y=df_wine['Class label']

le = LabelEncoder()
y = le.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=23,stratify=y)

estimator1=DecisionTreeClassifier(max_depth=3)
estimator1.fit(x_train,y_train)
y_pred=estimator1.predict(x_test)
print(accuracy_score(y_test,y_pred))

estimator2=AdaBoostClassifier(estimator=estimator1,n_estimators=200,learning_rate=0.1)
estimator2.fit(x_train,y_train)
y_pred=estimator2.predict(x_test)
print(accuracy_score(y_test,y_pred))