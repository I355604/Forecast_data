
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 10:10:21 2018

@author: Administrator
"""

from datetime import datetime,timedelta,date
import holidays
import pandas as pd
import numpy as np
import json
try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass
#import date
i_holidays = holidays.India()
holiday_update={}
listt=[]
hd=[]
def load_json(path):
    
    try:
        with open(path) as data_file:
            data=json.load(data_file)
        return data
    except:
        print("Json File Not Loaded ")

def date_id(data):
    dates=[]
    headers=[]
    for i in data['Header']:
        n=i.get('name')
        t=i.get('type')
        headers.append(n)
        if t=='SKUID':
            v=i.get('values')
            name1=n
        if t=='date':
            s=i.get('start')
            e=i.get('end')
            frmt=i.get('date_format')
            name2=n
            daterange = pd.date_range(s,e)
            for i in daterange:
                dates.append(i.strftime(frmt))
    x=np.array(v)
    y=np.array(dates)
    data1= np.transpose([np.tile(x,len(y)),np.repeat(y,len(x))])
    product=pd.DataFrame(data = data1.tolist(), columns = [name1,name2])
    return data1,name1,name2,product,headers
def rand_data(data,l,product):
    for i in data['Header']:
        n=i.get('name')
        t=i.get('type')
        if t=='string':
           v=i.get('values')
           str=np.random.choice(v,l)
           product[n]=str
          
           
        if t=='decimal':
            m=i.get('min')
            ma=i.get('max')
            pr=np.random.uniform(low=int(m),high=int(ma),size=l)
            product[n]=pr
        if t=='integer':
            m=i.get('min')
            ma=i.get('max')
            pr=np.random.randint(low=m,high=ma,size=l)
            product[n]=pr
    return product
def fetch_hollist(data):
    hol={}
    for i in data['Holiday']:
        n1=i.get('details')
        n2=i.get('holiday_percentage')
        n3=i.get('season_percentage')
        n4=i.get('weekends_percentage')
        hol[n1[0]]=[n1[1],n2,n3,n4]
    
    return hol
def fetch_weekdays(date,percent,oldvalue,file):
        #print(oldvalue)
        newvalue=oldvalue
        d=datetime.strptime(date,"%Y-%m-%d").date()
        day=d.strftime('%A')
        if day.lower()=='sunday' or day.lower()=='saturday':
           newvalue=oldvalue + (oldvalue * int(percent)/100)
        #print(newvalue)
        return newvalue
      
        

    


def weather_data(region,d,percent,oldvalue):
    #region='china'
    flag=0
    w={}
    dd=datetime.strptime(d,'%Y-%m-%d')
    month=dd.strftime('%B').lower()

    w={'china':{'summer':'may,june,july','autumn':'july,august,september,october','winter':'november,december,january,february'},
              'africa':{'dry':'december,january,may,june,july,august','rainy':'february,march,april,september,october,november'},
              'amazon':{'summer':'february,march,april,may,june'},
              'new zealand':{'spring':'september,october,november','summer':'december,january,february','autumn':'march,april,may','winter':'june,july,august'},
              'australia':{'spring':'september,october,november','summer':'december,january,february','autumn':'march,april,may','winter':'june,july,august'},
              'russia':{'winter':'december,january,february','spring':'march,april,may','summer':'june,july,august','autumn':'september,october,november'}
              
              } 

    ddd=np.array(region)
    
    
    
    if ddd[0] in w.keys():
        for i in w[ddd[0]]:
            if month in w[ddd[0]][i]:
                newvalue=oldvalue + (oldvalue * int(percent)/100 )    
                return newvalue
    else:
                return oldvalue
    
            
def holiday_check(data):
    for h in data["holiday_name"]:
        h1=h.get('pub_holiday')
        h2=h.get('pub_holiday_date')
    print(h1)
    print(h2)
    holiday_update= {k: v for k, v in zip(h1,h2)}
    
    
    for d in holiday_update.values():
        i_holidays.append(d)
    return i_holidays
def holilist_update(holiday_checks,datedata,percent,oldvalue):
       newvalue1=oldvalue + (oldvalue * int(percent)/100)   
       return newvalue1
       
        #print(newvalue1)        
       
        #print(newvalue1)
   
def date_check(holiday_checks,olddate):
    flag=0
    for i in holiday_checks:
        dt1=i+timedelta(days=-10)
        dt2=i+timedelta(days=10)
        if dt1<=datetime.strptime(olddate,"%Y-%m-%d").date()<=dt2:
            flag=1
            break   
    return flag

def seaholweek(data):                
    for x in data['Header']:
        h=x.get('name')
        g=x.get('description')
        if(g):
            if 'sea' in g:
                sheader=h
            if 'week' in g:
                wheader=h
            if 'hol' in g:
                hheader=h
            if 'loc' in g:
                loc=h
       
    for y in data['Holiday']:
        details=y.get('details')
        time=details[1]
        hper=y.get('holiday_percentage')
        seper=y.get('season_percentage')
        wper=y.get('weekends_percentage')
        
        
        oldweek=r.loc[(r[id]==details[0]) & (r[d]==details[1]),wheader]
        nw=fetch_weekdays(time,wper,oldweek,'s.json')
        r.loc[(r[id]==details[0]) & (r[d]==time),wheader]=nw
        
        
        
        oldsea=r.loc[(r[id]==details[0]) & (r[d]==details[1]),sheader]
        print(oldsea)
        region=r.loc[(r[id]==details[0]) & (r[d]==details[1]),loc]
        neww=weather_data(region,time,seper,oldsea)
        r.loc[(r[id]==details[0]) & (r[d]==time),sheader]=neww
        print(neww)
        
        
        
        oldday=r.loc[(r[id]==details[0]) & (r[d]==details[1]),hheader]
        olddate= r.loc[(r[id]==details[0]) & (r[d]==details[1]),d]
        ddate=np.array(olddate)
        status=date_check(holiday_checks,ddate[0])
        if status==1:
            r.loc[(r[id]==details[0]) & (r[d]==details[1]),hheader]=holilist_update(holiday_checks,time,hper,oldday)

           
def file(data):
    try:
        file=data.get("filename")            
        r.to_csv(file,index=False)
        return file    
    except:
        print("enter correct file name ")    


data=load_json(r's.json')
dataa,id,d,product,headers=date_id(data)
reg=data.get('location')
l=len(product)
r=rand_data(data,l,product)
holidays=fetch_hollist(data)
holiday_checks=holiday_check(data)
seaholweek(data)
file(data)


"""for x in holidays.keys():
    for y in data['Header']:
        h=y.get('name')
        g=y.get('description')
        
        if(g):
            if 'sea' in g:
                header=h
                oldvalue=r.loc[(r[id]==x) & (r[d]==holidays[x][0]),h]
                print(r.loc[(r[id]==x) & (r[d]==holidays[x][0]),'date'],x)"""
                






