import os
import math
import time
import json
import xlrd
import jieba
import pickle
import random
import requests
import numpy as np
import pandas as pd
from flask_cors import CORS
from datetime import datetime
import sklearn.ensemble as ens
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
from sklearn import linear_model
from sklearn.cluster import KMeans
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory, request
from sklearn.manifold import TSNE


def trans(_dataUrl, saveUrl):
    try:
        f = open(_dataUrl, 'r', encoding='utf-8')
    except:
        f = open(_dataUrl, 'r', encoding='gbk')
    s = ""
    for c in f:
        s += str(c).replace('"', "")
    try:
        f = open(saveUrl, 'w', encoding='utf-8')
        f.write(s)
        f.close()
    except:
        f = open(saveUrl, 'w', encoding='gbk')
        f.write(s)
        f.close()


def keys(article, length=100):
    """
    :param article: 需要切分的文本
    :param length: 关键词数量
    :return:
    """
    dele = {'。', '！', '？', '的', '“', '”', '（', '）', ' ', '》', '《', '，'}
    words = list(jieba.cut(article))
    # 词频字典
    articleDict = {}
    # 关键词
    articleSet = set(words) - dele
    for w in articleSet:
        if len(w) > 1:
            articleDict[w] = words.count(w)
    s = []
    k = list(articleDict.keys())
    w = list(articleDict.values())
    for i in range(len(k)):
        s.append({
            "key": k[i],
            "value": w[i]
        })
    data = pd.DataFrame(s)
    data = data.sort_values(by=['value'], ascending=False)
    try:
        k = list(data['key'])[: length]
    except:
        k = list(data['key'])
    return k


def weights(article, length=100):
    """
    :param article: 需要切分的文本
    :param length: 关键词数量
    :return:
    """
    dele = {'。', '！', '？', '的', '“', '”', '（', '）', ' ', '》', '《', '，'}
    words = list(jieba.cut(article))
    # 词频字典
    articleDict = {}
    # 关键词
    articleSet = set(words) - dele
    for w in articleSet:
        if len(w) > 1:
            articleDict[w] = words.count(w)
    s = []
    k = list(articleDict.keys())
    w = list(articleDict.values())
    for i in range(len(k)):
        s.append({
            "key": k[i],
            "value": w[i]
        })
    data = pd.DataFrame(s)
    data = data.sort_values(by=['value'], ascending=False)
    try:
        w = list(data['value'])[: length]
    except:
        w = list(data['value'])
    return w


