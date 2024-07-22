from _1_main import *

data1 = readCsv(dataUrl + 'data1.csv')
dataR3 = readCsv(dataUrl + '综合数据.csv')


@app.route('/tzxl1')
def tzxl1():
    """
    :return: 返回人员信息分类的可选特征序列
    """
    headers = []
    for header in list(data1.head(0)):
        if header != '就诊ID':
            headers.append(header)
    return jsonStr({
        'tzxl1': headers
    })


@app.route('/tzxled1')
def tzxled1():
    """
    :return: 返回默认特征序列
    """
    headers = []
    data = readCsv(tempDataUrl + "data1.csv")
    for header in list(data.head(0)):
        if not header in ['就诊ID', 'x', 'y', '人员信息分类']:
            headers.append(header)
    return jsonStr({
        'tzxl1': headers
    })


@app.route('/classify1', methods=['POST', 'GET'])
def classify1():
    """
    :return: 人员信息分类
    """
    rFile = request.json
    headers = ['就诊ID']
    for c in rFile['headers']:
        headers.append(c)
    classifyNum = int(rFile['classifyNum'])
    randomState = int(rFile['randomState'])
    classifyType = rFile['classifyType']
    data = data1[headers]
    if classifyType == 'kmeans':
        data = kmClsAuto(data, classifyNum, '人员信息分类', randomState)
    elif classifyType == 'tsne':
        data = pd.concat([data, tsnePosAuto(data, 1)], axis=1)
        data = modify(data, 'x', '人员信息分类')
        data = transHeaderType(data, '人员信息分类', 'int32')
        _data = quality(data, '人员信息分类')
        data.loc[:, '人员信息分类'] = _data['_人员信息分类']
        maxL = maxs(list(data['人员信息分类']))
        minL = mins(list(data['人员信息分类']))
        data.loc[:, '人员信息分类'] = ((maxL - minL) // (data['人员信息分类'] - minL + 1)) % classifyNum
    data = pd.concat([data, tsnePosAuto(data)], axis=1)
    data.to_csv(tempDataUrl + 'data1.csv', index=False)
    # 每次创建新的分类都会生成新的异常标记数据
    s = []
    L = list(data['就诊ID'])
    for i in L:
        s.append({
            '就诊ID': i,
            '分组标识': 0
        })
    pd.DataFrame(s).to_csv(tempDataUrl + 'data1_2.csv', index=False)
    return jsonStr({
        'message': '分类成功'
    })


@app.route('/classify1Score', methods=['POST', 'GET'])
def classify1Score():
    """
    :return: 人员信息分类分数
    """
    rFile = request.json
    headers = ['就诊ID']
    for c in rFile['headers']:
        headers.append(c)
    classifyNum = int(rFile['classifyNum'])
    randomState = int(rFile['randomState'])
    data = data1[headers]
    _data = readCsv(tempDataUrl + 'data1.csv')[['就诊ID', 'x', 'y']]
    s = []
    datas = {}
    for i in range(2, 12):
        textHeaders = []
        for header in headers:
            if data[header].dtypes == 'object':
                textHeaders.append(header)
        dd = kmeansClassifyWithScore(data, list(data.head(0))[1:], i, '人员信息分类', textHeaders, randomState)
        s.append({
            'name': str(i),
            'type': str(int(i == classifyNum)),
            'value': dd['score']
        })
        dd = dd['data'][['就诊ID', '人员信息分类']]
        dd = mergeLR(dd, _data, ['就诊ID'])
        _s = []
        xL = list(dd['x'])
        yL = list(dd['y'])
        cL = list(dd['人员信息分类'])
        for j in range(len(xL)):
            _s.append({
                'x': xL[j],
                'y': yL[j],
                'type': cL[j]
            })
        datas.update({
            str(i): _s
        })
    return jsonStr({
        'score': s,
        'datas': datas
    })


@app.route('/sxHeader1')
def sxHeader1():
    """
    :return: 筛选字段
    """
    data = readCsv(tempDataUrl + 'data1.csv')
    headers = []
    for header in list(data.head(0)):
        if not header in ['就诊ID', '人员信息分类', 'x', 'y'] and data[header].dtypes != 'object':
            headers.append(header)
    return jsonStr({
        'headers': headers
    })


@app.route('/<x>/sxValue1')
def sxValue1(x):
    """
    :return: 筛选值
    """
    data = readCsv(tempDataUrl + 'data1.csv')
    return jsonStr({
        'values': list(data[x].unique())
    })


@app.route('/<x>/sxValues1')
def sxValues1(x):
    """
    :return: 筛选值
    """
    data = readCsv(tempDataUrl + 'data1.csv')
    L = list(data[x].unique())
    return jsonStr({
        'min': mins(L),
        'max': maxs(L)
    })


# 过滤数据
@app.route('/data1Gl', methods=['POST', 'GET'])
def data1Gl():
    rFile = request.json
    data = readCsv(tempDataUrl + 'data1.csv')
    sxValueRange = rFile['sxValueRange']
    for header in sxValueRange:
        L = sxValueRange[header]
        data = data[data[header] >= L[0]]
        data = data[data[header] <= L[1]]
    data.to_csv(tempDataUrl + '_data1.csv', index=False)
    return jsonStr({
        'message': '过滤成功'
    })


# 人员信息分类聚类画像
@app.route('/r1')
def r1():
    data = readCsv(tempDataUrl + '_data1.csv')
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


# 群体标记分组
@app.route('/fzbj', methods=['POST'])
def fzbj():
    rFile = request.json
    jzid = rFile['jzid']
    fzbsValue = rFile['fzbsValue']
    data = readCsv(tempDataUrl + 'data1_2.csv')
    L = []
    for c in list(data['就诊ID']):
        if not c in jzid:
            L.append(c)
    _data = data[data['就诊ID'].isin(jzid)]
    data = data[data['就诊ID'].isin(L)]
    _data.loc[:, '分组标识'] = fzbsValue
    data = pd.concat([data, _data])
    data.to_csv(tempDataUrl + 'data1_2.csv', index=False)
    return jsonStr({
        'message': '标记成功'
    })


# 排行榜画像可选字段
@app.route('/rankHeaders1')
def rankHeaders1():
    return jsonStr({
        'rankHeaders1': [
            '报销平均频率', '报销最大频率', '报销最大金额', '小额多次', '先行自付占比', '超限价自付占比', '全自费占比',
            '医疗费总额', '实际支付起付线', '统筹基金支出', '基本医疗统筹支付比例', '医保认可费用总额', '公务员医疗补助资金支出',
            '大病补充医疗保险基金支出', '医疗救助基金支出', '个人账户支出', '个人支付金额'
        ]
    })


# 某医疗目录下报销比例占比情况
@app.route('/rank1', methods=['POST'])
def rank1():
    rFile = request.json
    yljgml = rFile['yljgml']
    ratio = rFile['ratio']
    L = rFile['L']  # 筛选的人员分类信息列表
    data = dataR3[dataR3['医保目录名称'] == yljgml]
    _data = readCsv(tempDataUrl + "data1.csv")
    _data = _data[_data['人员信息分类'].isin(L)]
    data = data[data['就诊ID'].isin(list(
        _data['就诊ID'].unique()
    ))]
    s = []
    data = drop(data, ['就诊ID'])
    jzidL = list(data['就诊ID'])
    valueL = list(data[ratio])
    for i in range(len(jzidL)):
        s.append({
            'name': jzidL[i],
            'value': valueL[i]
        })
    return jsonStr(s)


# rank1点击后的返回的数据
@app.route('/<x>/rank1Click', methods=['POST'])
def rank1Click(x):
    data = readCsv(tempDataUrl + 'data1.csv')
    data = data[data['就诊ID'] == x]
    _s = {}
    for header in list(data.head(0)):
        _s.update({
            header: firstValue(data, header),
        })
    """
    某一对象的报销占比画像
    """
    d = dataR3[dataR3['就诊ID'] == x]
    data = readCsv(tempDataUrl + 'data1.csv')
    ryxxfl = firstValue(data[data['就诊ID'] == x], '人员信息分类')
    jzidL = list(data[data['人员信息分类'] == ryxxfl]['就诊ID'].unique())
    dd = dataR3[dataR3['就诊ID'].isin(jzidL)]
    s1 = {}
    for i in ['报销平均频率', '报销最大频率', '报销最大金额', '小额多次']:
        s1.update({
            i: round(firstValue(d, i) / max(1, maxs(list(dd[i]))), 4)
        })
    s3 = []
    for i in ['报销平均频率', '报销最大频率', '报销最大金额', '小额多次']:
        s3.append({
            'name': i,
            'type': '组内平均',
            'value': firstValue(dd, i)
        })
        s3.append({
            'name': i,
            'type': x,
            'value': firstValue(d, i)
        })
    """
    某一对象的整个医药支付转移记录（有时间线）
    """
    rFile = request.json
    ybjgmls = rFile['ybjgmls']
    d = dataR3[dataR3['就诊ID'] == x]
    d = d[['就诊ID', '结算时间', '医药机构目录名称', '个人支付金额', '医疗费总额', '明细项目费用总额', '符合范围金额']]
    d = drop(d, ['就诊ID', '结算时间', '医药机构目录名称', '明细项目费用总额', '符合范围金额'])
    nodes = []
    edges = []
    for i in list(d['结算时间'].unique()):
        dd = d[d['结算时间'] == i]
        for j in ybjgmls:
            ddd = dd[dd['医药机构目录名称'] == j]
            try:
                nodes.append({
                    'id': str(j),
                    'label': str(j),
                    'donutAttrs': {
                        '个人支付费用': 20 * round(
                            firstValue(ddd, '明细项目费用总额') - firstValue(ddd, '符合范围金额'), 2
                        ) / firstValue(ddd, '明细项目费用总额'),
                        '报销费用': 20 * (1 - round(
                            firstValue(ddd, '明细项目费用总额') - firstValue(ddd, '符合范围金额'), 2
                        ) / firstValue(ddd, '明细项目费用总额')),
                    },
                })
                edges.append({
                    'source': str(j),
                    'target': str(i),
                    'value': firstValue(ddd, '符合范围金额'),
                    'size': round(
                        1000 * min(firstValue(ddd, '符合范围金额') / firstValue(dd, '医疗费总额'), 0.3), 2
                    ),  # 报销的钱作为路径宽度
                })
            except:
                continue
        try:
            nodes.append({
                'id': str(i),
                'label': str(i),
                'donutAttrs': {
                    '个人支付费用': 20 * firstValue(dd, '个人支付金额') / firstValue(dd, '医疗费总额'),
                    '报销费用': 20 * (1 - firstValue(dd, '个人支付金额') / firstValue(dd, '医疗费总额')),
                },
            })
        except:
            s = s
    return jsonStr({
        'feature': _s,
        'lngLat': [_s['x'], _s['y']],
        'chart1': s1,
        'chart2': {
            'nodes': nodes,
            'edges': edges
        },
        'chart3': s3,
    })


@app.route('/download/<csvName>')
def download_data1(csvName):
    data = readCsv(tempDataUrl + csvName + '.csv')
    headers = []
    for header in list(data.head(0)):
        if not header in ['x', 'y']:
            headers.append(header)
    return data[headers].to_csv(index=False)
