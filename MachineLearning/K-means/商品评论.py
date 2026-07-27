import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv('./data/书籍评价.csv',encoding='gbk')
df['labels'] = np.where(df['评价']=='好评',1,0)
y=df['labels']

comment_list = [','.join(jieba.lcut(line)) for line in df['内容']]

with open('./data/stopwords.txt','r',encoding='utf-8') as src_f:
    stopwords_list = src_f.readlines()
    stopwords_list = [line.strip() for line in stopwords_list]
    stopwords_list = list(set(stopwords_list))

transfer = CountVectorizer(stop_words=stopwords_list)
transfer.fit(comment_list)
x = transfer.transform(comment_list).toarray()
x_train=x[:10]
y_train=y[:10]
x_test=x[10:]
y_test=y[10:]
estimator = MultinomialNB()
estimator.fit(x_train,y_train)
y_pred = estimator.predict(x_test)

print(accuracy_score(y_test,y_pred))
