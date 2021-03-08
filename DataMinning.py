
from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime
import pandas as pd
import csv


df = pd.DataFrame()
i = 1
fmt = "%d %b %y"
rvs = {}
rv = {}

for i in range(1 , 100):
    
    url = "https://www.whatuni.com/university-course-reviews/"  
    if i > 1:
        
        url = url + "?pageno=" + str(i)
    r = requests.get(url)
    soup = bs(r.content, features="lxml")

    info = soup.find(class_ = "rev_lst")

    info_row = info.find_all (class_ = 'rlst_row')
    reviews = info.find_all(class_ = 'rate_new')
    

    
    for index, row in enumerate(info_row):
        rvs = {}
        w = enumerate(rvs)
        rvs['School'] = row.find('h2').text
        Date = row.find(class_= 'rev_dte').text
        cleanDate = datetime.strptime(Date, fmt).date()
        cleanDate = cleanDate.strftime("%d %B %Y")
        rvs ['Date'] = cleanDate
        Deg = row.find ('h3')
        if Deg is None:
            Deg == ''
        else:
            Deg = Deg.text
        rvs ['Degree'] = Deg
        rv.update({str(i) +"_"+ str(index):rvs})

        step1 = row.select("div[class=rate_new]")
        for rows in step1:            
            if rows.find(class_ = 'rw_qus_des') and rows.find(class_ = 'rw_qus_des').text == "How many contact hours per week do you have?" :
                
              txt = str(rows.find(class_ = 'rw_qus_des').text.replace("\n", ""))
                
            elif rows.find(class_ = 'cat_rat') is not None:
              txt = str(rows.find(class_ = 'cat_rat').text.replace("\n", ""))
            else:
                pass
        
            if rows.find(class_ = 'rev_dec') is None: 
              txt2 = ""    
            else:
              txt2 = rows.find(class_ = 'rev_dec').text.replace("\n", "")
            rvs[txt] = txt2
            
            if rows.find(class_ = 'ml5 rat rat5'):
              txt3 = 5
            elif rows.find(class_ = 'ml5 rat rat4'):
              txt3 = 4
            elif rows.find(class_ = 'ml5 rat rat3'):
              txt3 = 3
            elif rows.find(class_ = 'ml5 rat rat2'):
              txt3 = 2
            elif rows.find(class_ = 'ml5 rat rat1'):
              txt3 = 1
            else:
              txt3 = "NaN"
            
            rvs[txt + " Rating"] = txt3
        df = pd.DataFrame.from_dict(rv, orient='index')
        df.to_csv("RawData.csv")
