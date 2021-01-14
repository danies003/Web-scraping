#!/usr/bin/env python
# coding: utf-8

# # DOE

# In[2]:
from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from scraping.models import Job
import urllib.request as req
import pandas as pd
import bs4
import os
import psycopg2
class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options):


    
    
       



        # # NSF

        # In[3]:




        url="https://www.nsf.gov/news/"
        request=req.Request(url, headers={"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")


        root=bs4.BeautifulSoup(data, "html.parser")
        links=root.find('div',class_="col-md-12 l-add__border")
        list1={'title':[],'href':[],'time':[]}
        for a in links.find_all("div", {"class":"media l-media"}):
            for b in a.find_all("div", {"class":"media-body"}):

                for c in b.find_all("span", {"class":"l-media__date" }):
                        list1['time'].append(c.get_text())

                for d in b.find_all("a"):
                        list1['title'].append(d.get_text())


                        if "https://" in d['href']:

                            list1['href'].append(d['href'])

                        else:
                            list1['href'].append("https://www.nsf.gov"+d['href'])




        NSF = pd.DataFrame(list1, columns=['time', 'title', 'href'])






        # # FAA 

        # In[4]:



        url="https://www.faa.gov/news/"
        request=req.Request(url, headers={"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")


        root=bs4.BeautifulSoup(data, "html.parser")
        links=root.find('article',class_="content")
        list1={'title':[],'href':[],'time':[]}
        for a in  links.find_all("div", {"class":"newsItem"}):   
            for p in a.find_all("p", {"class":"join"}):
                for small in p.find_all("small"):
                    for btag in small.find_all("b"):

                        list1['time'].append(btag.get_text())


            for h3 in a.find_all("h3"):
                   for atag in h3:

                        list1['title'].append(atag.get_text())


                        if "https://" in atag['href']:

                            list1['href'].append(atag['href'])

                        else:    

                            list1['href'].append("https://www.faa.gov"+atag['href'])




        FAA = pd.DataFrame(list1, columns=['time', 'title', 'href'])





        # # NIST

        # In[5]:



        url="https://www.nist.gov/news-events/news"
        request=req.Request(url, headers={"user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")


        root=bs4.BeautifulSoup(data, "html.parser")
        links=root.find('div',class_="nist-block nist-block--news")
        list1={'title':[],'href':[],'time':[]}
        for a in  links.find_all("article", {"class":"nist-teaser"}):    
                for b in  a.find_all("div", {"class":"nist-teaser__content-wrapper"}): 
                    for time in b.find_all("time"):

                        list1['time'].append(time.get_text())

                    for title in b.find_all("span"):

                        list1['title'].append(title.get_text())

                    for p in b.find_all("a"):
                            if "https://" in p['href']:

                                list1['href'].append(p['href'])

                                print("")
                            else:    

                                list1['href'].append("https://www.nist.gov"+p['href'])
                                print("")


        NIST = pd.DataFrame(list1, columns=['time', 'title', 'href'])

        #FCCguideline

        url = "https://www.fcc.gov/reports-research/guides"
        request = req.Request(url, headers={"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find("div", class_='view-content')
        list = {'title': [], 'href': [], 'time': []}  # 這個清單有兩個column name
        for text in links.find_all('header'):
            list['title'].append(text.get_text().strip())
        for text in links.find_all('header'):
            for b in text.find_all('a'):
                list['href'].append("https://www.fcc.gov/" + b['href'])
        for c in links.find_all('span', class_='date-display-single'):
            list['time'].append(c.text)

        FCCGuideline = pd.DataFrame(list, columns=['time', 'title', 'href'])

        #USFCCreports
        url = "https://www.fcc.gov/reports-research/reports"
        request = req.Request(url, headers={
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find("div", class_='view-content')
        list = {'title': [], 'href': [], 'time': []}  # 這個清單有兩個column name
        for text in links.find_all('header'):  # nasty loop，loop內的loop
            list['title'].append(text.get_text().strip())  # strip把空白見用掉 \n
        for a in links.find_all('a'):
            list['href'].append("https://www.fcc.gov/" + a['href'])
        for c in links.find_all('span', class_='date-display-single'):
            list['time'].append(c.text)

        FCCreport=pd.DataFrame(list, columns=['time','title','href'])


        #USFDA

        url = 'https://www.fda.gov/news-events/fda-newsroom/press-announcements'
        request = req.Request(url, headers={
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find('div', class_="view-content")
        list = {'title': [], 'href': [], 'time': []}
        for t in links.find_all('time'):
            list['time'].append(t.text)
        for b in links.find_all('span', class_='field-content'):
            for c in links.find_all('time'):
                c.decompose()
            list['title'].append(b.text.strip())
        for c in links.find_all('li'):
            for d in c.find_all('a'):
                list['href'].append("https://www.fda.gov/" + d['href'])

        USFDA = pd.DataFrame(list, columns=['time', 'title', 'href'])

        #USDOT
        url = "https://www.transportation.gov/newsroom/press-releases"
        request = req.Request(url, headers={
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find('div', class_="container list_news")
        list = {'title': [], 'href': [], 'time': []}
        for a in links.find_all('a', class_='node__link'):
            list['href'].append('https://www.transportation.gov/' + a['href'])
        for b in links.find_all('span', class_='field field--name-title field--type-string field--label-hidden'):
            list['title'].append(b.text)
        for c in links.find_all('time', class_='datetime'):
            list['time'].append(c.text)

        USDOT = pd.DataFrame(list, columns=['time', 'title', 'href'])


        #USDOC
        url = 'https://www.commerce.gov/news/press-releases'
        request = req.Request(url, headers={
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find('div', class_="view-content")
        list1 = {'title': [], 'href': [], 'time': []}
        for a in links.find_all('h2'):
            list1['title'].append(a.text.strip())
        for a in links.find_all('h2'):
            for b in a.find_all('a'):
                list1['href'].append('https://www.commerce.gov/' + b['href'])
        for c in links.find_all('time', class_='datetime'):
            list1['time'].append(c.text)

        USDOC = pd.DataFrame(list1, columns=['time', 'title', 'href'])


        #USOSTP
        url = 'https://www.whitehouse.gov/ostp/'
        request = req.Request(url, headers={
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find("div", class_='page-results page-results--related-content')
        list = {'title': [], 'href': [], 'time': []}
        for text in links.find_all('h2'):
            list['title'].append(text.text)
        for text in links.find_all('h2'):
            for a in text.find_all('a'):
                list['href'].append(a['href'])
        for c in links.find_all('time'):
            list['time'].append(c.text)

        USOSTP = pd.DataFrame(list, columns=['time', 'title', 'href'])

        #USFTC

        url = 'https://www.ftc.gov/news-events/press-releases'
        request = req.Request(url, headers={"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        links = root.find('div', class_="view-content")
        list = {'title': [], 'href': [], 'time': []}
        for t in links.find_all('time', class_='field field-name-field-date field-type-datetime field-label-hidden field-wrapper'):
            list['time'].append(t.text.strip())
        for b in links.find_all('span'):
            for s in b.find_all('a'):
                list['title'].append(s.text)
        for c in links.find_all('a'):
            list['href'].append("https://www.ftc.gov" + c['href'])

        USFTC = pd.DataFrame(list, columns=['title', 'time', 'href'])




        # # 建立各自panda dataframe  加上website 標籤

        # In[6]:



        NIST['website'] = 'NIST'
        FAA['website'] = 'FAA'
        NSF['website'] = 'NSF'
        FCCGuideline['website'] = 'FCCGuideline'
        USFDA['website'] = 'USFDA'
        USDOT['website'] = 'USDOT'
        USDOC['website'] = 'USDOC'
        FCCreport['website'] = 'FCCreport'
        USOSTP['website'] = 'USOSTP'
        USFTC['website'] = 'USFTC'







        # # 合成一個大的table 用時間排序

        # In[7]:


        merged_df = pd.concat([NIST, FAA, NSF, FCCreport, FCCGuideline, USFTC, USOSTP, USDOC, USDOT, USFDA])
        merged_df = merged_df[['time', 'website', 'title', 'href']]
        merged_df['time'] = pd.to_datetime(merged_df['time'])
        merged_df = merged_df.reset_index(drop=True)
        
       
          
        merged_df=merged_df.sort_values(by=['time'], ascending=False)
        merged_df=merged_df.reset_index(drop=True)
        
       
        
        # check if url in db
       
       
        DATABASE_URL ='postgres://ggtamhzvdihrif:28efb7a45be4cdb210e093c3de7a6b8c693bd87afd062f3c4c2f50d9cf6a87bf@ec2-34-238-26-109.compute-1.amazonaws.com:5432/d404hhtto3f27h'
        print(DATABASE_URL )
        from sqlalchemy import create_engine
        import psycopg2 
        import io


        merged_df.head(0).to_sql('crawing_record',DATABASE_URL, if_exists='replace',index=False) #truncates the table

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        output = io.StringIO()
        merged_df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(output, 'crawing_record', null="") # null values become ''
        conn.commit()
        
        cur.close()
        conn.close()
       