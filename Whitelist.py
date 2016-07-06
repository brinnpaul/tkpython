# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:44:21 2015

@author: CP
"""

import pandas as pd
import time
import os

def list_files(path):
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files
    
def read_file(): ## folder_raw_wl -> choose folder where to keep reports from adapt
    folder_raw_wl = r'C:\\Users\\CP\\documents\\raw_white'
    print list_files(folder_raw_wl)
    inputted = raw_input("Type file name from above list: ") 
    #inputted = 'ad1_06.10.15.csv'
    path = folder_raw_wl +'\\' + inputted 
    frame = pd.read_csv(path,index_col=None,header=0)
    frame.columns = ['Campaign','Media','Ad Attempts','Ad Impressions']
    return frame
    
def fr(): #creates fill column
    frame = read_file()
    frame['Fill Rate'] = frame['Ad Impressions']/frame['Ad Attempts']
    return frame
      
def rbs(): #removes blocked sites
    frame = fr()
    frame = frame[frame['Media'].notnull()]
    return frame[~frame['Media'].str.contains('Site')]

def rlf(): #removes low fill rate
    frame = rbs()
    inputted_fill_rate = raw_input("Fill Rate cutoff? (Format: 0.nn): ")
    return frame[frame['Fill Rate'] >= float(inputted_fill_rate)]
    
def sbc(): #splits up dataframe by spotx account
    accounts = []
    frame = rlf()
    while True:
        acc = raw_input("CP-TVW-LUXE-RRI-YP: Enter one at a time; enter 'end' to load media lists: ")
        if acc == 'end':
            break
        else:
            accounts.append(acc)
    wll = []
    for ac in accounts:
        wl = frame[frame['Campaign'].str.startswith(ac)]
        wll.append(wl)
    return wll

def sbch(): #splits up dataframes by channel
    if not os.path.exists(r'C:\\Users\\CP\\Documents\\Python_WL\\'+str(time.strftime("%d.%m.%Y"))):
        os.makedirs(r'C:\\Users\\CP\\Documents\\Python_WL\\'+str(time.strftime("%d.%m.%Y")))
    frame = sbc()
    for f in frame:
        channels = f['Campaign'].unique()
        for ch in channels:
            wl_ch = f[f['Campaign'] == ch]
            path = r'C:\\Users\\CP\\Documents\\Python_WL\\'+str(time.strftime("%d.%m.%Y"))+'\\'+str(ch)+'_'+str(len(wl_ch))+'.csv'
            #if len(wl_ch) > 50:
            wl_ch.to_csv(path)
            #path = r'C:\\Users\\CP\\Documents\\Python_WL\\'+str(time.strftime("%d.%m.%Y"))+'\\'+str(ch)+'.csv'
            #wl_ch.to_csv(path)
            
