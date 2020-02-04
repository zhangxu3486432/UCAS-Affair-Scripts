#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : 张旭
# @Email   : zhangxu3486432@gmail.com
# @Blog    : https://zhangxu3486432.github.io
# @FileName: monitor_grades.py
# @Time    : 2020/2/4


from http import cookiejar

import requests
from bs4 import BeautifulSoup

from take_courses import identification
from utils import logger, send_email

from settings import RECEIVE_EMAIL


def query_grades(session):
    resp = session.get('http://jwxk.ucas.ac.cn/score/yjs/all')
    soup = BeautifulSoup(resp.text, 'lxml')
    grades = soup.select('#main-content > div > div.m-cbox.m-lgray > div.mc-body > table > tbody > tr')
    return grades


def monitor(grades, grades_num):
    if len(grades) > grades_num:
        grades_num = len(grades)
        score_content = ''
        for item in grades:
            score = item.find_all(name='td', attrs={'class': ''})
            if score.__len__() == 0:
                continue
            score_content += '{0}：{1}\n\n'.format(score[0].text, score[2].text)
        logger.info(score_content)
        send_email(score_content, RECEIVE_EMAIL)
    return grades_num


if __name__ == '__main__':
    session = requests.session()
    session.cookies = cookiejar.LWPCookieJar()
    session.cookies.load('sep.cookie')
    session = identification(session)
    grades_num = 0
    while True:
        grades = query_grades(session)
        grades_num = monitor(grades, grades_num)