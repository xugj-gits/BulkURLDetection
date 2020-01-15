# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import threading
import queue
import time
import opertaeExcel


index = 1
array = [["序号", "域名", "Title", "Keywords", "Description"]]
queue = queue.Queue()

# with open('url.txt') as f:
#     l = f.readlines()


def btdk(url):
    try:
        html = requests.get(url, timeout=10).text
        html = html.encode("UTF-8")
    except:
        html = '<html><title>%s</title><meta name="keywords" content="" /><meta name="description" content="" /></html>' % url

    soup = BeautifulSoup(html.lower())
    try:
        t = soup.title.text
    except:
        t = "暂无title"

    try:
        k = soup.find(attrs={"name": "keywords"})[
            'content']
    except:
        k = "暂无keywords"
    try:
        d = soup.find(attrs={"name": "description"})[
            'content']
    except:
        d = "暂无description"

    return t, d, k


class MyThread(threading.Thread):

    def __init__(self, queue, url):
        threading.Thread.__init__(self)
        self.queue = queue
        self.url = url

    def run(self):
        global index
        while True:
            url = self.queue.get()
            t, k, d = btdk(url)
            array.append([index, url, t,
                          d, k])
            self.queue.task_done()
            index += 1


def test(l, ts=20):
    ll = [i.rstrip() for i in l]
    for j in range(ts):
        t = MyThread(queue, ll)
        t.setDaemon(True)
        t.start()
    for url in ll:
        queue.put(url)
    queue.join()
    opertaeExcel.write_excel_xlsx("tdk检测结果.xlsx", "tdk", array)


if __name__ == '__main__':
    # array = [["序号", "域名", "Title", "Keywords", "Description"]]
    # queue = queue.Queue()
    start = time.time()
    test(l, 20)
    end = time.time()
    print('共耗时:%s秒' % (end - start))
    # print(array)
    # opertaeExcel.write_excel_xlsx("tdk检测结果.xlsx", "tdk", array)
