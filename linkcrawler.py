import __future__
import bs4
import urllib2 as donut
import socket
import sys
import os
Queue=list()
import sqlite3
robots=list() #global list of all the links to avoid
urlobject=list()
limit=0
global count
while (1):
    try:
        con=sqlite3.connect('webcrawler')#yo ho pycache thanks for saving it in bytecode
        print ("database has been converted to bytecode")
        break
    except:
        print("trying again")
l=con.cursor()
l.execute('''CREATE TABLE IF NOT EXISTS crawlfinaldata
                      (urlpath VARCHAR(200)  PRIMARY KEY NOT NULL UNIQUE ,urlrank FLOAT  DESC not null,urldamped FLOAT DESC NOT NULL ,backlinks DESC INT not null ,urldirectory blob )''')

class url:
    urlpath=None
    urlrank=None
    dampingrank=None
    tempparentrank=None
    lastparnet='nolink'
    ip=None
    backlinks=None
    data=None
    urlproviderlist=list()
    urldirect=None
    pol=None

def table_existence():
    global l
    try:                                                                                 #currently no use
        l.execute("SELECT * FROM  data")
        print(l)
        return 1
    except:
        return -1

def getlink (url):
    socket.setdefaulttimeout(2000)
    print("checker")
    html=donut.urlopen(url)
    html=html.read()
    html=html.replace("<scr'+'ipt","")#managing problem with python parser
    temp=list()
    soup=bs4.BeautifulSoup(html)
    for find in soup.find_all('a'):
        p=find.get('href')
        if (p.find('rel=nofollow')==-1 and p.find("javascript")==-1):
            parts=donut.urlparse.urlsplit(p)
            if (parts.scheme!=''):
                temp.append(p)
        else:
            continue
    z=len(temp)
    return [[temp],[z]]

def add(queue,value):
    queue.append(value)

def pop(queue):
    return queue.pop(0)


#page rank algo is implemented in function database
def database(urlpath,urlparentrank,outlinks,urldirector,):
    l.execute('''select COUNT (*) FROM crawlfinaldata''')
    con.commit()
    l1=l.fetchone()
    print(l1,"database")
    if (l1[0]==None or l1[0]==0):
        damper=0.15
    else:
        print(l1)
        damper=0.15/l1[0]
    print(urlpath)
    l.execute('''SELECT  urlrank, urldamped, backlinks FROM crawlfinaldata WHERE urlpath=?''', (urlpath,))
    con.commit()
    temp=l.fetchall()
    if (len(temp)==0):
        rank=0.85*urlparentrank/float(outlinks)
        print("case1")
    elif (temp[0][0]==0):
        if outlinks==0:
            rank=0
            print("case2")
        else:
            rank = 0.85 * urlparentrank/float(outlinks)
            print("case3")
    else:
        print (temp[0],"bliss")
        rank = 0.85 * temp[0][0]+urlparentrank/float(outlinks)
        print("case4")
    if len(temp)==0:
        backlinks = 1
    else:
        backlinks= 1+int(temp[0][2])
    print("123456")
    q=l.execute('''insert or replace into crawlfinaldata values(?,?,?,?,NULL )''',(urlpath,rank,damper,backlinks))
    con.commit()
    print(rank,backlinks,damper,"123")
    return rank+damper


#page rank exceeding 1




fill=None

def page_mechanism(urlmain):
    global l
    global fill
    global q
    if fill==None:
        fill=0
        link=url.urlpath
        urlobject.append(url())
        urlobject[fill].urlpath=urlmain
        urlobject[fill].dampingrank=()
        urlobject[fill].tempparentrank=0
        urlobject[fill].backlinks=0
        urlobject[fill].pol=0
        urlobject[fill].urlproviderlist=list()
        add(Queue,urlobject[fill])
        print (urlobject[fill].urlpath)
    while (Queue!=None):
        print (1)
        linktemp=pop(Queue)
        rank=linktemp.urlrank
        print ("12",linktemp.urlpath)
        q1=getlink(linktemp.urlpath)
        len1=len(q1)
        print(len(linktemp.urlpath),linktemp.tempparentrank,linktemp.pol)
        if fill==0:
            temper=0
        else:
            for i in linktemp.urlproviderlist:
                if linktemp.lastparent!=i:
                    temper =database(linktemp.urlpath, linktemp.tempparentrank, linktemp.pol, None)
        global limit
        limit=limit+1
        print(limit,"is this what we want")
        for i in q1[0][0]:
            fill=fill+1
            urlobject.append(url)
            urlobject[fill].urlpath=i
            urlobject[fill].lastparent=linktemp.urlpath
            print(temper,"check error")
            urlobject[fill].tempparentrank=temper
            urlobject[fill].pol=len1
            urlobject[fill].urlproviderlist.append(linktemp.urlpath)
            add(Queue,urlobject[fill])



def main ():
    q=input("please enter link in quotation")
    page_mechanism(q)

main()





























