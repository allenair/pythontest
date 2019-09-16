# -*- coding: utf-8 -*-
import re
import urllib.request
from bs4 import BeautifulSoup
import spider.pg_tool as pg
from pyquery import PyQuery as pq
from urllib.parse import urlencode
import json


def getHtmlContent(url, encoding):
    headers = {'User_Agent': 'Mozilla/5.1 (Windows NT 10.0; Win64; x64) Chrome/77.0.3809.100 Safari/537.36'}
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
            index += 1
            for tag in soup.find_all('li'):
                for htmlStr in tag.contents:
                    line = ''
                    if htmlStr:
                        line = str(htmlStr)
                    if pattern.match(line):
                        print(str(index) + '>>>' + line)
                        fout.write(line + '\n')


def findPage_company(baseUrl, num):
    urlList = []
    for i in range(1, num + 1):
        if i == 1:
            urlList.append(baseUrl)
        else:
            urlList.append(baseUrl + '&page=' + str(i))

    with open('e:/tmp.txt', 'w', encoding='utf-8') as fout:
        index = 0
        for url in urlList:
            htmlContent = getHtmlContent(url, 'utf-8')
            doc = pq(htmlContent)
            index += 1
            for tag in doc('.list').items():
                companyName = tag('strong').filter('.px14').eq(0).text()
                companyProperty = tag('li').filter('.f_gray').eq(0).text()
                print(str(index) + '>>>' + companyName)
                fout.write("{}###{}\n".format(companyName, companyProperty[3:]))


def getCompanyInfoFromBaidu(companyName):
    params = {
        "q": companyName
    }
    htmlContent = getHtmlContent("https://xin.baidu.com/s?" + urlencode(params) + '&t=0', 'utf-8')
    doc = pq(htmlContent)
    for tag in doc('.zx-list-item-url').items():
        url = 'https://xin.baidu.com' + tag.attr('href')
        propertyDict = getCompanyDetailInfo(url)
        break
    else:
        return ''
    return propertyDict


def getCompanyDetailInfo(url):
    resDict = {}

    detailUrl = url.replace('/compinfo?', '/basicAjax?')
    htmlContent = getHtmlContent(detailUrl, 'utf-8')
    baseDict = json.loads(htmlContent, encoding='utf-8')
    baseDict = baseDict['data']

    leaderUrl = url.replace('/compinfo?', '/directorsAjax?')
    leaderContent = getHtmlContent(leaderUrl, 'utf-8')
    leaderDict = json.loads(leaderContent, encoding='utf-8')

    resDict['ent_name'] = baseDict['entName']
    resDict['annual_date'] = baseDict['annualDate']
    resDict['authority'] = baseDict['authority']
    resDict['describe'] = baseDict['describe']
    resDict['district'] = baseDict['district']
    resDict['other_name'] = baseDict['entLogoWord'] if baseDict['entLogoWord'] else ''

    resDict['ent_type'] = baseDict['entType']
    resDict['industry'] = baseDict['industry']
    resDict['legal_person'] = baseDict['legalPerson']
    resDict['license_number'] = baseDict['licenseNumber'] if 'licenseNumber' in baseDict else ''
    resDict['other_name'] = resDict['other_name'] + ', ' + baseDict['oldEntName'] if baseDict['oldEntName'] else \
        resDict['other_name']
    resDict['open_status'] = baseDict['openStatus']
    resDict['open_time'] = baseDict['openTime']
    resDict['org_code'] = baseDict['orgNo']
    resDict['reg_addr'] = baseDict['regAddr']
    resDict['reg_capital'] = baseDict['regCapital']
    resDict['reg_code'] = baseDict['regNo']
    resDict['buz_scope'] = baseDict['scope']
    resDict['start_date'] = baseDict['startDate']

    shareList = []
    for item in baseDict['shares']:
        shareList.append(item['name'])

    resDict['shares'] = ', '.join(shareList)

    leaderList = []
    for item in leaderDict['data']['list']:
        leaderList.append("{}：{}".format(item['title'], item['name']))

    resDict['leaders'] = ', '.join(leaderList)

    return resDict


def saveCompanyInfo(infoDict, conn):
    sql = """
        INSERT INTO spider_company
            (ent_name, annual_date, authority, describe, district, other_name, ent_type, industry, legal_person, 
                license_number, open_status, open_time, org_code, reg_addr, reg_capital, reg_code, buz_scope, start_date, shares, leaders, remark)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    valTuple = (
        infoDict['ent_name'], infoDict['annual_date'], infoDict['authority'], infoDict['describe'],
        infoDict['district'], infoDict['other_name'], infoDict['ent_type'], infoDict['industry'],
        infoDict['legal_person'], infoDict['license_number'], infoDict['open_status'], infoDict['open_time'],
        infoDict['org_code'], infoDict['reg_addr'], infoDict['reg_capital'], infoDict['reg_code'],
        infoDict['buz_scope'], infoDict['start_date'], infoDict['shares'], infoDict['leaders'], infoDict['remark'])
    pg.insert_update(sql, valTuple, conn)


if __name__ == '__main__':
    findPage_company('http://www.goodlift.net/company/search.php?areaid=5', 4)
    # getCompanyInfoFromBaidu('通力')
    # pass
