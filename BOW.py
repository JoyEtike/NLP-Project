from math import sqrt
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import time


df = pd.read_csv ('CleanData.csv')
df = df.drop(['Unnamed: 0'], axis = 1)



stop_words = stopwords.words('english')
l2 = ['not']
stop_words =  [x for x in stop_words if x not in l2]
#print(stop_words)
ps = PorterStemmer()
lem = WordNetLemmatizer()
cv = CountVectorizer(min_df = 0.01, max_df = 0.90)


df["token"] = df['Review'].fillna("").map(nltk.word_tokenize)
df['NoStopWord'] = df['token'].apply(lambda x: [word for word in x if word not in stop_words])
df['LemWords'] = df['NoStopWord'].apply(lambda x: [lem.lemmatize(y) for y in x])
df['LemWordsJoin'] = df['LemWords'].apply(lambda x:" ".join(x))




x_trsfrm = cv.fit_transform(df['LemWordsJoin'])
X_trsfrm = x_trsfrm.toarray()
df_y = df['Rating']
y_trsfrm=df_y.astype('int')

x_train, x_test, y_train, y_test = train_test_split(X_trsfrm,y_trsfrm,test_size=0.30)



counts = pd.DataFrame(x_train,
                      columns=cv.get_feature_names())
counts.to_csv('array.csv',index=True)
k = round(sqrt (len(x_train[0])))
print(x_train.shape)

def Nvb (a,b,c,d):
    t0 = time.time()
    nb = MultinomialNB()
    clf = nb.fit(a, b)
    y_pred = clf.predict(c)
    print("Accuracy: ", accuracy_score(d, y_pred)*100,"%")
    print("F1 Score: ", f1_score(d,y_pred,average='weighted'))
    print("Classification: ", classification_report(d,y_pred))
    print("Confusion Matrix: ", '\n',confusion_matrix(d, y_pred))
    t1 = time.time()
    total = t1-t0
    print(total)

    return total


def knn(a,b,c,d):
    t0 = time.time()
    
    scaler = StandardScaler()

    scaler.fit(a)

    X_train_trfm = scaler.transform(a)
    X_test_trfm = scaler.transform(c)
    
    classifier = KNeighborsClassifier(n_neighbors = 10, weights='uniform')
    classifier.fit(X_train_trfm, b)
    y_pred = classifier.predict(X_test_trfm)
    print("Accuracy: ", accuracy_score(d, y_pred)*100,"%")
    print("F1 Score: ", f1_score(d,y_pred,average='weighted'))
    print(classification_report(d,y_pred))
    print("Confusion Matrix: ", '\n', confusion_matrix(d, y_pred))
    t1 = time.time()
    total = t1-t0
    print(total)
    return total



  

Nvb(x_train,y_train,x_test,y_test)
knn(x_train,y_train,x_test,y_test)

