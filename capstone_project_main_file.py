# -*- coding: utf-8 -*-
"""Capstone_project_main_file.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KGGJ4I6prZM5qziXqgXEir6lzKRaGlEA
"""

!pip install pandas

!pip install lazypredict
!pip install tweet-preprocessor
!pip install -U pip setuptools wheel
!pip install spacy
nltk.download('stopwords')

import nltk

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd

import string
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from lazypredict.Supervised import LazyClassifier
import preprocessor as p
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import spacy 

#nlp = spacy.load('en_core_web_sm')
stopword = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()
# %matplotlib inline

from google.colab import drive
drive.mount('/gddrive')

# df = pd.read_csv('/gddrive/MyDrive/Colab Notebooks/Marathi_tweet_sentiment/covid19.csv')
df = pd.read_csv('/content/pred_data1.csv')

clean_data =df.iloc[:,0].apply(lambda x: p.clean(x))

"""Data Preprocessing/Module 3"""

# data clean methods
stopword=stopword+['brt','xfxfxcxe','xfxfxxvaccin']

def clean_text(text):
    text_lc = "".join([word.lower() for word in text if word not in string.punctuation]) # remove puntuation
    text_rc = re.sub('[0-9]+', '', text_lc)
    #after tweepy preprocessing the colon symbol left remain after    
    tweet = re.sub(r':', '', text_rc)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
    #filter using NLTK library append it to a string
    tokens = re.split('\W+', tweet)    # tokenization
    text = [word for word in tokens if word not in stopword]  # remove stopwords
    return text

df['clean_tweets'] = clean_data.apply(lambda x:clean_text(x))
df['clean_tweets']= df['clean_tweets'].apply(lambda x: ' '.join(x))

df

df.head()

sns.countplot(df['label'])

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

df['clean_tweets']

"""Build Algorithm & Predict Accurcy/Module 4"""

X=df['clean_tweets']
y=df['label']
tfidf=TfidfVectorizer()
X=tfidf.fit_transform(X)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0,stratify=y)
print('shape of x',X.shape)
clf=LinearSVC()
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)
print(classification_report(y_test,y_pred))

def run_svm(df):
    X=df['clean_tweets']
    y=df['label']
    tfidf=TfidfVectorizer()
    X=tfidf.fit_transform(X)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0,stratify=y)
    print('shape of x',X.shape)
    clf=LinearSVC()
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    print(classification_report(y_test,y_pred))
    
    return tfidf,clf

# Commented out IPython magic to ensure Python compatibility.
# %%time
# tfidf,clf=run_svm(df)

x=df['clean_tweets']
clf.predict(tfidf.transform(x))

rf = RandomForestClassifier()
rf.fit(X_train,y_train)
predict=rf.predict(X_test)
accuracy_score(y_test,predict)

dt = DecisionTreeClassifier()
dt.fit(X_train,y_train)
predict=dt.predict(X_test)
accuracy_score(y_test,predict)

from sklearn.linear_model import LogisticRegression
logmodel = LogisticRegression(random_state=400 )
logmodel.fit(X_train,y_train)
log_predictions = logmodel.predict(X_test)
from sklearn.metrics import confusion_matrix,f1_score
confusion_matrix(y_test,log_predictions)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,log_predictions)

sns.set_style('darkgrid')
x_axis=['SVM','RandomForest','DescisionTree','logisticRegression']
y_axis=[92.42,91.85,92.28,88.14]
sns.barplot(x_axis,y_axis)
plt.show()

"""Module Building/Module 5"""

import joblib

rf = RandomForestClassifier()
rf.fit(X_train,y_train)

# save the model to disk
filename = 'RF_finalized_model.sav'
joblib.dump(rf, filename)

# load the model from disk
loaded_model = joblib.load(filename)
result = loaded_model.score(X_test, y_test)
print(result)

#TF-IDF

from sklearn.feature_extraction.text import TfidfVectorizer

tfidfVectorizer = TfidfVectorizer() 
tfidfVector = tfidfVectorizer.fit_transform(df['clean_tweets'])

text = 'RT @zlj517: Facing #COVID19, the British government suggested #HerdImmunity by infection regardless of the right to life and health. Across\xe2\x80\xa6'

def predict_sentiment(text):
  test_doc = ' '.join(clean_text(text))
  pd.DataFrame([test_doc]).iloc[0]
  test_vect = tfidfVectorizer.transform(pd.DataFrame([test_doc]).iloc[0])
  test_tfidf = pd.DataFrame(test_vect.toarray(), columns=tfidfVectorizer.get_feature_names()).iloc[:,0:]
  test_predict = rf.predict(test_tfidf)[0]
  print('Tweet: ',text,' \nPredicted sentiment of tweet: ',test_predict)

predict_sentiment(text)