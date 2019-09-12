# -*- coding: utf-8 -*-
import spider.pg_tool as pg
import spider.deal_page as dp
from urllib.error import HTTPError


def deal01():
    conn = pg.getConnection()
    index = 0
    with open('e:/spider.csv', 'r', encoding='utf-8') as fin:
        with open('e:/wrong.txt', 'w', encoding='utf-8') as fout:
            for ln in fin.readlines():
                ln = ln.strip()
                if len(ln) < 2:
                    continue
                url, title = ln.split(',')
                index += 1
                try:
                    htmlContent = dp.getHtmlContent(url=url, encoding='utf-8')
                    description, content = dp.parseHtml01(htmlContent)
                    description = description or title
                    if content:
                        dp.saveResult(url, title, description, content, '电梯企业新闻', conn)
                    else:
                        fout.write(url+' >>> ' + title + '\n')
                except HTTPError:
                    print("HTTPError!!{:d} --- {} --- {}".format(index, title, url))
                # print(content,'\n',description)
                else:
                    print("{:d} --- {} --- {}".format(index, title, url))

    conn.close()


if __name__ == '__main__':
    deal01()
