import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
style.use('ggplot')
from matplotlib import pyplot as plt

import matplotlib.dates as mdates


import Tkinter as tk
import ttk

import os
import threading

import time
import datetime

import urllib2
import json

import pandas as pd
import numpy as np

f = plt.figure()
#f = Figure(figsize=(5,4), dpi=100)

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Helvetica", 10)
SMALL_FONT= ("Helvetica", 8)

wl_Account = "null"
wl_userName = "null"
wl_passWord = "null"

wl_password1 = "###"
wl_password2 = "###"
wl_password3 = "###"
wl_password4 = "###"

wl_org_ID = "null"
wl_fill_min = 0
wl_start_date = "figure out some button"

darkColor = "#183A54"
lightColor = "#00A3E0"

class Account():

    def __init__(self, name, username, password, org_id):
        self.name = name
        self.username = username
        self.password = password
        self.org_id = org_id

    def update_pw(self, pw):
        self.password = pw

Adap1 = Account('Adap1', 'email', 'pass####', 'account#')
Adap2 = Account('Adap2', 'email', 'pass####', 'account#')
Adap3 = Account('Adap3', 'email', 'pass####', 'account#')
Adap4 = Account('Adap4', 'email', 'pass####', 'account#')

class Report():

    def __init__(self, keys = ['campaign','site'], metrics = ['ad_attempts','ad_impressions']):
        self.keys = keys
        self.metrics = metrics

    def update_key(self, key):
        self.keys = key

    def update_metric(self, metric):
        self.metrics = metric

    def list_keys(self):
        key = []
        return key

    def list_metrics(self):
        metric = []
        return metric


url_base = "base_url"
adict = {"Adap1": Adap1, "Adap2": Adap2, "Adap3": Adap3, "Adap4": Adap4}

def acct():
    while True:
        account = raw_input(r'Adap1, Adap2, Adap3, or Adap4? ')
        result = adict.get(account,None)
        if result:
            return result


def grab_date(message = 'date: '):
    i = str(raw_input(message))
    try:
        dt_start = datetime.datetime.strptime(i, '%Y,%m,%d')
    except ValueError:
        print 'Incorrect Format'
    return dt_start

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def changeAccount(toWhich, UN, PW, oID):
    global wl_Account
    global wl_userName
    global wl_passWord
    global wl_org_ID

    wl_Account = toWhich
    wl_userName = UN
    wl_passWord = PW
    wl_org_ID = oID

def changeFill():

    fillQ = tk.Tk()
    fillQ.wm_title("Periods?")
    label = ttk.Label(fillQ, text = "Choose a fill rate at which to cut off the whitelist.")
    label.pack(side="top",fill="x",pady=10)

    e = ttk.Entry(fillQ)
    e.insert(0,10)
    e.pack()
    e.focus_set()

    def callback():
        global wl_fill_min

        fill_rate = (e.get())

        wl_fill_min = fill_rate
        fillQ.destroy()

    b = ttk.Button(fillQ, text = "Submit", width = 10, command = callback)
    b.pack()
    tk.mainloop()

def changePassword(account):

    passQ = tk.Tk()
    passQ.wm_title("Password?")
    label = ttk.Label(passQ, text = "Update password for account:")
    label.pack(side="top",fill="x",pady=10)

    e = ttk.Entry(passQ)
    e.insert(0, "Password")
    e.pack()
    e.focus_set()

    def callback():
        global wl_password1
        global wl_password2
        global wl_password3
        global wl_password4

        pw = (e.get())

        if account == 'adap1':
            wl_password1 = pw
        elif account == 'adap2':
            wl_password2 = pw
        elif account == 'adap3':
            wl_password3 = pw
        elif account == 'adap4':
            wl_password4 = pw
        passQ.destroy()

    b = ttk.Button(passQ, text = "Submit", width = 10, command = callback)
    b.pack()
    tk.mainloop()

