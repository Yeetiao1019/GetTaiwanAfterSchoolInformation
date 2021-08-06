#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import sys

url="https://bsb.kh.edu.tw/afterschool/register/statistic_city.jsp"
addressList = []
nameList = []
idList = []
presidentList = []
cityList = []
contactPhoneList = []
supervisorList = []
createtimeList = []
emailList = []
pageCount = 0
tz_TW = pytz.timezone('Asia/Taipei')
dateTimeNow = datetime.now(tz_TW)
hrefUrl = 'https://bsb.kh.edu.tw/afterschool/register/'

def get_page_num(url):  #取第二層的頁數
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.find("select",{"name":"jump"}).findAll('option')
    pageCount = int(len(results))
    return pageCount

def get_layer2_data_layer3_url(url, cityname):      #第二層的資料與第三層的班主任、負責人、聯絡電話資料
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.select("tr.listBody > td")
    resultsLen = len(results)
    for i in range(resultsLen):
            if(i % 7 == 1):
                if(results[i+1].text.strip() != ''):        #用地址的有無來判斷補習班資料是否完整
                    if(results[i].text.strip() != ''):
                        cityList.append(cityname.strip())
                        name = results[i].text.strip()
                        nameList.append(name.strip())
                else:
                    cityList.append(cityname)
                    nameList.append('此補習班資料不完整，或為網站的測試資料')
            if(i % 7 == 2):            
                if(results[i].text.strip() != ''):
                    title = results[i].text.strip()            
                    addressList.append(title.strip())       
                else:
                    addressList.append('')
            if(i % 7 == 5):
                if(results[i].text.strip() != ''):
                    createtime = results[i].text.strip()
                    createtimeList.append(createtime.strip())         
                else:
                    createtimeList.append('')         
            if(i % 7 == 6):
                a_item = results[i].select_one("input.searchButton")       #查詢按鈕的url
                if a_item:            
                    get_president_and_contactphone(article_url= hrefUrl + a_item.get('onclick').replace("location.href=","").replace("'",""))        

