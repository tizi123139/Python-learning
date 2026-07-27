import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from collections import Counter
from sklearn.metrics import  classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import class_weight

from MathModeling.决策树 import y_train


def data_process():
    df = pd.read_csv('./data/红酒品质分类.csv')
    x=df.iloc[:,:-1]
    y=df.iloc[:,-1]-3
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=23,stratify=y)

    pd.concat([x_train,y_train],axis=1).to_csv('./data/红酒品质分类_train.csv',index=False)
    pd.concat([x_test,y_test],axis=1).to_csv('./data/红酒品质分类_test.csv',index=False)


def train_model():
    train_data = pd.read_csv('./data/红酒品质分类_train.csv')
    test_data = pd.read_csv('./data/红酒品质分类_test.csv')
    x_train = train_data.iloc[:,:-1]
    y_train = train_data.iloc[:,-1]

    x_test = test_data.iloc[:,:-1]
    y_test = test_data.iloc[:,-1]

    estimator = xgb.XGBClassifier(
        max_depth=5,
        n_estimators=100,
        learning_rate=0.1,
        random_state=23,
        objective='multi:softmax',
    )

    class_weight.compute_sample_weight('balanced',y_train)
    estimator.fit(x_train, y_train)
    print(estimator.score(x_test,y_test))
    joblib.dump(estimator,'./model/红酒品质分类_model.pkl')

def use_model():
    train_data = pd.read_csv('./data/红酒品质分类_train.csv')
    test_data = pd.read_csv('./data/红酒品质分类_test.csv')
    x_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1]

    x_test = test_data.iloc[:, :-1]
    y_test = test_data.iloc[:, -1]
    estimator = joblib.load('./model/红酒品质分类_model.pkl')
    param_dict={'max_depth':[2,3,5,6,7],'n_estimators':[30,50,100,150],'learning_rate':[0.2,0.3,1,1.3]}
    skf = StratifiedKFold(n_splits=5,shuffle=True,random_state=23)
    gs_estimator = GridSearchCV(estimator,param_dict,cv=skf)
    gs_estimator.fit(x_train,y_train)
    y_pred = gs_estimator.predict(x_test)
    print(classification_report(y_test,y_pred))
    print(gs_estimator.best_params_)
    print(gs_estimator.best_score_)

if __name__ == '__main__':
    use_model()
