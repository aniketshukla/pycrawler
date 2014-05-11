__author__ = 'Aniket'
import __future__
import bs4
import urllib2 as donut
import socket
import hashlib
import codecs
import time
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
        print ("connected to database...")
        break
    except:
        print("blimey!....trying again")
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
    html=donut.urlopen(url)
    html=html.read()
    html=html.replace("<scr'+'ipt","")#managing problem with python parser)
    temp=list()
    soup=bs4.BeautifulSoup(html)
    for find in soup.find_all('a'):
        p=find.get('href')
        try:
            p=str(p)
        except:
            p=p.replace("u'\u200e","")
        if (p.find('rel=nofollow')==-1 and p.find('mailto')==-1 and p.find('javascript')==-1 ) :
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
    q=l1
    print(l1,"database storing begins")
    if (l1==None or l1==0):
        damper1=0.15
    else:
        print(l1)
        damper1=0.15/l1[0]
    print(urlpath)
    l.execute('''SELECT  urlrank, urldamped, backlinks FROM crawlfinaldata WHERE urlpath=?''', (urlpath,))
    con.commit()
    temp=l.fetchall()
    if (len(temp)==0):
        rank=0.85*urlparentrank/float(outlinks)
    elif (temp[0][0]==0):
        if outlinks==0:
            rank=0
        else:
            rank = 0.85 * urlparentrank/float(outlinks)
    else:
        rank = 0.85 * temp[0][0]+urlparentrank/float(outlinks)
    if len(temp)==0:
        backlinks = 1
    else:
        backlinks= 1+int(temp[0][2])
    if len(temp)==0:
        damper=damper1
    elif temp[0][1]==0:
        damper=damper1
    else:
        damper=-temp[0][1]+damper1
    print("123456")
    q=l.execute('''insert or replace into crawlfinaldata values(?,?,?,?,NULL )''',(urlpath,rank,damper,backlinks))
    con.commit()
    print("page_rank is",rank+damper)
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
    while (Queue!=None):
        linktemp=pop(Queue)
        print("popped element",linktemp.urlpath)
        rank=linktemp.urlrank
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
        for i in q1[0][0]:
            fill=fill+1
            urlobject.append(url)
            urlobject[fill].urlpath=i
            urlobject[fill].lastparent=linktemp.urlpath
            urlobject[fill].tempparentrank=temper
            urlobject[fill].pol=len1
            urlobject[fill].urlproviderlist.append(linktemp.urlpath)
            add(Queue,urlobject[fill])



def main ():
    q=input("starting the execution...please enter the link>>>>")
    page_mechanism(q)

main()





























