import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from random import random
from time import sleep
apiurl="https://www.baidu.com/s?ie=UTF-8&wd="
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}

def baiduSpider(que:str, onlyFindSite=""):
    if onlyFindSite:
        onlyFindSite=" site:"+onlyFindSite.replace(" ","")
    r=requests.get(apiurl+que.replace("\n","").replace(" ","+")+onlyFindSite,headers=headers)
    if r.text.find("wappass.baidu.com")!=-1:
        dri=webdriver.Chrome()
        dri.get(apiurl+que.replace("\n","").replace(" ","+")+onlyFindSite)
        sleep(4+random())
        text=dri.page_source
        dri.quit()
    else:
        text=r.text
    bsobj = BeautifulSoup(text, features="html.parser")
    search_results = bsobj.find_all('div', {'class': 'result c-container'})
    regex=r'href=".+?"'
    ans=[]
    for item in search_results:
        ans.append(str(re.search(regex,str(item),flags=0).group(0)[6:-1]))
        ans[-1]=requests.get(ans[-1],headers=headers).url
        yield ans[-1]

def mofanggexinSpider(url):
    r=requests.get(url,headers=headers)
    bsobj = BeautifulSoup(r.text, features="html.parser")
    b=bsobj.find(id="q_indexkuai321").table.tbody
    if b:
        ans=str(bsobj.find(id="q_indexkuai321").table.tbody.tr.td)[4:-5].replace("<br/>","\n")
    else:
        ans=str(bsobj.find(id="q_indexkuai321").table.tr.td)[4:-5].replace("<br/>","\n")
    for i in ["<div>","</div>","："]:
        ans=ans.replace(i,"")
    for i in "ABCDEFG":
        ans=ans.replace(i,f"\033[0;30;43m{i}\033[0m")
    return ans

def manfen5Spider(url):
    r=requests.get(url,headers=headers)
    ans=re.search('http://img2.+\'',r.text,flags=0).group(0)[:-1]
    return ans

def zybangSpider(url):
    r=requests.get(url,headers=headers)
    bsobj = BeautifulSoup(r.text, features="html.parser")
    if not bsobj.find(id="good-answer"):
        return ""
    b=bsobj.find(id="good-answer").table
    try:
        if b:
            ans=str(bsobj.find(id="good-answer").table.tbody.tr.td)[4:-5].replace("<br/>","\n")
        else:
            ans=str(bsobj.find(id="good-answer").dd.span)[6:-7].replace("<br/>","\n")
    except:
        return ""
    for i in ["<span>","</span>","<div>","</div>","："," "]:
        ans=ans.replace(i,"")
    for i in "ABCDEFG":
        ans=ans.replace(i,f"\033[0;30;43m{i}\033[0m")
    return ans

def findAnswer(que,onlyFindSite=""):
    vis=set()
    for i in baiduSpider(que,onlyFindSite):
        if i.find("mofangge")!=-1 and "mofangge" not in vis:
            yield mofanggexinSpider(i)
            vis.add("mofangge")
        elif i.find("zybang")!=-1 and "zybang" not in vis:
            yield zybangSpider(i)
            vis.add("zybang")
        elif i.find("manfen5")!=-1 and "manfen5" not in vis:
            yield manfen5Spider(i)
            vis.add("manfen5")
        

if __name__ == '__main__':

    for i in baiduSpider("CO2","www.zybang.com"):
        print(i)
 