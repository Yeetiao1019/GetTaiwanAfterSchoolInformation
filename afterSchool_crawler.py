#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
url="https://bsb.kh.edu.tw/afterschool/register/statistic_city.jsp"
addressList = []
nameList = []
idList = []
presidentList = []
contactPhoneList = []
pageCount = 0
tz_TW = pytz.timezone('Asia/Taipei')
dateTimeNow = datetime.now(tz_TW)
hrefUrl = 'https://bsb.kh.edu.tw/afterschool/register/'

def get_page_num(url):
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.find_all("font",{"color":"#D00000"})
    pageCount = int(results[1].text)
    return pageCount


def get_address_president_contactphone(url):      #取地址
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.select("tr.listBody > td")
    resultsLen = len(results)
    for i in range(resultsLen):
        if(i % 7 == 2):            
            title = results[i].text            
            addressList.append(title)                
        if(i % 7 == 6):
            a_item = results[i].select_one("input.searchButton")       #查詢按鈕
            if a_item:            
                get_president_and_contactphone(article_url= hrefUrl + a_item.get('onclick').replace("location.href=","").replace("'",""))                

def get_afterschool_name(url):
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.select("tr.listBody > td")
    resultsLen = len(results)
    for i in range(resultsLen):
        if(i % 7 == 1):
            name = results[i].text
            nameList.append(name)

def get_president_and_contactphone(article_url):
    req = requests.get(article_url)
    bs = BeautifulSoup(req.text, "lxml")
    results = bs.select('tr > td.listBody')     
    if results:
        idList.append(results[0].text)                 #電話
        contactPhoneList.append(results[7].text)       #電話
        presidentList.append(results[24].text)         #24:負責人 25:設立人 26:班主任

req = requests.get(url)
bs = BeautifulSoup(req.text,"lxml")
totalHref = bs.select('td.statisticBody > a')       #合計超連結
tagLen = len(totalHref)
up_page_href = totalHref[tagLen - 1]['href']   #取總計的超連結
next_page_url = hrefUrl + up_page_href
url = next_page_url + "&range=1" + '&citylink=20'       #range=1是讓頁面的共..筆顯示正常，citylink=20是讓資料從台北市開始排序
pageCount = get_page_num(url = url)
if pageCount > 0:
    for pageNum in range(1, pageCount):
        get_address_president_contactphone(url = url)
        get_afterschool_name(url = url)
        url = url.replace("pageno=" + str(pageNum) , "pageno=" + str(pageNum + 1))
        print("目前正在撈取第 " + str(pageNum) + " 頁，共有 " + str(pageCount) + " 頁")


from yattag import Doc
from yattag import indent

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
                        text("補習班代碼")
                    with tag("th"):
                        text("補習班名稱")
                    with tag("th"):
                        text("班址")
                    with tag("th"):
                        text("負責人")
                    with tag("th"):
                        text("電話")
                for id, name, address, president, contactPhone  in zip(idList, addressList, nameList, presidentList, contactPhoneList):
                    with tag("tr"):
                        with tag("td"):
                            text(id)     #放補習班代碼
                        with tag("td"):
                            text(name)     #放補習班名稱
                        with tag("td"):
                            text(address)     #放補習班地址
                        with tag("td"):
                            text(president)     #放補習班負責人
                        with tag("td"):
                            text(contactPhone)    #放補習班聯絡電話                        
                        
with open("web_crawler.html", "wt") as code:
    code.write(indent(doc.getvalue()))
    print("全部處理完成！" )