# coding:utf-8


import os
import random

from bs4 import BeautifulSoup
import requests
from jinja2 import Environment
from jinja2 import FileSystemLoader

def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

headers = {
    "Host": "t66y.com",
    "Accept-Encoding": "gzip, deflate",
    'User-Agent': agent,
    'X-Forwarded-For': random_ip(),
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}
pre = "http://t66y.com/"

wanted = []

def judge_url():
    urldic = {}
    undownloaddic = {}
    if os.path.exists("article_url.txt"):
        if os.path.getsize("article_url.txt") > 0:
            f = open('article_url.txt', 'r', encoding="utf-8")
            for line in f:
                key, value = line.split("=", 1)
                urldic[key] = value.strip('\n')
            f.close()
    else:
        f = open('article_url.txt', 'w')
        f.close()
    if os.path.exists("undownload_url.txt"):
        if os.path.getsize("undownload_url.txt") > 0:
            f = open('undownload_url.txt', 'r', encoding="utf-8")
            for line in f:
                key, value = line.split("=", 1)
                undownloaddic[key] = value.strip('\n')
                wanted.append({'href': pre + key,
                               'name': value.strip('\n')})
            f.close()
    else:
        f = open('undownload_url.txt', 'w')
        f.close()
    url = "http://t66y.com/thread0806.php?fid=7&search=&page="
    for i in range(1, 20):
        if i>=2:
            headers['Referer'] = url + str(i-1)
        html = requests.get(url+str(i), headers=headers)
        print(url+str(i))
        html.encoding = 'gbk'
        soup = BeautifulSoup(html.text, "html.parser")
        lines = soup.find_all('tr', class_="tr3 t_one tac")
        for line in lines:
            a_all = line.find_all('a')
            urltd = a_all[0]
            hotspot = line.find('span', class_="sred")
            if hotspot is not None:
                title = ''.join(e for e in a_all[1].string if e.isalnum())
                if urltd['href'] in urldic.keys() and urldic[urltd['href']] == title:
                    break
                else:
                    try:
                        saveHtml(urltd['href'], title)
                        urldic[urltd['href']] = title
                    except Exception:
                        if urltd['href'] in undownloaddic.keys():
                            print('in ' + title)
                        if urltd['href'] not in undownloaddic.keys():
                            undownloaddic[urltd['href']] = title
                            wanted.append({'href': pre + urltd['href'],
                                           'name': title})
                            print('not in haha' + title)
    fp = open('article_url.txt', 'w', encoding="utf-8")
    for x in urldic:
        line = x + '=' + urldic[x]
        fp.write(line)
        fp.write('\n')  # 显示写入换行
    fp.close()

    fp = open('undownload_url.txt', 'w', encoding="utf-8")
    for x in undownloaddic:
        line = x + '=' + undownloaddic[x]
        fp.write(line)
        fp.write('\n')  # 显示写入换行
    fp.close()

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR))
    template = env.get_template('1024article.template')
    content = template.render(wanted=wanted)
    filename = '1024article/undownload-article.html'
    fp = open(filename, 'w', encoding="utf-8")
    fp.write(content)
    fp.close()

def saveHtml(post_url, post_name):
    html = requests.get(pre + post_url, headers=headers)
    html.encoding = 'gbk'
    soup = BeautifulSoup(html.text, "html.parser")
    with open("1024article/" + post_name + ".html", "wb") as handler:
        soup_html = soup.prettify("utf-8")
        handler.write(soup_html)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    judge_url()
