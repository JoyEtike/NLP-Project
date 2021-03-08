import numpy as np
import pandas as pd
from IPython.display import display

def lower(data):
    df = pd.read_csv (data)
    df2 = df.fillna('').astype(str).apply(lambda x: x.str.lower())
    df2 = df2.replace( {'n\’t' : ' not','n\'t': " not", "\'ve": " have", 
                  "\’ve": " have","\'m": " am", "\’m": " am", 
                  "wo not": "will not", "\'ll" : " will",
                 "\’ll": " will", "tbh": "to be honest", "idk":"i do not know",
                 "dunno": "do not know", "it's":"it is", "it’s":"it is", "ca not":"can not","n/a":"not applicable",
                 "havent":"have not", "ive":"i have","uni haversity":"university","uni ":"university","covid":"pandemic", "effecti havely": "effectively",
                 "supporti havely":"supportively","positi havely": "positively", "gi haven":"given","gi haves":"gives","gi have":"give",
                 "amazingi":"amazing"}, regex = True)
    return df2


def Columns (lower):
    df = lower('RawData.csv')
    df2 = df.drop(['Job Prospects','Job Prospects Rating','Course and Lecturers','Course and Lecturers Rating',"Students' Union",
                        "Students' Union Rating",'Uni Facilities','Accommodation','Accommodation Rating',
                       'Uni Facilities Rating','School','Date','Degree','Local life','Local life Rating','Societies and Sports','Societies and Sports Rating',
                        'Student Support','Student Support Rating','Facilities','Facilities Rating','How many contact hours per week do you have?'], axis = 1)
    df2 = df2.rename({"OverallReview":"Review","OverallReview_Rating":"Rating"},axis = 'columns')
    return category(df2)
    
def category(df2):
    
    Pos = ["5","4"]
    Neu = ['3']
    Neg = ["2","1"]

    df2.loc[df2['Rating'].str.contains('|'.join(Pos), case=True, na=False), 'Rating']= 1
    df2.loc[df2['Rating'].str.contains('|'.join(Neu), case=True, na=False), 'Rating']= 0
    df2.loc[df2['Rating'].str.contains('|'.join(Neg), case=True, na=False), 'Rating']= -1
    
    df2['Review'] = df2['Review'].replace('[^A-Za-z]', ' ', regex = True )
    df2['Review'].replace('', np.nan, inplace=True)
    df2.dropna(subset = ["Review"], inplace=True)
    pd.value_counts(df2['Rating']).plot.bar()
    df2.to_csv("CleanData.csv")

Columns(lower)