def get_president_and_contactphone(article_url):
    req = requests.get(article_url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.select('tr > td.listBody')
    if(results and results[1].text.strip() != 'null'): 
        if(results[0].text.strip() != ''):
            idList.append(results[0].text.strip())                 #補習班代碼
        else:
            idList.append('')
        if(results[7].text.strip() != ''):
            contactPhoneList.append(results[7].text.strip())       #電話
        else:
            contactPhoneList.append('')
        if(results[24].text.strip() != ''):
            presidentList.append(results[24].text.strip())         #24:負責人 25:設立人 26:班主任
        else:
            presidentList.append('')
        if(results[26].text.strip() != ''):
            supervisorList.append(results[26].text.strip())
        else:
            supervisorList.append('')
        if(len(results[16].select("a")) > 0):
            emailList.append(results[16].select("a")[0].text.strip())
        else:
            emailList.append('')
    else:       #假設'主管機關文件單位代碼'是空的
        idList.append('')                 #補習班代碼
        contactPhoneList.append('')       #電話
        presidentList.append('')         #24:負責人 25:設立人 26:班主任
        supervisorList.append('')
        emailList.append('')

req = requests.get(url)
bs = BeautifulSoup(req.text,"lxml") 
cityCount = 22
citytempcount = 0
citynametemplist = bs.find_all('td',{'class':'statisticCenter'}) #[cityCount].text 
totalHref = bs.select('td.statisticBody > a')       #不取合計超連結
tagLen = len(totalHref)
for pageUrl in range(tagLen - 1):                    #不取最後總計的超連結    
    if(pageUrl % 15 != 14):
        hrefnum = int(totalHref[pageUrl].text.strip())                
        if(citytempcount < 22):     # 共22個縣市
            cityname = citynametemplist[citytempcount].text.strip()
        if(hrefnum > 0):
            up_page_href = totalHref[pageUrl]['href']  
            next_page_url = hrefUrl + up_page_href
            url = next_page_url + "&range=1"          #range=1是讓頁面的共..筆顯示正常
            pageCount = get_page_num(url = url)                            
            if pageCount > 0:
                if(pageCount > 99): #該網頁無法查大於100頁的資料
                    for pageNum in range(1, 100):                
                        print("目前正在撈取 " + cityname +" 第 " + str(pageNum) + " 頁，共有 " + str(pageCount) + " 頁(此頁面只能查到第99頁)")
                        get_layer2_data_layer3_url(url = url, cityname = cityname)
                        if(len(cityList) != len(nameList) and len(cityList) != len(createtimeList) and len(cityList) != len(addressList) and len(cityList) != len(contactPhoneList) and len(cityList)!= len(presidentList) and len(cityList)!= len(supervisorList) and (len(cityList) != len(emailList))):
                            sys.exit("陣列的數量已經不一致")
                        url = url.replace("pageno=" + str(pageNum) , "pageno=" + str(pageNum +1))      
                elif(pageCount <= 99):
                    for pageNum in range(1, pageCount + 1):                
                        print("目前正在撈取 " + cityname +" 第 " + str(pageNum) + " 頁，共有 " + str(pageCount) + " 頁")
                        get_layer2_data_layer3_url(url = url, cityname = cityname)
                        if(len(cityList) != len(nameList) and len(cityList) != len(createtimeList) and len(cityList) != len(addressList) and len(cityList) != len(contactPhoneList) and len(cityList)!= len(presidentList) and len(cityList)!= len(supervisorList) and (len(cityList) != len(emailList))):
                            sys.exit("陣列的數量已經不一致")
                        url = url.replace("pageno=" + str(pageNum) , "pageno=" + str(pageNum +1))            
    elif(pageUrl % 15 == 14):        
        citytempcount = citytempcount + 1

from yattag import Doc
from yattag import indent

# 做成網頁
doc, tag, text = Doc().tagtext()
print("正在處理HTML...")
doc.asis('<!DOCTYPE html>')
with tag('html'):
    with tag('head'):
        with tag('title'):
            text("ToolBox")
        with tag("style"):
            text("table, th, td { border: 2px solid pink;  border-collapse: collapse; } th, td {  padding: 5px;  text-align: left;}")
        doc.stag("meta", charset="UTF-8")
    with tag('body'):
        with tag("h1"):
            text("臺灣補習班資料")
        with tag("h2"):
            text("資料時間："+  str(dateTimeNow))
        with tag("p"):
            with tag("table", style="width:100%"):
                with tag("tr"):
                    with tag("th"):
                        text("縣市")
                    with tag("th"):
                        text("補習班名稱")
                    with tag("th"):
                        text("立案日期")
                    with tag("th"):
                        text("地址")
                    with tag("th"):
                        text("電話")
                    with tag("th"):
                        text("負責人")
                    with tag("th"):
                        text("班主任")      
                    with tag("th"):
                        text("email")                
                for city, name, createtime, address, contactPhone, president, supervisor, email  in zip(cityList, nameList, createtimeList, addressList, contactPhoneList, presidentList, supervisorList, emailList):
                    with tag("tr"):
                        with tag("td"):
                            text(city)     #放縣市
                        with tag("td"):
                            text(name)     #放補習班名稱
                        with tag("td"):
                            text(createtime)     #放立案日期
                        with tag("td"):
                            text(address)     #放補習班地址
                        with tag("td"):
                            text(contactPhone)    #放補習班聯絡電話 
                        with tag("td"):
                            text(president)     #放補習班負責人
                        with tag("td"):
                            text(supervisor)     #放補習班班主任
                        with tag("td"):
                            text(email)     #放email
                        
with open("web_crawler.html", "wt", encoding='utf-8-sig') as code:
    code.write(indent(doc.getvalue()))
    print("HTML處理完成！" )

import csv

# 開啟輸出的 CSV 檔
with open('補習班名單.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)

    # 建立標題列
    writer.writerow(['縣市','補習班名稱','立案日期', '地址', '電話', '負責人', '班主任', '電子郵件'])

    # 寫入爬回來的資料
    for city, name, createtime, address, contactPhone, president, supervisor, email  in zip(cityList, nameList, createtimeList, addressList, contactPhoneList, presidentList, supervisorList, emailList):
        writer.writerow([city, name, createtime, address, contactPhone, president, supervisor, email])

    print("CSV處理完成！" )
print("程式結束" )