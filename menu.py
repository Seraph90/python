#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import datetime
import sys
from termcolor import colored

is_html = False
is_bot = False

if 1 == len(sys.argv):
    print colored('Нужно указать вариант ланча (250 или 300)', 'green')
    exit()
elif '250' == sys.argv[1]:
    response = urllib2.urlopen('http://www.brandmeister.spb.ru/menu/biznes-lanch#content')
elif '300' == sys.argv[1]:
    response = urllib2.urlopen('http://www.brandmeister.spb.ru/menu/premium-lanchi-300-rub#content')
else:
    print colored('Нужно указать вариант ланча (250 или 300)', 'magenta')
    exit()

if 3 == len(sys.argv):
    if 'html' == sys.argv[2]:
        is_html = True
    elif 'bot' == sys.argv[2]:
        is_bot = True


html = response.read()
html = html[html.find(r'<table style="width: 100%;" border="0">'):html.find(r'</table>')]
html = re.sub('style="text-align: left;"', '', html)
html = re.sub('style="text-align: center;"', '', html)
html = re.sub('\s+colspan="2"', '', html)
html = re.sub('&nbsp;', '', html)
html = re.sub('</?span>', '', html)
html = re.sub(' >', '>', html)
html = re.sub('<hr />', '', html)
html = re.sub('<br>', '', html)
html = re.sub('<tr>\n<td><strong></strong></td>\n</tr>', '', html)
html = re.sub('</?thead>', '', html)
html = re.sub('</?tbody>', '', html)
html = re.sub('\n+', "\n", html)
html = re.sub('\s{3,}', '', html)
html = re.sub('(</strong>)+', '</strong>', html)
html = re.sub('(<strong>)+', '<strong>', html)
html = re.sub('</strong><strong>', '', html)
html = re.sub('<strong></strong>', '', html)
html = re.sub('<(\w+) .*?>', '<\g<1>>', html)
html = re.sub('<br>', '', html)
html = re.sub('<tr>\n<td></td>\n</tr>', '', html)

months = ['ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ', 'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ',
          'ДЕКАБРЯ']
day = str(datetime.date.today().day)
month = months[int(datetime.date.today().month) - 1]
reg = r'<tr>\n((?:.|\n)*?)\n</tr>'
pos = []
items = []
head = False

for item in re.compile(reg).findall(html):
    if not ':' in item and '<strong>' in item:
        pos.append(html.find(item))
        items.append(item)
        if month in item:
            if str(day) in item:
                head = item
                continue
            elif not head and str(int(day)+1) in item:
                head = item
                continue

if head:
    if pos[-1] > html.find(head):
        end = items[pos.index(html.find(head))+1]
        html = html[html.find(head)+len(head):html.find(end)]
    else:
        html = html[html.find(head)+len(head):]

html = re.sub(r'\n?</?tr>', '', html)
html = re.sub(r'<td>', '', html)
html = re.sub(r'</td>', '<br />', html)
html = re.sub(r'<br>', '', html)
html = re.sub(r'(<br />)+', '<br />', html)
html = re.sub(r'<strong>', '<br /><strong>', html)
html = re.sub(r'<br />\n(\s?\d)', ' - \g<1>', html)
html = re.sub(r'<br />', '<br />', html)
html = re.sub(r'  ', ' ', html)


if is_html:
    print html
    exit()

if is_bot:
    print "\n" + day + ' ' + month
else:
    print colored("\n" + day + ' ' + month, 'yellow')

html = re.sub('<.*?>', '', html)
html = re.sub('&laquo;', '«', html)
html = re.sub('&raquo;', '»', html)
html = re.sub('(\d)([мг])', '\g<1> \g<2>', html)
html = re.sub('\n (\d [мг])', ' - \g<1>', html)
if not is_bot:
    html = re.sub('([А-Яа-яЁёЮюЫыРрТт ]+:)', colored('\n\g<1> ', 'green'), html)
    html = re.sub('\n+', "\n", html)
else:
    html = re.sub('([А-Яа-яЁёЮюЫыРрТт ]+:)', '\n\g<1> ', html)

print html[1:]

