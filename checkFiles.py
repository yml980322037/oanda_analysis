#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os
import csv


def dateList(beginDate, endDate):
    """
    参考来源自https://www.zhihu.com/question/35455996， 侯处然
    主要是生成一段时间内的日期列表
    :param beginDate: 开始日期，形如‘20160601’的字符串或datetime格式 
    :param endDate: 结束日期， 形如‘20160601’的字符串或datetime格式
    :return: 日期列表
    """
    date_list = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_list


def generateFileName(cate, dates):
    """
    根据货币对种类来生成数据集中该货币对的所有文件
    :param cate: 货币对种类, 参数类型为字符串(string)
    :param dates: 日期列表，参数类型为列表(list)
    :return: 生成对应的文件名, 返回值类型为列表(list)
    """

    cwd = os.getcwd()
    fileNames = [cwd + '\\' + cate + '\\' + x + '_' + cate + '_minute_quote.csv' for x in dates]
    return fileNames


def lostOrNot(fileNames):
    """
    检查出各个货币对数据集的丢失文件，然后返回丢失文件的文件名
    :param fileNames: 查询的文件名列表，参数类型为列表(list)
    :return: 丢失的文件的文件名，返回值类型为列表(list)
    """
    lost = []
    for file in fileNames:
        if not os.path.exists(file):
            lost.append(file.split("\\")[-1])
    return lost


def lostFiles(cates):
    """
    检查20060319-20170725这段时间内的各个货币对的每天文件是否存在，汇总丢失文件的文件名
    :param cates: 货币对种类列表，参数类型为列表(list)
    :return: 返回的丢失文件的文件名合集的文件名，返回值为字符串(string)
    """
    files = []
    dates = dateList('20060319', '20170725')

    # 汇总各个货币对的丢失文件的文件名
    for cate in cates:
        fileNames = generateFileName(cate, dates)
        lost = lostOrNot(fileNames)
        files.append(lost)

    # 将文件名写入csv，若长度不够则以空格(' ')代替
    with open('lostFiles.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(cates)
        length = max([len(x) for x in files])
        for i in range(length):
            row = []
            for j in files:
                if i < len(j):
                    row.append(j[i])
                else:
                    row.append(' ')
            writer.writerow(row)
    # print('Data has been checked. Open lostFiles.csv to read the result of lost files.')
    return 'lostFiles.csv'


def datesFromLostFile(csvFile):
    """
    提取丢失文件的时间
    :param csvFile: 丢失文件的合集
    :return: 丢失文件日期列表和外汇类型，返回类型为list和list
    """
    dataFrame = pd.read_csv(csvFile)
    columns = dataFrame.columns
    dates = []

    # 提取日期
    for column in columns:
        li = [x.split('_')[0] for x in dataFrame[column].tolist()]
        dates[len(dates):] = li
    dates = list(set(dates))
    dates.sort()

    # 处理空格
    try:
        dates.remove(' ')
    except:
        print('checkFiles.datesFromlostFile: No File exists on some bu not all dates.')

    return dates, columns


def delLostFiles(csvFile):
    """
    主要是用来删除没有同一时间都有的数据
    :param csvFile: 丢失文件的合集
    :return: 
    """

    dates, columns = datesFromLostFile(csvFile)
    # 删除文件
    for cate in columns:
        files = generateFileName(cate, dates)
        for fileName in files:
            if os.path.exists(fileName):
                os.remove(fileName)


def existingFiles():
    """
    这个函数主要是返回已存在的数据的文件名
    :return: 
    """
    files = []
    lostDates, cates = datesFromLostFile('lostFiles.csv')
    dates = dateList('20060319', '20170725')
    for x in lostDates:
        dates.remove(x)
    for cate in cates:
        fileNames = generateFileName(cate, dates)
        files.append(fileNames)

    return files, cates


if __name__ == '__main__':
    # Test dateList function and run normally
    dates = dateList('20060319', '20170725')
    # print(dates)

    # Test generateFileName function and run normally
    files = generateFileName('eurusd', dates)
    # print(files)

    # Test lostOrNot function
    lost = lostOrNot(files)
    # print(lost)

    # Test lostFiles funtion and run normally
    cates = ['eurusd', 'gbpusd', 'usdjpy', 'xagusd', 'xauusd']
    # lostFiles(cates)

    # Test delLostFiles function
    # delLostFiles('./lostFiles.csv')
    existingFiles()
