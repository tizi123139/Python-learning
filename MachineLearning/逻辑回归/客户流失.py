
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,roc_auc_score,recall_score,precision_score,f1_score,classification_report

def data_preprocess():
    churn_df = pd.read_csv('./data/churn.csv')
    churn_df = pd.get_dummies(churn_df,columns=['gender','Churn'])
    churn_df.drop(['Churn_No','gender_Male'],axis=1,inplace=True)
    churn_df.rename(columns={'Churn_Yes':'flag'},inplace=True)
    x=churn_df[['Contract_Month','internet_other','PaymentElectronic']]
    y=churn_df['flag']
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=23)
    estimator = LogisticRegression()
    estimator.fit(x_train,y_train)
    y_pred = estimator.predict(x_test)
    print(accuracy_score(y_test,y_pred))
    print(roc_auc_score(y_test,y_pred))
    print(precision_score(y_test,y_pred))
    print(recall_score(y_test,y_pred))
    print(f1_score(y_test,y_pred))
    print(classification_report(y_test,y_pred))


if __name__ == '__main__':
    data_preprocess()
