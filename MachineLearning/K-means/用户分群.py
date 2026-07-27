import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='4'
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import calinski_harabasz_score,silhouette_score

def find_k():
    df = pd.read_csv('./data/customers.csv')
    sse_list = []
    sc_list = []
    x=df.iloc[:,3:5]

    for k in range(2,20):
        estimator = KMeans(n_clusters=k,max_iter=100, random_state=23)
        estimator.fit(x)
        y_pred = estimator.predict(x)
        sse_list.append(estimator.inertia_)
        sc_list.append(silhouette_score(x,y_pred))
    plt.figure(figsize=(20,10))
    plt.plot(range(2,20),sse_list,label='SSE')
    plt.show()
    plt.figure(figsize=(20,10))
    plt.plot(range(2,20),sc_list,label='SC')
    plt.show()

def train():
    df = pd.read_csv('./data/customers.csv')
    x=df.iloc[:,3:5]
    estimator = KMeans(n_clusters=5,max_iter=100,random_state=23)
    estimator.fit(x)
    y_pred = estimator.predict(x)
    plt.scatter(x.values[y_pred==0,0],x.values[y_pred==0,1])
    plt.scatter(x.values[y_pred == 1, 0], x.values[y_pred == 1, 1])
    plt.scatter(x.values[y_pred == 2, 0], x.values[y_pred == 2, 1])
    plt.scatter(x.values[y_pred == 3, 0], x.values[y_pred == 3, 1])
    plt.scatter(x.values[y_pred == 4, 0], x.values[y_pred == 4, 1])
    plt.scatter(estimator.cluster_centers_[:,0], estimator.cluster_centers_[:,1])
    plt.title('K-Means')
    plt.show()

if __name__ == '__main__':
    train()