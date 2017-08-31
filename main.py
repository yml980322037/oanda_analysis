#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
import checkFiles


if __name__ == '__main__':

    # 检查文件是否有遗漏的并且删除丢失日期不一致的文件
    check = input('Need to check data?(y/n)')
    if check == 'y':
        cates = ['eurusd', 'gbpusd', 'usdjpy', 'xagusd', 'xauusd']
        file = checkFiles.lostFiles(cates)
        checkFiles.delLostFiles(file)
    else:
        print('contiue')