def cost(acct):

    plt_url1 = "url1"+acct.username+"&pw="+acct.password+"&s=1"
    plt_url2 = "url2"
    plt_url_base = "base_url"

    keys = ['campaign','date']
    metrics = ['ad_attempts','ad_impressions','cost']

    def read_clean_data():
        dt = datetime.datetime.utcnow()
        dt64 = np.datetime64(dt)
        ts = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        current_timestamp = str(int(ts))

        st = datetime.date(2015,07,01)
        st64 = np.datetime64(st)
        ss = (st64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        start_timestamp = str(int(ss))

        plt_url_custom = plt_url_base + "reporting/run_report?org_id="+acct.org_id+"&keys="+','.join(keys)+"&metrics="+','.join(metrics)+"&start_date="+start_timestamp+"&end_date="+current_timestamp+""

        req1 = urllib2.Request(plt_url1)
        response = urllib2.urlopen(req1)
        cookie = response.headers.get('Set-Cookie')

        # Use the cookie in subsequent requests
        req2 = urllib2.Request(plt_url_custom)
        req2.add_header('cookie', cookie)
        response = urllib2.urlopen(req2)

        for line in response:
            obj = json.loads(line)
            columns = obj['columns']
            data = obj['data']
            l = []
            for d in data:
                l += [d['row']]
            df = pd.DataFrame(l, index=None, columns=columns)

        df.columns = keys+metrics

        df['ad_attempts'] = df['ad_attempts'].astype(float)
        df['ad_impressions'] = df['ad_impressions'].astype(float)
        df['cost'] = df['cost'].astype(float)
        df = df.groupby(df['date']).sum()
        df['fill rate'] = df['ad_impressions']/df['ad_attempts']
        df['date'] = df.index
        #frame = frame[frame['Media'].notnull()]
        #frame = frame[~frame['Media'].str.contains('Site')]
        return df
    data = read_clean_data()
    return data


data1 = cost(Adap1)
data2 = cost(Adap2)
data3 = cost(Adap3)
data4 = cost(Adap4)

graph_param = 'fill rate'

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
y1 = np.array(data1[graph_param]).tolist()
x1 = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in np.array(data1['date'])]

y2 = np.array(data2[graph_param]).tolist()
x2 = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in np.array(data2['date'])]

y3 = np.array(data3[graph_param]).tolist()
x3 = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in np.array(data3['date'])]

y4 = np.array(data4[graph_param]).tolist()
x4 = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in np.array(data4['date'])]

#dates = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in np.array(data1['date'])]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
a.plot(x1, y1, lightColor, label="Adap1")
a.plot(x2, y2, label = 'Adap2')
a.plot(x3, y3, label = 'Adap3')
a.plot(x4, y4, label = 'Adap4')
a.set_title(graph_param)
a.set_xlabel('Date')
a.set_ylabel(graph_param)
a.legend()
plt.gcf().autofmt_xdate()


