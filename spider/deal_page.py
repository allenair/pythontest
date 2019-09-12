# -*- coding: utf-8 -*-
import re
import urllib.request
from bs4 import BeautifulSoup
import spider.pg_tool as pg


def getHtmlContent(url, encoding):
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/75.0.3809.100 Safari/537.36'}
    response = urllib.request.Request(url, headers=headers)
    htmlObj = urllib.request.urlopen(response)
    htmlContent = htmlObj.read().decode(encoding, errors='ignore')
    return htmlContent


def parseHtml01(htmlContent):
    description, content = '', ''
    soup = BeautifulSoup(htmlContent, 'html.parser')
    for tag in soup.find_all('div'):
        if tag.get("id") == 'article':
            content = replaceSpace(tag.text)
            break

    # for tag in soup.find_all('div'):
    #     if tag.get('class') and tag.get('valign') and (
    #             tag.get('height') == '27' or tag.get('height') == '250') and tag.get('valign') == 'top':
    #         content = replaceSpace(tag.text)
    #         break

    return description, content


def saveResult(url, title, description, content, content_type, conn):
    sql = "INSERT INTO spider_result (url_str, title, description, content_str, content_type) VALUES(%s, %s, %s, %s, %s);"
    valTuple = (url, title, description, content, content_type)
    pg.insert_update(sql, valTuple, conn)


def replaceSpace(content, pattern='\s+', replaceStr='  '):
    return re.sub(pattern, replaceStr, content)


def findPage(baseUrl, num):
    urlList = []
    for i in range(1, num + 1):
        if i == 1:
            urlList.append(baseUrl)
        else:
            urlList.append(baseUrl[:-1] + '-page-' + str(i) + "/")

    pattern = re.compile('.*<a href="//www.zgelevator.com/news.*')
    with open('e:/tmp.txt', 'w', encoding='utf-8') as fout:
        for url in urlList:
            htmlContent = getHtmlContent(url, 'utf-8')
            soup = BeautifulSoup(htmlContent, 'html.parser')
            for tag in soup.find_all('li'):
                if tag.get('class') and 'catlist_li' in tag.get('class'):
                    for htmlStr in tag.contents:
                        line = ''
                        if htmlStr:
                            line = str(htmlStr)
                        if pattern.match(line):
                            print(line)
                            fout.write(line + '\n')


def findPage_worldelevator(baseUrl, num):
    urlList = []
    for i in range(1, num + 1):
        if i == 1:
            urlList.append(baseUrl)
        else:
            urlList.append(baseUrl + '&page=' + str(i))

    pattern = re.compile('.*<a href="\sdetail.php\?id=.*')
    with open('e:/tmp.txt', 'w', encoding='utf-8') as fout:
        for url in urlList:
            htmlContent = getHtmlContent(url, 'gbk')
            soup = BeautifulSoup(htmlContent, 'html.parser')
            for tag in soup.find_all('li'):
                for htmlStr in tag.contents:
                    line = ''
                    if htmlStr:
                        line = str(htmlStr)
                    if pattern.match(line):
                        print(line)
                        fout.write(line + '\n')

def findPage_goodlift(baseUrl, num):
    urlList = []
    for i in range(1, num + 1):
        if i == 1:
            urlList.append(baseUrl)
        else:
            urlList.append(baseUrl[:-5] + '-' + str(i) + '.html')

    pattern = re.compile('.*<a href="http://www.goodlift.net/elevator_news/show-.*')
    with open('e:/tmp.txt', 'w', encoding='utf-8') as fout:
        index = 0
        for url in urlList:
            htmlContent = getHtmlContent(url, 'utf-8')
            soup = BeautifulSoup(htmlContent, 'html.parser')
            index +=1
            for tag in soup.find_all('li'):
                for htmlStr in tag.contents:
                    line = ''
                    if htmlStr:
                        line = str(htmlStr)
                    if pattern.match(line):
                        print(str(index) + '>>>' + line)
                        fout.write(line + '\n')



if __name__ == '__main__':
    findPage_goodlift('http://www.goodlift.net/elevator_news/list-5006.html', 80)
    # pass