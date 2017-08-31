#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import checkFiles

def readDataPerKindOneDay(file, cate):
    """
    读取外汇数据csv文件的函数的第一个版本。主要功能是将读取单一外汇的某天数据中的两个开盘价相加之后取平均作为该分钟的报价
    :param file: 外汇数据csv文件，参数类型为string
    :param cate: 外汇类型，参数类型为string
    :return: 报价的DataFrame类型变量，存储着报价数据和报价时间。返回类型为DataFrame
    """
    # 将csv文件中的数组存在N x M 的list中
    data = []
    with open(file) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            data.append(row)

    # 将list中的数据转化为numpy中的array格式存储
    data = np.array(data)

    # 将numpy的array格式转为pandas的DataFrame格式存储
    dataFrame = pd.DataFrame(data, columns=['time', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J','K'])
    dataFrame = dataFrame.drop(['C','D', 'E', 'F', 'H', 'I', 'J', 'K'], axis=1)

    # 将列中的字符串转为浮点数
    dataFrame['B'] = dataFrame['B'].astype(float)
    dataFrame['G'] = dataFrame['G'].astype(float)

    dataFrame[cate] = (dataFrame['B'] + dataFrame['G']) / 2.0
    dataFrame = dataFrame.drop(['B', 'G'], axis=1)

    # 保存着报价与报价时间:['A', cate]
    return dataFrame


def dropNotInAll(datas, cates):
    """
    丢失没有同一时间都有的报价，保证数据的同步
    :param datas: 保存着不同外汇同一天的报价数据，参数类型为list
    :param cates: 外汇种类， 参数类型为list， list里面的为string
    :return: 返回不同外汇同一天的报价数据
    """

    dataFrame = []
    timeTemp = [x['time'].tolist() for x in datas]
    dataTemp = []
    for i in range(len(cates)):
        dataTemp.append(datas[i][cates[i]].tolist())
    # print(len(dataTemp))
    for i in range(len(timeTemp[0])):
        # 挑出有相同时间的报价
        timestamp = timeTemp[0][i]
        accept = True
        indices = []
        for data in timeTemp:
            # 若不存在则处理异常
            try:
                indices.append(data.index(timestamp))
            except ValueError:
                accept = False
                break
        if accept:
            line = []
            for i in range(len(indices)):
                line.append(dataTemp[i][indices[i]])
            temp = [timestamp]
            #temp[len(temp):] = line
            temp.extend(line)
            dataFrame.append(temp)
    col = ['time']
    col.extend(cates)
    dataFrame = pd.DataFrame(dataFrame, columns=col)

    return dataFrame



def readData(start, end):
    """
    这个函数是用来读取数据。此时读取的数据可以被直接用来进行建模。
    :return: 
    """

    # 用DataFrame的数据类型来存储现有文件的文件名
    files = []

    # 读取现有文件的文件名，不理会丢失了的文件
    files, cates = checkFiles.existingFiles()
    files = pd.DataFrame(np.array(files).T, columns=cates)

    # 读取现有文件的数据
    datas = []
    selects = files.iloc[start:end]
    row, col = np.shape(selects)
    for i in range(row):
        datas.append(readDataSameDay(selects.iloc[i],cates))

    return datas




def readDataSameDay(files, cates):
    """
    读取同一天的时候不同种类货币的外汇数据并存储在DataFrame数据类型的变量中。
    :param files: 同一天数据的不同外汇文件名，参数类型为list
    :param cates: 外汇种类， 参数类型为list
    :return: 同一天的时候不同种类货币的外汇数据, 返回类型为DataFrame
    """
    dataFrame = []
    for i in range(len(cates)):
        # DataFrame 格式
        data = readDataPerKindOneDay(files[i], cates[i])
        dataFrame.append(data)
    dataFrame = dropNotInAll(dataFrame,cates)

    return dataFrame




def calMean(datas, cate):
    """
    给定一天的数据量，计算其中一个类别的货币外汇的各点的后续均值。最后添加回该天数据中
    :param datas: 
    :param cate: 
    :return: 
    """
    for data in datas:
        # print(data.dtypes)
        s = data[cate].sum()
        print(s)
        l = len(data[cate])
        nl = []
        for x in data[cate]:
            if l > 1:
                m = (s - x)/(l - 1)
                if m < x:
                    m = 0
                else:
                    m = 1
                nl.append(m)
            else:
                nl.append(1)
        data['Trend'] = pd.Series(nl, index=data.index)






if __name__ == '__main__':

    # Test readDataOneDay function
    # data = readDataSameDay('./xagusd/20170725_xagusd_minute_quote.csv', 'xauusd')
    # print(data)

    #Test readData and readDataSameDay function
    datas = readData()
    for x in datas:
        cates = x.columns
        break
    calMean(datas, cates[1])
    #print("*"*49)
    for data in datas:
        print(data)