def print_whitelist():
    global wl_Account
    global wl_userName
    global wl_passWord
    global wl_org_ID

    if wl_Account == "null":
        popupmsg("Please choose an account to generate a whitelist for.")
    else:
        url1 = "url1"+wl_userName+"&pw="+wl_passWord+"&s=1"
        url_base = "base_url"

        def dates():
            global wl_org_ID
            dt = datetime.datetime.utcnow()
            dt64 = np.datetime64(dt)
            ts = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
            current_timestamp = str(int(ts))

            st = datetime.date(2015, 7,01)
            st64 = np.datetime64(st)
            ss = (st64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
            start_timestamp = str(int(ss))

            url_custom = url_base + "reporting/run_report?org_id="+wl_org_ID+"&keys=campaign,site&metrics=ad_attempts,ad_impressions&start_date="+start_timestamp+"&end_date="+current_timestamp+""
            return url_custom

        def pull_data():
            req1 = urllib2.Request(url1)
            response = urllib2.urlopen(req1)
            cookie = response.headers.get('Set-Cookie')

            # Use the cookie in subsequent requests
            req2 = urllib2.Request(dates())
            req2.add_header('cookie', cookie)
            response = urllib2.urlopen(req2)

            for line in response:
                obj = json.loads(line)
                columns = obj['columns']
                data = obj['data']
                l = []
                for d in data:
                    l += [d['row']]
                df = pd.DataFrame(l, index=None, columns=columns)

            df.columns = ['Campaign','Media','Ad Attempts','Ad Impressions']
            return df

        def clean_data():
            df = pull_data()

            df = df[df['Media'].notnull()]
            df = df[~df['Media'].str.contains('Site')]
            df['Ad Attempts'] = df['Ad Attempts'].astype(float)
            df['Ad Impressions'] = df['Ad Impressions'].astype(float)
            df = df.groupby(df['Media']).sum()
            df['Fill Rate'] = df['Ad Impressions']/df['Ad Attempts']
            return df

        def name_data(): #removes low fill rate and deposits finished whitelist in reporting\ad%_d%.m%.Y%\
            global wl_fill_min
            global wl_Account
            ad = wl_Account
            if not os.path.exists(r'C:\\Users\\CP\\Documents\\api_whitelist\\'+str(ad)+'_'+str(time.strftime("%m.%d.%Y"))):
                os.makedirs(r'C:\\Users\\CP\\Documents\\api_whitelist\\'+str(ad)+'_'+str(time.strftime("%m.%d.%Y")))

            frame = clean_data()
            frame = frame[frame['Fill Rate'] >= float(wl_fill_min)/100]
            path = r'C:\\Users\\CP\\Documents\\api_whitelist\\'+str(ad)+'_'+str(time.strftime("%m.%d.%Y"))+'\\'+str(ad)+'_'+str(time.strftime("%m.%d.%Y"))+'_'+str(float(wl_fill_min))+'%'+'.csv'
            frame.to_csv(path)
            while True:
                popupmsg("Whitelist finished!")

        t = threading.Thread(target=name_data)
        t.start()
        popupmsg("Whitelist is being generated!")

class Adap_API(tk.Tk):

    def __init__(self, *args, **kwargs):
        global wl_password1
        global wl_password2
        global wl_password3
        global wl_password4

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self) ## filepath\clinticon.ico ico file with filepath to put in icon
        tk.Tk.wm_title(self, "White List Generator")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        AccountChoice = tk.Menu(menubar, tearoff=0)
        AccountChoice.add_command(label="Adap 1", command = lambda: changeAccount("Adap 1","email",wl_password1,"account#"))
        AccountChoice.add_command(label="Adap 2", command = lambda: changeAccount("Adap 2","email",wl_password2,"account#"))
        AccountChoice.add_command(label="Adap 3", command = lambda: changeAccount("Adap 3","email",wl_password3,"account#"))
        AccountChoice.add_command(label="Adap 4", command = lambda: changeAccount("Adap 4","email",wl_password4,"acccount#"))
        menubar.add_cascade(label="Adap.tv Account", menu=AccountChoice)

        FillChoice = tk.Menu(menubar, tearoff=0)
        FillChoice.add_command(label="Fill Rate", command = lambda: changeFill())
        menubar.add_cascade(label="Fill Rate", menu=FillChoice)

        UpdatePassword = tk.Menu(menubar, tearoff=0)
        UpdatePassword.add_command(label="Adap 1", command = lambda: changePassword('adap1'))
        UpdatePassword.add_command(label="Adap 2", command = lambda: changePassword('adap2'))
        UpdatePassword.add_command(label="Adap 3", command = lambda: changePassword('adap3'))
        UpdatePassword.add_command(label="Adap 4", command = lambda: changePassword('adap4'))
        menubar.add_cascade(label="Password", menu=UpdatePassword)

        tk.Tk.config(self,menu=menubar)

        self.frames = {}

        for F in (start_page, whitelist_page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(start_page)


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class start_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="White List Generator", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(whitelist_page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree") ## command = quit??
        button2.pack()

class whitelist_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Generate a Whitelist", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(start_page))
        button1.pack()

        button2 = ttk.Button(self, text="Generate Whitelist!", command = lambda: print_whitelist())

        button2.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = Adap_API()
#ani = animation.FuncAnimation(f,cost,interval=2000000)
app.mainloop()
