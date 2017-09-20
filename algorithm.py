#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import svm
import arrangeData
import numpy as np
import checkFiles


def buildModel(datas, cate):
    """
    
    :param datas: 用来建模的数据
    :param cate: 算法的种类，决定了采用何种算法来建模
    :return: 
    """
    if cate == 'svc':
        clf = svm.SVC()

    for data in datas:
        label = data.iloc[:, -1]
        data.drop(['Trend'], axis=1)
        # data.drop(['time'], axis=1)
        clf.fit(data.values, np.array(label))

    return clf


def testModel(clf, datas):
    accuracy = []
    for data in datas:
        label = data.iloc[:, -1]
        data.drop(['Trend'], axis=1)
        # data.drop(['time'], axis=1)
        result = clf.score(data, np.array(label))
        accuracy.append(result)
    print(sum(accuracy)/len(accuracy))



if __name__ == '__main__':
    length = len(checkFiles.existingFiles()[0][0])

    # 建模预测 eurusd
    trainingDatas = arrangeData.readData(length - 150, length)
    for x in trainingDatas:
        cates = x.columns
        break
    arrangeData.calMean(trainingDatas, cates[1])
    clf = buildModel(trainingDatas, 'svc')


    # 测试分类器精度
    testingDatas = arrangeData.readData(length - 200, length - 150)
    arrangeData.calMean(testingDatas, cates[1])
    testModel(clf, testingDatas)