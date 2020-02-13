from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from random import randint
from random import random
from PIL import Image
import time
import requests
import myspiders
import wget
url=["https://www.zhixue.com/login.html","https://www.zhixue.com/middleweb/student#/work-list?type=1&pageIndex=1"]
driver = webdriver.Chrome()
print("打开登陆页面")
driver.get(url[0])
driver.maximize_window()
time.sleep(1+random())
print("请输入账号密码:")
driver.find_element_by_id("txtUserName").send_keys(input("账号:"))
time.sleep(random())
driver.find_element_by_id("txtPassword").send_keys(input("密码:"))
time.sleep(random())
driver.find_element_by_id("txtPassword").send_keys(Keys.ENTER)
time.sleep(1+random())

print("打开作业网址")
driver.get(url[1])
time.sleep(random())

isOnlyFindZybang=input("""
在做某些学科(如化学)时,只搜索作业帮可能更好
但做另一些学科(如英语)时,这么做反而效果不好
请问要只搜索作业帮吗[Y/n]?
""")
if isOnlyFindZybang.lower()=="y":
    isOnlyFindZybang=True
else:
    isOnlyFindZybang=False

print("点击未完成")
driver.find_element_by_xpath('//span[contains(text(),"未完成")]').click()
time.sleep(1+random())
print("开始寻找,请在十秒内点击作业")
#driver.find_element_by_class_name("get-homework-detail").click()

time.sleep(10.5)

#找到选项元素
opts=driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div/div/div[3]/div[1]/div[3]/div/div/div[position()>1]")
times=0
vis=set()
while True:
    if not driver.find_element_by_class_name("c-Formula").text in vis:
        print("发现新的问题")
        vis.add(driver.find_element_by_class_name("c-Formula").text)
        if isOnlyFindZybang:
            li=myspiders.findAnswer(driver.find_element_by_class_name("c-Formula").text,onlyFindSite="www.zybang.com")
        else:
            li=myspiders.findAnswer(driver.find_element_by_class_name("c-Formula").text)
        ansnum=0
        for i in li: #i是找到的答案(可能为文字或者图片链接)
            if len(i)!=0 :
                print("找到答案: ",end="")
                ansnum+=1
                ans=[]
                if i[:4]=="http": #如果找到的答案是图片链接
                    filename=wget.download(i)
                    im = Image.open(filename)
                    im.show()
                    break
                else: #如果找到的答案是文字
                    for ch in i:
                        if ord(ch)>=ord("A") and ord(ch)<=ord("G"):
                            ans.append(ch)
                    print(ans)
                print(i)
                break #一般第一个答案就是正确答案,如果第一个答案都不对,那下一个答案也不会好到哪去
        else:
            print("没找到")
    time.sleep(0.5)
print("退出")
driver.quit()
