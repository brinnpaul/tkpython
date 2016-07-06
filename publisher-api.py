import requests
import json
import pandas as pd
import numpy as np
import datetime

class SP_Account():

    def __init__(self, name, abbr, username, password, pub_id):
        self.name = name
        self.abbr = abbr
        self.username = username
        self.password = password
        self.pub_id = pub_id

    def update_pw(self, pw):
        self.password = pw

SP1 = SP_Account('account-name', 'short', 'username', 'password', 'account#')
SP2 = SP_Account('account-name', 'short', 'username', 'password', 'account#')
SP3 = SP_Account('account-name', 'short', 'username', 'password', 'account#')
SP7 = SP_Account('account-name', 'short', 'username', 'password', 'account#')
SP8 = SP_Account('account-name', 'short', 'username', 'password', 'account#')

SP_Accounts = [SP1, SP7]


class SP_Report(object):

    def __init__(self,rep):
        self = self
        rep_dict = {1:'Revenue Report',2:'Traffic Report',3:'Referrer Report',4:'Advertiser Report',5:'Deal Report'}
        url_dict = {1:'/Channels/RevenueReport',2:'/Channels/TrafficReport',3:'/Channels/ReferrerReport',4:'/Channels/AdvertiserReport',5:'/Deal/DealReport'}
        try:
            lis = [1,2,3,4,5]
            if rep in lis:
                self.report_type = rep_dict.get(rep,None)
                self.url = url_dict.get(rep,None)
        except ValueError:
            print 'Choose 1-4'

    def type_update(self):
        base_url = "base_url"
        rep_dict = {'1':'Revenue Report','2':'Traffic Report','3':'Referrer Report','4':'Advertiser Report'}
        url_dict = {'1':'RevenueReport','2':'TrafficReport','3':'ReferrerReport','4':'AdvertiserReport'}
        rep = str(raw_input('Report type? \n 1: Revenue Report \n 2: Traffic Report \n 3: Referrer Report \n 4: Advertiser Report \n'))
        try:
            lis = ['1','2','3','4']
            if rep in lis:
                self.report_type = rep_dict.get(rep,None)
                self.url = base_url+url_dict.get(rep,None)
        except ValueError:
            print 'Choose 1-4'


Revenue = SP_Report(1)
Traffic = SP_Report(2)
Referrer = SP_Report(3)
Advertiser = SP_Report(4)
Deal = SP_Report(5)

SP_Reports = [Revenue, Traffic, Referrer, Advertiser]
Report_Dict = {Revenue:'channel_id', Traffic:'', Referrer:'', Advertiser:'advertiser_domain'}

#st = datetime.datetime.today()
#et = datetime.datetime.today()

def grab_date(message = 'date: '):
    i = str(raw_input(message))
    try:
        dt_start = datetime.datetime.strptime(i, '%Y,%m,%d')
    except ValueError:
        print 'Incorrect Format'
    return dt_start

def spotx_date(date):
    spotx_date = date.strftime('%Y-%m-%d')
    return spotx_date

def data(account, report, st, et):


    url_post = "post_url"
    payload = {'username':account.username,'password':account.password}
    base_url = "base_url("+account.pub_id+")"
    url_get = base_url+report.url+"?date_range="+st+"|"+et+""

    with requests.Session() as s:
        r1 = s.post(url_post,data=payload)
        r2 = s.get(url_get)
    data = r2.json()
    df = pd.DataFrame.from_dict(data['value']['data'])

    df['Date'] = pd.Series([st]*len(df.index))
    df['Account'] = pd.Series([account.abbr]*len(df.index))
    return df


def rev_all(st, et):

    Rev = []
    for a in SP_Accounts:
        df = data(a, Advertiser, st, et)
        Rev.append(df)

    df = pd.concat(Rev,ignore_index=True)
    return df

def all_dates():
    datelist = pd.date_range(pd.datetime.strptime('2016,02,22','%Y,%m,%d'), periods=3).tolist()

    dates = []
    for d in datelist:
        date = d.strftime('%Y-%m-%d')
        dates.append(date)

    all_dates = []
    for d in dates:
        e = d
        df = rev_all(d, e)
        all_dates.append(df)

    df = pd.concat(all_dates,ignore_index=True)
    return df


def yh_rev():
    info = all_dates()
    yh = ['117221','117222','112166','112167','122020','122019','122018','122017','122016','122015','122014','122012','122371','134563','134564','134565']
    yh_tags = info[info['channel_id'].isin(yh)]
    format = yh_tags[['Date','Account','channel_id','channel_name','queries','impressions','cpm']]

    return format

def mav_rev():
    info = all_dates()
    mav = ['116740','116738','120929','125962','125961','125960','125959']
    mav_tags = info[info['channel_id'].isin(mav)]

    return mav_tags


def adnet():
    info = all_dates()
    ad = ['110403','110404','112158','112159']
    ad_tags = info[info['channel_id'].isin(ad)]

    return ad_tags