def mkdir(path):
    """
    :param path: 创建文件夹位置
    :return:
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return False
    return True


def csvLists(fileUrl):
    L = []
    for root, ds, fs in os.walk(fileUrl):
        for f in fs:
            L.append(f)
    return L


# 读取文件
def readCsv(url, chunksize=5000):
    try:
        data = pd.read_csv(url, encoding="utf-8", chunksize=chunksize)
    except:
        data = pd.read_csv(url, encoding="gbk", chunksize=chunksize)
    chunk_result_list = []
    for chunk in data:
        chunk_result_list.append(chunk)
    return pd.concat(chunk_result_list)


# 读取文件
def readXlsx(url):
    return pd.read_excel(url)


def saveTxt(url, s, encoding="gbk"):
    file = open(url, 'w', encoding=encoding)
    file.write(s)
    file.close()


def jsonStr(s):
    return jsonify(json.loads(str(s).replace("'", '"')))


def counts(L):
    return len(L)


def uniLen(data, name):
    return list(data[name].unique())


def avr(L):
    if len(L):
        s = 0
        n = 0
        for c in L:
            try:
                if c != 0:
                    s += float(c)
                    n += 1
            except:
                a = 1
        if n != 0:
            return round(s / n, 2)
        return 0
    return 0


def sums(L):
    if len(L):
        s = 0
        for c in L:
            s += float(c)
        return round(s, 2)
    return 0


def maxs(L):
    maxl = 0
    for c in L:
        try:
            if float(maxl) < float(c):
                maxl = c
        except:
            continue
    return maxl


def mins(L):
    minl = 1e9
    for c in L:
        try:
            if float(minl) > float(c):
                minl = c
        except:
            continue
    if minl == 1e9:
        return 0
    return minl


def firstValue(data, header):
    return list(data[header])[0]


def q1(L):
    L.sort()
    return L[int(len(list(L)) / 4)]


def q2(L):
    L.sort()
    return L[int(len(list(L)) / 2)]


def q3(L):
    L.sort()
    return L[int(3 * len(list(L)) / 4)]


def returnValue(data, value='valueXXX', valueType='cnt'):
    if valueType == 'cnt':
        return len(list(data[list(data.head(0))[0]]))
    elif valueType == 'avr':
        return avr(list(data[value]))
    elif valueType == 'sum':
        return sums(list(data[value]))


# 筛选数据
def sxData(data, sxHeader, sxValue):
    try:
        data.loc[:, sxHeader] = data[sxHeader].astype('str')
    except:
        a = 1
    try:
        data = data[data[sxHeader] == str(sxValue)]
    except:
        try:
            data = data[data[sxHeader] == int(sxValue)]
        except:
            data = data[data[sxHeader] == sxValue]
    return data


def appendL(L1, L2):
    for c in L2:
        L1.append(c)
    return L1


def aToA(s):
    _s = ""
    for c in s:
        if 'a' <= c <= 'z':
            _s += str(c).upper()
        else:
            _s += str(c)
    return _s


def AToa(s):
    _s = ""
    for c in s:
        if 'A' <= str(c) <= 'Z':
            _s += str(c).lower()
        else:
            _s += str(c)
    return _s


"""
数据处理
"""


# 修改字段名
def modify(data, h1, h2):
    data.rename(columns={h1: h2}, inplace=True)
    return data


# 某列特定文本替换
def replace(data, header, d1, d2):
    d1 = str(d1).replace("234", "/")
    data.loc[:, header] = data[header].astype('str')
    data.loc[:, header] = data[header].str.replace(d1, d2)
    return data


# 去重
def drop(data, headers):
    return data.drop_duplicates(subset=headers, keep='first', inplace=False)


# 去空
def dropSpace(data, header):
    data.dropna(axis=0, how="any", subset=header, inplace=True)
    return data


# 删除某列
def deleteHeader(data, header):
    return data.drop(labels=header, axis=1)


# 排序
def sortHeader(data, headers, ascending=False):
    return data.sort_values(by=headers, ascending=ascending)


# 分割
def splitHeader(data, header, splitCh):
    splitCh = str(splitCh).replace("234", "/")
    s = data[header].str.split(splitCh, expand=True)
    return data.join(s)


# 转换类型
def transHeaderType(data, header, headerType):
    data.loc[:, header] = data[header].astype(headerType)
    return data


# 缺失值补充
def nullInsert(data, header, insertType, insertValue):
    if insertType == '特定值':
        data[header] = data[header].fillna(insertValue)
    elif insertType == '平均值':
        df = data
        df = df.dropna(axis=0, how='any')
        insertValue = avr(list(df[header]))
        data[header] = data[header].fillna(insertValue)
    return data


# 转置
def transPosition(data, trainsHeaders, newHeader, newValue):
    headers = list(data.head(0))
    extraHeaders = []
    for header in headers:
        if not (header in trainsHeaders):
            extraHeaders.append(header)
    firHeader = extraHeaders[0]
    s = []
    L = []
    for header in extraHeaders:
        L.append(list(data[header]))
    for i in range(len(list(data[firHeader]))):
        data1 = data
        for j in range(len(extraHeaders)):
            data1 = data1[data1[extraHeaders[j]] == L[j][i]]
        for j in trainsHeaders:
            try:
                dataL = list(data1[j])
                if len(dataL) != 0:
                    _s = {}
                    for k in range(len(extraHeaders)):
                        header = extraHeaders[k]
                        _s.update({
                            header: L[k][i]
                        })
                    _s.update({
                        newHeader: j,
                        newValue: dataL[0]
                    })
                    s.append(_s)
            except:
                continue
    return pd.DataFrame(s)


# 量化操作
def quality(data, header, quantifyType='量化'):
    headerUnique = list(data[header].unique())
    s = []
    L = list(data[header])
    for i in range(len(L)):
        s.append(
            headerUnique.index(
                L[i]
            )
        )
    s = np.array(s)
    headers = list(data.head(0))
    headers.append("_" + header)
    if quantifyType == '量化':
        data = np.c_[data.values, s]
        data = pd.DataFrame(data)
        data.columns = headers
        return data
    elif quantifyType == '标准化':
        data.loc[:, header] = round((data[header] - data[header].mean()) / data[header].std(), 3)
        return data
    elif quantifyType == '归一化':
        L = data[header]
        data.loc[:, header] = round((L - L.min()) / (L.max() - L.min()), 3)
        return data


# 字典降维
def dimenList(_S, _L=None, depth=1):
    if _L is None:
        _L = []
    if type(_S) != list:
        return _S
    for ii in _S:
        _L.append(dimenList(ii, _L, depth + 1))
    if depth == 1:
        L = []
        for ii in _L:
            if ii != None:
                L.append(ii)
        return L


# 检查字典是否包含某元素
def isInDict(d, k):
    _f = 0
    for c in d:
        if str(c) == str(k):
            _f = 1
    return _f


# 检查列表是否互相包含元素
def checkLInclude(L1, L2):
    for c in L1:
        if c in L2:
            return True
    return False


# y-m-d转datetime
def y_m_dToDatetime(timeStr):
    if '-' in timeStr:
        timeStr = timeStr.split('-')
    elif '/' in timeStr:
        timeStr = timeStr.split('/')
    return datetime(int(timeStr[0]), int(timeStr[1]), int(timeStr[2]))


def cntMaxI(L):
    """众数统计"""
    s = {}
    maxNum = 0
    maxI = 0
    for c in L:
        try:
            s[str(c)] += 1
            if maxNum < s[str(c)]:
                maxI = c
                maxNum = s[str(c)]
        except:
            s.update({
                str(c): 1
            })
            if maxNum < s[str(c)]:
                maxI = c
                maxNum = s[str(c)]
    return maxI


def mergeLR(data1, data2, headers):
    return pd.merge(left=data1, right=data2, how='left', on=headers)


"""
header trait(将数据中出现的0排除)
"""


# 最高频率
def maxFreq(data, header):
    data = dropSpace(data, header)
    maxL = 0
    for i in list(data[header].unique()):
        if str(i) != '0':
            if list(data[header].unique()).index(i) == 0:
                maxL = len(data[data[header] == i])
            else:
                maxL = max(maxL, len(data[data[header] == i]))
    return maxL


# 最低频率
def minFreq(data, header):
    data = dropSpace(data, header)
    minL = 0  # 数据次数过多需要更新
    for i in list(data[header].unique()):
        if str(i) != '0':
            if list(data[header].unique()).index(i) == 0:
                minL = len(data[data[header] == i])
            else:
                minL = min(minL, len(data[data[header] == i]))
    return minL


# 频率和
def sumFreq(data, header):
    data = dropSpace(data, header)
    s = 0
    for i in list(data[header].unique()):
        if str(i) != '0':
            s += len(data[data[header] == i])
    return s


# 中位数频率
def middleFreq(data, header):
    data = dropSpace(data, header)
    L = []
    for i in list(data[header].unique()):
        if str(i) != '0':
            L.append(len(data[data[header] == i]))
    L.sort()
    try:
        return L[int(len(L) / 2)]
    except:
        return 0


def isText(unique):
    for c in unique[:10]:
        if u'\u4e00' <= str(c) <= u'\u9fff':
            return True
    return False


def isTime(name, unique):
    for c in unique[:10]:
        for cc in [":", "：", '\\', "/", "-", "年", "月", "日", "星期"]:
            if cc in str(c):
                return True
    for c in ['year', 'month', 'day', 'date', '年', '月', '日', '时', '分', '秒', '时间', '时段', '星期']:
        if (str(c) in str(name)) or (str(name) in str(c)):
            return True
    return False


def isJd(name):
    for c in ['lng', '经度', 'Lng', 'LNG']:
        if c in str(name):
            return True
    return False


def isWd(name):
    for c in ['lat', '纬度', 'LAT', 'Lat']:
        if c in str(name):
            return True
    return False


"""
chart
"""


def normalChartData(data, headers, value='valueXXXX', valueType='cnt', names=None, depth=0):
    if names is None:
        names = []
    if depth == 0:
        if value != 'valueXXXX':
            L = [value]
        else:
            L = []
        for c in headers:
            L.append(c)
        data = data[L]
    s = []
    if depth == len(headers):
        __s = {}
        for i in range(len(headers)):
            __s.update({
                'name' + str(i + 1): names[i],
            })
        __s.update({
            'value': returnValue(data, value, valueType)
        })
        return __s
    _s = []
    header = headers[depth]
    for i in uniLen(data, header):
        _data = data[data[header] == i]
        names.append(i)
        _s.append(normalChartData(_data, headers, value, valueType, names, depth + 1))
        names.pop()
    s = dimenList(_s)
    return s


def sankeyChartsData(data, headers, value='valueXXXX', valueType='cnt', names=None, depth=0):
    if names is None:
        names = []
    if depth == 0:
        if value != 'valueXXXX':
            L = [value]
        else:
            L = []
        for c in headers:
            L.append(c)
        data = data[L]
    if depth >= len(headers):
        return
    _s = []
    header = headers[depth]
    for i in uniLen(data, header):
        _data = data[data[header] == i]
        names.append(i)
        _s.append(sankeyChartsData(_data, headers, value, valueType, names, depth + 1))
        _s.append({
            'name1': names[depth - 1],
            'name2': names[depth],
            'value': returnValue(data, value, valueType)
        })
        names.pop()
    s = dimenList(_s)
    return s


def boxChartsData(data, headers, value='valueXXXX', valueType='cnt', names=None, depth=0):
    if names is None:
        names = []
    if depth == 0:
        if value != 'valueXXXX':
            L = [value]
        else:
            L = []
        for c in headers:
            L.append(c)
        data = data[L]
    if depth == len(headers):
        __s = {}
        for i in range(len(headers)):
            __s.update({
                'name' + str(i + 1): names[i],
            })
        __s.update({
            'high': maxs(list(data[value])),
            'q1': q1(list(data[value])),
            'q2': q2(list(data[value])),
            'q3': q3(list(data[value])),
            'low': mins(list(data[value])),
        })
        return __s
    _s = []
    header = headers[depth]
    for i in uniLen(data, header):
        _data = data[data[header] == i]
        names.append(i)
        _s.append(boxChartsData(_data, headers, value, valueType, names, depth + 1))
        names.pop()
    s = dimenList(_s)
    return s


def treeChartsData(data, headers, value='valueXXXX', valueType='cnt', names=None, depth=0):
    """
    :param data:
    :param headers:
    :param value:
    :param valueType:
    :param names:
    :param depth:
    :return: 数据筛选逻辑有问题，需要重新弄
    """
    if names is None:
        names = []
    if depth == 0:
        if value != 'valueXXXX':
            L = [value]
        else:
            L = []
        for c in headers:
            L.append(c)
        data = data[L]
    if depth == len(headers):
        return {
            'name': str(names[depth - 1]).replace(",", ""),
            'value': returnValue(data, value, valueType)
        }
    _s = []
    header = headers[depth]
    for i in uniLen(data, header):
        _data = data[data[header] == i]
        names.append(i)
        _s.append({
            'name': str(names[depth]).replace(",", ""),
            'children': treeChartsData(_data, headers, value, valueType, names, depth + 1),
            'value': returnValue(data, value, valueType)
        })
        names.pop()
    if depth == 0:
        return {
            'name': 'root',
            'children': _s,
        }
    else:
        return _s


def getChartData(chartName, data, headers, value='valueXXXX', valueType='cnt'):
    for header in list(data.head(0)):
        data = dropSpace(data, header)
    if 'normalChart' in chartName:
        return normalChartData(data, headers, value, valueType)
    elif 'sankey' in chartName:
        return sankeyChartsData(data, headers, value, valueType)
    elif 'box' in chartName:
        return boxChartsData(data, headers, value, valueType)
    elif 'tree' in chartName:
        return treeChartsData(data, headers, value, valueType)
    return normalChartData(data, headers, value, valueType)


"""
chart
"""

"""
sklearn
"""


# k-means分类
def kmeansClassify(data, headers, n_clusters, classifyHeader, textHeaders=None, random_state=9):
    if textHeaders is None:
        textHeaders = []
    x_test = []
    uniques = {}
    for header in textHeaders:
        uniques.update({
            str(header): list(data[header].unique())
        })
    for iii in range(len(list(data[headers[0]]))):
        _s = []
        for header in headers:
            if header in textHeaders:
                _s.append(uniques[str(header)].index(list(data[header])[iii]))
            else:
                _s.append(list(data[header])[iii])
        x_test.append(_s)
    y = np.array(
        KMeans(
            n_clusters=n_clusters,
            random_state=random_state
        ).fit_predict(x_test)
    )
    headers = list(data.head(0))
    headers.append(classifyHeader)
    data = data.values
    data = pd.DataFrame(
        np.c_[data, y]
    )
    data.columns = headers
    return data


def kmeansClassifyWithScore(data, headers, n_clusters, classifyHeader, textHeaders=None, random_state=9):
    if textHeaders is None:
        textHeaders = []
    x_test = []
    uniques = {}
    for header in textHeaders:
        uniques.update({
            str(header): list(data[header].unique())
        })
    for iii in range(len(list(data[headers[0]]))):
        _s = []
        for header in headers:
            if header in textHeaders:
                _s.append(uniques[str(header)].index(list(data[header])[iii]))
            else:
                _s.append(list(data[header])[iii])
        x_test.append(_s)
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state
    )
    y = np.array(
        kmeans.fit_predict(x_test)
    )
    headers = list(data.head(0))
    headers.append(classifyHeader)
    data = data.values
    data = pd.DataFrame(
        np.c_[data, y]
    )
    data.columns = headers
    score = sum(np.min(cdist(np.array(x_test), kmeans.cluster_centers_, 'euclidean'), axis=1)) / np.array(x_test).shape[
        0]
    return {
        'data': data,
        'score': round(score, 4)
    }


# 基于三个字段的散点图绘制(plot)
def pltScatter(data, xHeader='x', yHeader='y', color='用户基础信息分类', saveName='基于用户信息特征的分类.png'):
    data = data[[xHeader, yHeader, color]]
    data = drop(data, [xHeader, yHeader, color])
    plt.figure(figsize=(7, 7))
    colors = [
        'red', 'blue', 'green', 'yellow', 'pink', 'orange', 'cyan', 'brown', 'purple', 'grey',
        '#007700', '#770000', '#770077', '#777700', '#007777',
        '#77ff77', '#ff7777', '#ffff77', '#ff77ff', '#7777ff',
        '#77aaff'
    ]
    L = list(data[color].unique())
    for i in range(len(L)):
        if str(L[i]) != 'nan':
            dd = data[data[color] == L[i]]
            x = np.array(list(dd[xHeader]))
            y = np.array(list(dd[yHeader]))
            plt.scatter(x, y, c=colors[i], s=100, label=L[i], alpha=0.6, edgecolors='white')
    plt.title('')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig(saveName)


# k-means自动分类
def kmClsAuto(data, n_clusters, classifyHeader, random_state=9):
    textHeaders = []
    headers = list(data.head(0))[1:]
    for header in headers:
        if data[header].dtypes == 'object':
            textHeaders.append(header)
    return kmeansClassify(data, headers, n_clusters, classifyHeader, textHeaders, random_state)


# TSNE 降维 -> 二维坐标
def tsneDimen(data, n_components=2):
    tsne = TSNE(n_components=n_components)
    tsne.fit_transform(data)  # 进行数据降维,降成两维
    # a=tsne.fit_transform(data_zs) #a是一个array,a相当于下面的tsne_embedding_
    return pd.DataFrame(tsne.embedding_, index=data.index)  # 转换数据格式


# t-sne自动计算坐标
def tsnePosAuto(data, n=2):
    # 需要无脑归一化
    headers = list(data.head(0))[1:]
    textHeaders = headers
    # 不需要无脑归一化就注释
    """textHeaders = []
    headers = list(data.head(0))[1:]
    for header in headers:
        if data[header].dtypes == 'object':
            textHeaders.append(header)"""
    uniques = {}
    s = []
    for header in textHeaders:
        uniques.update({
            str(header): list(data[header].unique())
        })
    for iii in range(len(list(data[headers[0]]))):
        _s = {}
        for header in headers:
            if header in textHeaders:
                _s.update({
                    header: uniques[str(header)].index(list(data[header])[iii])
                })
            else:
                _s.update({
                    header: list(data[header])[iii]
                })
        s.append(_s)
    s = pd.DataFrame(s)
    s = tsneDimen(s, n)
    s = modify(s, 0, 'x')
    s = modify(s, 1, 'y')
    s = modify(s, 2, 'z')
    return s


"""
经纬度获取
"""


def getlnglat(address):
    KEY = '6775b4dbc3f89fb93b728bae7de8ec76'
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {'key': KEY,
              'address': address}
    res = requests.get(url, params)
    json_data = json.loads(res.text)
    jsonData = json_data['geocodes'][0]['location']
    return jsonData


def jwdInsert(data, header, pre='上海市'):
    s = []
    for i in list(data[header]):
        try:
            L = getlnglat(pre + i).split(',')
            s.append({
                "jd": L[0],
                "wd": L[1],
            })
        except:
            L = getlnglat(pre).split(',')
            s.append({
                "jd": L[0],
                "wd": L[1],
            })
    return pd.concat([data, pd.DataFrame(s)], axis=1)


app = Flask(__name__)
CORS(app, resources=r'/*')
