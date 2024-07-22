import xgboost

from _2_L1 import *

data2 = readCsv(dataUrl + 'data2.csv')


@app.route('/tzxl2')
def tzxl2():
    """
    :return: 返回人员信息分类的可选特征序列
    """
    headers = []
    for header in list(data2.head(0)):
        if not header in ['就诊ID']:
            headers.append(header)
    return jsonStr({
        'tzxl2': headers
    })


@app.route('/tzxled2')
def tzxled2():
    """
    :return: 返回默认特征序列
    """
    headers = []
    data = readCsv(tempDataUrl + '_data2.csv')
    for header in list(data.head(0)):
        if not header in ['就诊ID', 'x', 'y', '分组标识', '人员信息分类']:
            headers.append(header)
    return jsonStr({
        'tzxl2': headers
    })


@app.route('/classify2', methods=['POST', 'GET'])
def classify2():
    """
    :return: 行为识别
    """
    rFile = request.json
    L = rFile['headers']
    defineType = rFile['defineType']
    defineFun = rFile['defineFun']
    # 数据读取
    data = readCsv(dataUrl + 'data2.csv')
    data = data.sort_values(by=['就诊ID'])
    _data = data[L].reset_index(drop=True)  # 行为特征
    ycbs = readCsv(tempDataUrl + 'data1_2.csv')  # 异常标识数据
    ycbs = ycbs.sort_values(by=['就诊ID'])
    ycbs = ycbs[['分组标识']].reset_index(drop=True)
    ryxx = readCsv(tempDataUrl + 'data1.csv')[['就诊ID', '人员信息分类']]  # 人员类别数据
    ryxx = ryxx.sort_values(by=['就诊ID'])
    ryxx = ryxx.reset_index(drop=True)
    # 根据已有数据对数据进行行为分组
    groupData = pd.concat([ryxx, _data, ycbs], axis=1)
    if defineFun == '分组标识':
        tempData = groupData[groupData['分组标识'] != 0]
        L1 = list(tempData['人员信息分类'].unique())
        L2 = []
        for i in list(groupData['人员信息分类'].unique()):
            if not i in L1:
                L2.append(i)
        trainData = groupData[groupData['人员信息分类'].isin(L1)]
        testData = groupData[groupData['人员信息分类'].isin(L2)]
    elif defineFun == '非分组识别':
        trainData = groupData[groupData['分组标识'] != 0]
        testData = groupData[groupData['分组标识'] == 0]
    else:
        trainData = groupData[groupData['分组标识'] != 0]
        testData = groupData[groupData['分组标识'] == 0]
    # 识别
    y = '分组标识'
    x = []
    for i in list(trainData.head(0)):
        if i != y and i != '就诊ID':
            x.append(i)
    train_x = trainData[x].values
    train_y = np.array(list(trainData[y]))
    test_x = testData[x].values
    if defineType == 'ExtraTreesClassifier':
        model = ens.ExtraTreesClassifier()
    elif defineType == 'BaggingClassifier':
        model = ens.BaggingClassifier()
    elif defineType == 'RandomForestClassifier':
        model = ens.RandomForestClassifier()
    elif defineType == 'XGBClassifier':
        model = xgboost.XGBClassifier()
    else:
        model = xgboost.XGBClassifier()
    model.fit(train_x, train_y)
    test_y = model.predict(test_x)
    _testData = pd.DataFrame(np.c_[test_x, test_y])
    L = x
    L.append(y)
    _testData.columns = L
    testData = pd.concat([testData[['就诊ID']].reset_index(drop=True),
                          _testData], axis=1)
    _data = pd.concat([trainData, testData], axis=0)
    _data = transHeaderType(_data, '分组标识', 'int32')
    _data = transHeaderType(_data, '人员信息分类', 'int32')
    _data = _data.sort_values(by=['就诊ID']).reset_index(drop=True)
    posData = readCsv(tempDataUrl + 'data1.csv')
    posData = posData[['就诊ID', 'x', 'y']]
    posData = posData.sort_values(by=['就诊ID']).reset_index(drop=True)
    _data = pd.concat([_data, posData[['x', 'y']]], axis=1)
    data = data.reset_index(drop=True)
    _data = _data[['人员信息分类', '分组标识', 'x', 'y']]
    data = pd.concat([data, _data], axis=1)

    """
    过滤不必要的字段
    """
    headers = ['就诊ID', 'x', 'y']
    for c in L:
        headers.append(c)
    data[headers].to_csv(tempDataUrl + 'data2.csv', index=False)
    # data[headers].to_csv(tempDataUrl + '_data2.csv', index=False)
    return jsonStr({
        'message': '识别成功',
        'fzbsflL': list(data['分组标识'].unique())
    })


@app.route('/sxHeader2')
def sxHeader2():
    """
    :return: 筛选字段
    """
    data = readCsv(tempDataUrl + 'data2.csv')
    headers = []
    for header in list(data.head(0)):
        if not header in ['就诊ID', '分组标识', 'x', 'y']:
            headers.append(header)
    return jsonStr({
        'headers': headers
    })


@app.route('/<x>/sxValue2')
def sxValue2(x):
    """
    :return: 筛选值
    """
    data = readCsv(tempDataUrl + 'data2.csv')
    return jsonStr({
        'values': list(data[x].unique())
    })


@app.route('/<x>/sxValues2')
def sxValues2(x):
    """
    :return: 筛选值
    """
    data = readCsv(tempDataUrl + 'data2.csv')
    L = list(data[x].unique())
    return jsonStr({
        'min': mins(L),
        'max': maxs(L)
    })


