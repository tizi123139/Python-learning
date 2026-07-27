import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import  classification_report
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

data = pd.read_csv('./data/titanic_train.csv')
x=data[['Pclass','Sex','Age']]
y=data['Survived']
x=x.copy()
x['Age']=x['Age'].fillna(x['Age'].mean())
x=pd.get_dummies(x,columns=['Sex'])
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=23)
estimator=DecisionTreeClassifier(max_depth=10)
estimator.fit(x_train,y_train)
y_pred=estimator.predict(x_test)
print(classification_report(y_test,y_pred))
plt.figure(figsize=(30,20))
plot_tree(estimator,filled=True,max_depth=10)
plt.show()