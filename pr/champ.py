# -*- coding: utf-8 -*-
import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

html_doc = urlopen('https://www.championat.com/').read()
soup = BeautifulSoup(html_doc, 'html.parser')

news =  soup.find_all('div', 'page__block livetable js-livetable')
link = news[0].find_all('noscript')
head=link[0].find_all('div', 'livetable__i football')
tour=head[0].find_all('div', 'livetable__i__tournament')
lin=tour[0].find_all('a', 'livetable__i__title__link')
text=lin[0].find_all('span')
eve=tour[0].find_all('a', 'livetable__i__link')


games=[]
file_1 = open("file.txt", "w")
file_1.write('\n')
file_1.close()
for c in tour:
    current_game = {}
    lin=c.find_all('a', 'livetable__i__title__link')
    text=lin[0].find_all('span', 'livetable__i__title__text')
    current_game['league'] = text[0].text
    eve=c.find_all('a', 'livetable__i__link')
    for z in eve:
        time=z.find_all('span', 'livetable__i__time')
        name=z.find_all('span', 'livetable__i__name')
        score=z.find_all('span', 'livetable__i__score')
        if z.find_all('span', 'livetable__i__state')[0].text=='окончен':
            current_game['time'] = time[0].text
            teams = name[0].text
            a=str(teams).split(' - ')
            current_game['teamHome']=re.sub(r'\s+$', '', a[0])
            current_game['teamAway']=re.sub(r'^\s+', '', a[1])
            sc = score[0].text
            sc = re.sub(r'\s', '', sc)
            sc = sc.replace('Б', '')
            sc = sc.replace('ОТ', '')
            s=str(sc).split(':')
            current_game['scoreHome']=re.sub(r'\s+$', '', s[0])
            current_game['scoreAway']=re.sub(r'^\s+', '', s[1])
            file_1 = open("file.txt", "a")
            file_1.write(str(current_game)+'\n')
            file_1.close()
            games.append(current_game)





head=link[0].find_all('div', 'livetable__i hockey')
tour=head[0].find_all('div', 'livetable__i__tournament')
lin=tour[0].find_all('a', 'livetable__i__title__link')
text=lin[0].find_all('span')
eve=tour[0].find_all('a', 'livetable__i__link')


games=[]

for c in tour:
    current_game = {}
    lin=c.find_all('a', 'livetable__i__title__link')
    text=lin[0].find_all('span', 'livetable__i__title__text')
    current_game['league'] = text[0].text
    eve=c.find_all('a', 'livetable__i__link')
    for z in eve:
        time=z.find_all('span', 'livetable__i__time')
        name=z.find_all('span', 'livetable__i__name')
        score=z.find_all('span', 'livetable__i__score')
        if z.find_all('span', 'livetable__i__state')[0].text=='окончен':
            current_game['time'] = time[0].text
            teams = name[0].text
            a=str(teams).split(' - ')
            current_game['teamHome']=re.sub(r'\s+$', '', a[0])
            current_game['teamAway']=re.sub(r'^\s+', '', a[1])
            sc = score[0].text
            sc = re.sub(r'\s', '', sc)
            sc = sc.replace('Б', '')
            sc = sc.replace('ОТ', '')
            s=str(sc).split(':')
            current_game['scoreHome']=re.sub(r'\s+$', '', s[0])
            current_game['scoreAway']=re.sub(r'^\s+', '', s[1])
            file_1 = open("file.txt", "a")
            file_1.write(str(current_game)+'\n')
            file_1.close()
            games.append(current_game)
