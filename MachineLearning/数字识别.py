import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
from collections import Counter

def show_digit(idx):
    df = pd.read_csv('./data/手写数字识别.csv')
    if idx < 0 or idx > len(df) -1:
        print('索引越界')
        return

    x=df.iloc[:,1:]
    y=df.iloc[:,0]

    x=x.iloc[idx].values.reshape(28,28)

    plt.imshow(x,cmap='gray')
    plt.axis('off')
    plt.show()

def train_model():
    df = pd.read_csv('./data/手写数字识别.csv')
    x = df.iloc[:, 1:]
    y = df.iloc[:, 0]

    x=x/255
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 22,stratify=y)
    clf = KNeighborsClassifier(n_neighbors=3)
    clf.fit(x_train, y_train)
    print(clf.score(x_test, y_test))
    joblib.dump(clf, './model/数字识别.pkl')

def use_model():
    x=plt.imread('./data/demo.png')
    #plt.imshow(x, cmap='gray')
    #plt.show()
    clf = joblib.load('./model/数字识别.pkl')
    x=x.reshape(1,-1)
    y_pre = clf.predict(x)
    print(y_pre)

if __name__ == '__main__':
    #show_digit(9)
    train_model()
    use_model()