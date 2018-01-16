# -*- coding: utf-8 -*-
import http.cookiejar
import urllib
from urllib.error import URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def GetIP():
    opener = urllib.request.build_opener()
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh - CN, zh;q = 0.8',
               'Cache-Control': 'max - age = 0',
               }

    get_url = "http://www.xicidaili.com/nt/"
    try:
        get_request  = urllib.request.Request(get_url, headers=headers)
        get_response = opener.open(get_request)
        #print(get_response.read().decode('utf-8'))
        soup = BeautifulSoup(get_response, "html.parser")
        trs = soup.findAll('tr')[1:]    #去除第一行的列名
        f = open('originip.txt','w',encoding="utf-8")
        for tr in trs:
            tdlist=tr.findAll('td')     #获取td
            f.write(tdlist[1].string+' ')  # ip
            f.write(tdlist[2].string+' ')  # port
            if tdlist[3].find('a'):
                f.write(tdlist[3].find('a').string)  # addr
            f.write('\n')
        f.close()
    except URLError as e:
        print(e)
def Visit():
    f = open('originip.txt', 'r', encoding="utf-8")
    while 1:
        lines = f.readlines(100000)
        if not lines:
            break
        for line in lines:
            ip = line.split()

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://'+ip[0]+':'+ip[1])
            chrome = webdriver.Chrome(executable_path=r'D:\Programme\chromedriver.exe',chrome_options=chrome_options)
            try:
                chrome.get('https://www.logicjake.xyz/?p=152')
                # chrome.get('http://www.baidu.com')
                # elem = chrome.find_element_by_id("kw")
                # elem.send_keys("site:www.logicjake.xyz")
                # elem.send_keys(Keys.RETURN)
                #
                # chrome.find_elements_by_link_text('滑天下之大稽')[0].click()
                # elem.click()
                # time.sleep(20)
            except Exception as e:
                print(e)
            else:
                print(chrome.session_id+" "+ip[0]+':'+ip[1])
            chrome.quit()

GetIP()
Visit()