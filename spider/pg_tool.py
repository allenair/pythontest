# -*- coding: utf-8 -*-

import psycopg2


def getConnection(database="aistudy",
                  user="aistudy",
                  password="aistudy@zxtech",
                  host="192.168.1.147",
                  port="5432"):
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)
    return conn


def insert_update(sql='', valTuple=None, conn=None):
    if not sql or not conn:
        return ''

    cur = conn.cursor()
    cur.execute(sql, valTuple)
    conn.commit()
    return 'OK'


def search(sql='', conn=None):
    if not sql or not conn:
        return []

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    return rows


if __name__ == '__main__':
    conn = psycopg2.connect(database="aistudy",
                            user="aistudy",
                            password="aistudy@zxtech",
                            host="localhost",
                            port="5432")

    rows = search(sql='select * from spider_result limit 20', conn=conn)
    for row in rows:
        print(row)