# 过滤数据
@app.route('/data2Gl', methods=['POST', 'GET'])
def data2Gl():
    rFile = request.json
    data = readCsv(tempDataUrl + 'data2.csv')
    sxValueRange = rFile['sxValueRange']
    for header in sxValueRange:
        L = sxValueRange[header]
        data = data[data[header] >= L[0]]
        data = data[data[header] <= L[1]]
    data.to_csv(tempDataUrl + '_data2.csv', index=False)
    return jsonStr({
        'message': '过滤成功'
    })


# 行为识别画像
@app.route('/r2')
def r2():
    data = readCsv(tempDataUrl + '_data2.csv')
    s = []
    headers = list(data.head(0))
    L = []
    for header in headers:
        L.append(list(data[header]))
    for i in range(len(L[0])):
        _s = {}
        for j in range(len(headers)):
            _s.update({
                headers[j]: L[j][i],
            })
        s.append(_s)
    return jsonStr(s)


# 分组标识读取
@app.route('/<jzid>/readFzbs')
def readFzbs(jzid):
    data = readCsv(tempDataUrl + 'data1_2.csv')
    data = data[data['就诊ID'] == jzid]
    return jsonStr({
        'group': firstValue(data, '分组标识')
    })


# 分组标识修改
@app.route('/<jzid>/<group>/addFzbs')
def addFzbs(jzid, group):
    data = readCsv(tempDataUrl + 'data1_2.csv')
    _data = data[data['就诊ID'] == jzid]
    _data.loc[:, '分组标识'] = int(group)
    data = data[data['就诊ID'] != jzid]
    data = pd.concat([data, _data])
    data.to_csv(tempDataUrl + 'data1_2.csv', index=False)
    return jsonStr({
        'message': '分组标记成功'
    })


# 修改分组标识
@app.route('/<jzid>/<group>/initFzbs')
def initFzbs(jzid, group):
    data = readCsv(tempDataUrl + 'data2.csv')
    _data = data[data['就诊ID'] == jzid]
    _data.loc[:, '分组标识'] = int(group)
    data = data[data['就诊ID'] != jzid]
    data = pd.concat([data, _data])
    data.to_csv(tempDataUrl + 'data2.csv', index=False)
    return jsonStr({
        'message': '分组修改成功'
    })


# 加载分组标识个数
@app.route('/fzbsUnique')
def fzbsUnique():
    data = readCsv(tempDataUrl + 'data2.csv')
    return jsonStr({
        'fzbsflL': list(data['分组标识'].unique())
    })


# 排行榜画像可选字段
@app.route('/rankHeaders2')
def rankHeaders2():
    data = readCsv(tempDataUrl + 'data2.csv')
    headers = []
    for header in list(data.head(0)):
        if not header in ['就诊ID', 'x', 'y', "人员信息分类", "分组标识"]:
            headers.append(header)
    return jsonStr({
        'rankHeaders2': headers
    })


# 某占比排行
@app.route('/rank2', methods=['POST'])
def rank2():
    rFile = request.json
    ratio = rFile['ratio']
    L = rFile['L']
    data = readCsv(tempDataUrl + 'data2.csv')
    data = data[data['分组标识'].isin(L)]
    s = []
    jzidL = list(data['就诊ID'])
    valueL = list(data[ratio])
    for i in range(len(jzidL)):
        s.append({
            'name': jzidL[i],
            'value': valueL[i]
        })
    return jsonStr(s)


# rank2点击后的返回的数据
@app.route('/<x>/<yljgml>/rank2Click')
def rank2Click(x, yljgml):
    data = readCsv(tempDataUrl + 'data2.csv')
    data = data[data['就诊ID'] == x]
    _s = {}
    for header in list(data.head(0)):
        _s.update({
            header: firstValue(data, header),
        })
    # 某对象的消费占比
    d = dataR3[dataR3['就诊ID'] == x]
    valueHeaders = ['医保认可费用总额', '个人支付金额']
    L = ['医药机构目录名称']
    for c in valueHeaders:
        L.append(c)
    d = d[L]
    s1 = []
    for i in list(d['医药机构目录名称'].unique()):
        dd = d[d['医药机构目录名称'] == i]
        for j in valueHeaders:
            s1.append({
                'name1': i,
                'name2': j,
                'value': returnValue(dd, j, 'sum')
            })
    # 某对象某项目消费情况
    d = dataR3[dataR3['就诊ID'] == x]
    d = d[d['医保目录名称'] == yljgml]
    s2 = []
    for i in ['全自费金额', '超限价自费费用', '先行自付金额', '符合范围金额']:
        try:
            s2.append({
                'name1': i,
                'value': firstValue(d, i)
            })
        except:
            a = 1
    return jsonStr({
        'feature': _s,
        'lngLat': [_s['x'], _s['y']],
        's1': s1,
        's2': s2
    })


# rank2点击后的返回的数据(单开一个饼状图返回数据)
@app.route('/<x>/<yljgml>/rank2Click_s2')
def rank2Click_s2(x, yljgml):
    # 某对象某项目消费情况
    d = dataR3[dataR3['就诊ID'] == x]
    d = d[d['医保目录名称'] == yljgml]
    s2 = []
    for i in ['全自费金额', '超限价自费费用', '先行自付金额', '符合范围金额']:
        try:
            s2.append({
                'name1': i,
                'value': firstValue(d, i)
            })
        except:
            a = 1
    return jsonStr({
        's2': s2
    })
