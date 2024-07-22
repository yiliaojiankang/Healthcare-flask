from _1_main import *

data1 = readCsv(rowDataUrl + '包含坐标的患者信息.csv')
data2 = readCsv(dataUrl + '病案首页表1.csv')
data3 = readCsv(dataUrl + '病案首页表2.csv')
data4 = readCsv(rowDataUrl + '病案首页表.csv')
data5 = readCsv(rowDataUrl + '患者门诊诊断表.csv')
data6 = readCsv(rowDataUrl + '检查信息.csv')
data7 = readCsv(rowDataUrl + '检验数据-2022.csv')
data8 = readCsv(dataUrl + '器官保养建议.csv')




# 删除相似度高的
def initDele():
    s = ""
    for i in list(data6['检查结论'].unique()):
        dd = data6[data6['检查结论'] == i]
        s += i * len(dd)
    _ks = keys(s, 30)
    for c in _ks:
        deles.update(c)


qgImg = {
    '脑': '🧠',
    '鼻': '👃',
    '眼': '👀',
    '喉': '👄',
    '耳': '👂',
    '肺': '🫁',
    '心': '🫀',
    '肝胆': '肝胆',
    '胰': '胰',
    '胃': '胃',
    '小肠': '小肠',
    '大肠': '大肠',
    '肾': '肾',
    '泌尿': '泌尿',
    '腿': '🦴',
    '血管': '🩸',
    '手': '👋'
}


@app.route('/<xb>/<age>/<qg>/body2')
def body2(xb, age, qg):
    datas = []
    for i in xb:
        for j in str(age).split(','):
            try:
                datas.append(pd.read_csv('./data/body2/' + str(i) + "/" + str(j) + "/" + str(qg) + '/body2.csv'))
            except:
                continue
    data = pd.concat(datas)
    data = data.sort_values(by=['value'], ascending=False)[: 30]
    s = []
    name = list(data.head(0))[0]
    names = list(data[name])[:30]
    values = list(data['value'])[:30]
    sumValue = max(sums(list(data['value'])), 1)
    for i in range(len(names)):
        value = round(values[i] / sumValue, 2)
        if value < 0.2:
            s.append({
                'name': names[i],
                'value': 0.2
            })
        else:
            s.append({
                'name': names[i],
                'value': value
            })
    return jsonStr(s)


@app.route('/<xb>/<age>/<qg>/body3_1')
def body3_1(xb, age, qg):
    data = pd.read_csv('./data/body3/' + str(xb) + "/" + str(age) + "/" + str(qg) + '/body3_1.csv')
    data = data.sort_values(by=['value'], ascending=False)
    s = []
    name = list(data.head(0))[0]
    names = list(data[name])[:5]
    values = list(data['value'])[:5]
    sumValue = max(sums(list(data['value'])), 1)
    for i in range(len(names)):
        s.append({
            'name': names[i],
            'value': round(values[i] / sumValue, 2)
        })
    return jsonStr(s)


@app.route('/<xb>/<age>/<qg>/body3_2')
def body3_2(xb, age, qg):
    data = pd.read_csv('./data/body3/' + str(xb) + "/" + str(age) + '/body3_2.csv')
    data = data.sort_values(by=['value'], ascending=False)
    s = []
    name = list(data.head(0))[0]
    sumValue = max(sums(list(data['value'])), 1)
    value = sums(list(data[data[name] == qg]['value']))
    return jsonStr({
        'value': round(value / sumValue, 4)
    })


@app.route('/<xb>/<age>/<qg>/body3_3')
def body3_3(xb, age, qg):
    data = pd.read_csv('./data/body3/' + str(xb) + "/" + str(age) + "/" + str(qg) + '/body3_3.csv')
    s = []
    name = list(data.head(0))[0]
    sumValue = max(sums(list(data['value'])), 1)
    for i in range(1, 13):
        d = data[data[name] == int(i)]
        s.append({
            'name': str(i) + "月",
            'value': round(sums(list(d['value'])) / sumValue, 2)
        })
    return jsonStr(s)


@app.route('/md1', methods=['POST', 'GET'])
def md1():
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    data = data1[data1['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    names1 = list(data['就诊编码'])
    names2 = list(data['患者编码'])
    xbs = list(data['性别'])
    ages = list(data['年龄'])
    zdmcs = list(data['诊断名称'])
    qgmcs = list(data['器官名称'])
    r1s = list(data['r1'])
    r2s = list(data['r2'])
    r3s = list(data['r3'])
    r4s = list(data['r4'])
    x = list(data['x'])
    y = list(data['y'])
    z = list(data['z'])
    types = list(data['人员类别'])
    s = []
    for i in range(len(names1)):
        s.append({
            'name1': names1[i],
            'name2': names2[i],
            'xb': xbs[i],
            'age': ages[i],
            'zdmc': zdmcs[i],
            'qgmc': qgmcs[i],
            'type': types[i],
            'r1': r1s[i],
            'r2': r2s[i],
            'r3': r3s[i],
            'r4': r4s[i],
            'jd': x[i],
            'wd': y[i],
        })
    return jsonStr(s)


@app.route('/md2', methods=['POST', 'GET'])
def md2():
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    colors = rFile['colors']
    data = data2[data2['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    data = data.sort_values(by=['住院次数'], ascending=False)
    s = []
    for i in list(data['出院病区'].unique())[:10]:
        dd = data[data['出院病区'] == i]
        _s = {
            'name': str(i),
            'itemStyle': {
                'color': colors[
                    cntMaxI(list(dd['人员类别']))
                ]
            },
            'children': []
        }
        for j in list(dd['器官名称'].unique()):
            ddd = dd[dd['器官名称'] == j]
            __s = {
                'name': str(j),
                'itemStyle': {
                    'color': colors[
                        cntMaxI(list(ddd['人员类别']))
                    ]
                },
                'children': []
            }
            for k in list(ddd['诊断名称'].unique()):
                dddd = ddd[ddd['诊断名称'] == k]
                __s['children'].append({
                    'name': str(k),
                    'itemStyle': {
                        'color': colors[
                            cntMaxI(list(dddd['人员类别']))
                        ]
                    },
                    'value': returnValue(dddd)
                })
            _s['children'].append(__s)
        s.append(_s)
    return jsonStr({
        'name': 'root',
        'children': s
    })


@app.route('/sxValuesForMd2', methods=['POST', 'GET'])
def sxValuesForMd2():
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    data = data2[data2['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    return jsonStr({
        'qgmcs': list(data['器官名称'].unique()),
        'rylbs': list(data['人员类别'].unique()),
    })


@app.route('/mainQgmc', methods=['POST', 'GET'])
def mainQgmc():
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    data = data1[data1['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    s = []
    for i in list(data['器官名称'].unique()):
        dd = data[data['器官名称'] == i]
        s.append({
            '器官名称': i,
            'value': returnValue(dd)
        })
    data = pd.DataFrame(s)
    data = data.sort_values(by=['value'], ascending=False)
    data = data[data['器官名称'] != '血管']
    names = list(data['器官名称'].unique())[: 5]
    values = []
    for i in names:
        dd = data[data['器官名称'] == i]
        values.append(returnValue(dd, 'value', 'sum'))
    return jsonStr({
        'mainQgmc': names,
        'values': values,
        'max': maxs(values),
    })


@app.route('/<x>/md3')
def md3(x):
    if x == '肝脏' or '胆' in x:
        x = '肝胆'
    data = data3[data3['器官名称'] == x]
    s1 = []
    for i in range(1, 13):
        dd = data[data['入院月'] == int(i)]
        s1.append({
            'name': i,
            'value': returnValue(dd)
        })
    s2 = []
    for i in range(60, 103):
        dd = data[data['年龄'] == int(i)]
        s2.append({
            'name': i,
            'value': returnValue(dd)
        })
    s3 = []
    for i in list(data['主诊断名称'].unique()):
        dd = data[data['主诊断名称'] == i]
        s3.append({
            'name': i,
            'value': returnValue(dd)
        })
    dd = pd.DataFrame(s3)
    dd = dd.sort_values(by=['value'], ascending=False)
    s3 = []
    names = list(dd['name'])
    values = list(dd['value'])
    for i in range(0, min(len(names), 30)):
        s3.append({
            'name': names[i],
            'value': values[i]
        })
    s4 = []
    for i in ['男', '女']:
        dd = data[data['性别'] == i]
        s4.append({
            'name': i,
            'value': returnValue(dd)
        })
    return jsonStr({
        'data1': s1,
        'data2': s2,
        'data3': s3,
        'data4': s4
    })


"""
第二页
"""


@app.route('/<x>/md4', methods=['POST', 'GET'])
def md4(x):
    datas = []
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    xbs = rFile['xb']
    for xb in xbs:
        for age in range(age1, age2 + 1):
            try:
                datas.append(readCsv(dataUrl + 'd2_1/' + xb + '/' + str(age) + '/' + x + '/d2_1.csv'))
            except:
                continue
    data = pd.concat(datas)
    s = []
    for i in list(data['主诊断名称'].unique()):
        dd = data[data['主诊断名称'] == i]
        for j in list(dd['其它诊断名称1'].unique()):
            ddd = dd[dd['其它诊断名称1'] == j]
            s.append({
                '主诊断名称': i,
                '其他诊断名称': j,
                'value': returnValue(ddd, 'value', 'sum')
            })
    # 主诊断名称
    names = list(data['其它诊断名称1'].unique())
    data = pd.DataFrame(s)
    # 为了节省渲染时间
    data = data[data['主诊断名称'].isin(list(data2['诊断名称'].unique()))][: len(data) // 10]
    nodes = []
    links = []
    categories = []
    _d = data2.sort_values(by=['人员类别'])
    for i in list(_d['人员类别'].unique()):
        categories.append({
            'name': str(i)
        })
    I = 0
    for i in list(data['主诊断名称'].unique()):
        dd = data[data['主诊断名称'] == i]
        dd1 = data2[data2['诊断名称'] == i]
        nodes.append({
            "id": str(I),
            'name': i,
            "x": returnValue(dd1, 'x', 'avr'),
            "y": returnValue(dd1, 'y', 'avr'),
            "symbolSize": min(returnValue(dd, 'value', 'sum'), 5),
            "value": min(returnValue(dd, 'value', 'sum'), 5),
            # "symbolSize": 10,
            # 'value': 10,
            "category": cntMaxI(list(dd1['人员类别']))
        })
        J = I + 1
        for j in list(dd['其他诊断名称'].unique()):
            ddd = dd[dd['其他诊断名称'] == j]
            dd2 = data2[data2['诊断名称'] == i]
            nodes.append({
                "id": str(J),
                'name': j,
                "x": returnValue(dd2, 'x', 'avr'),
                "y": returnValue(dd2, 'y', 'avr'),
                "symbolSize": min(returnValue(ddd, 'value', 'sum'), 5),
                "value": min(returnValue(ddd, 'value', 'sum'), 5),
                # "symbolSize": 10,
                # 'value': 10,
                "category": cntMaxI(list(dd2['人员类别']))
            })
            links.append({
                "source": str(I),
                "target": str(J)
            })
            J += 1
        I = J
    """
    分析主要患病器官
    """
    s = []
    for i in names:
        s.append({
            'name': i,
        })
    data = pd.DataFrame(s)
    data = drop(data, ['name'])
    data = data2[data2['诊断名称'].isin(list(data['name'].unique()))]
    s = []
    for i in list(data['器官名称'].unique()):
        if x != i:
            dd = data[data['器官名称'] == i]
            s.append({
                'name': i,
                'value': returnValue(dd)
            })
    return jsonStr({
        'nodes': nodes,
        'links': links,
        'categories': categories,
        'md4': s,
    })


@app.route('/<x>/md5', methods=['POST', 'GET'])
def md5(x):
    datas = []
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    xbs = rFile['xb']
    for xb in xbs:
        for age in range(age1, age2 + 1):
            try:
                datas.append(readCsv(dataUrl + 'd2_1/' + xb + '/' + str(age) + '/' + x + '/d2_1.csv'))
            except:
                continue
    data = pd.concat(datas)
    s = []
    for i in list(data['主诊断名称'].unique()):
        dd = data[data['主诊断名称'] == i]
        for j in list(dd['其它诊断名称1'].unique()):
            ddd = dd[dd['其它诊断名称1'] == j]
            s.append({
                '诊断名称': i,
                '其他诊断名称': j,
                'value': returnValue(ddd, 'value', 'sum')
            })
    data = pd.DataFrame(s)
    names = list(data['诊断名称'].unique())
    for name in list(data['其他诊断名称'].unique()):
        if not name in names:
            names.append(name)
    _data = data2[data2['诊断名称'].isin(names)][['诊断名称', '器官名称', '人员类别']]
    _data = _data.sort_values(by=['人员类别'])
    s = []
    for i in list(_data['人员类别'].unique()):
        dd = _data[_data['人员类别'] == i]
        for j in list(dd['器官名称'].unique()):
            ddd = dd[dd['器官名称'] == j]
            s.append({
                'name1': i,
                'name2': j,
                'value': returnValue(ddd)
            })
            for k in list(ddd['诊断名称'].unique()):
                dddd = ddd[ddd['诊断名称'] == k]
                s.append({
                    'name1': j,
                    'name2': k,
                    'value': returnValue(dddd)
                })
    return jsonStr(s)


@app.route('/md6', methods=['POST', 'GET'])
def md6():
    datas = []
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    xbs = rFile['xb']
    for xb in xbs:
        for age in range(age1, age2 + 1):
            try:
                datas.append(readCsv(dataUrl + 'd2_2/' + xb + '/' + str(age) + '/d2_2.csv'))
            except:
                continue
    data = pd.concat(datas)
    s = []
    name1 = list(data.head(0))[0]
    name2 = list(data.head(0))[1]
    for i in list(data[name2].unique())[:8]:
        if i != '血管':
            d = data[data[name2] == i]
            d = d.sort_values(by=['value'], ascending=False)
            s.append({
                "sets": [i],
                # "sets": [qgImg[i]],
                "size": sums(list(d['value'])),
            })
            dd = data[data[name1] == list(d[name1].unique())[0]]
            dd = dd.sort_values(by=['value'], ascending=False)
            for j in list(dd[name2].unique())[:5]:
                if i != j and j != '血管':
                    s.append({
                        "sets": [i, j],
                        # "sets": [qgImg[i], qgImg[j]],
                        "size": sums(list(dd['value'])),
                    })
    return jsonStr(s)


@app.route('/<x>/md7', methods=['POST', 'GET'])
def md7(x):
    datas = []
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    xbs = rFile['xb']
    for xb in xbs:
        for age in range(age1, age2 + 1):
            try:
                datas.append(readCsv(dataUrl + 'd2_3/' + xb + '/' + str(age) + '/' + x + '/d2_3.csv'))
            except:
                continue
    data = pd.concat(datas)
    s = []
    name = list(data.head(0))[0]
    for i in list(data[name].unique()):
        dd = data[data[name] == i]
        s.append({
            'name': i,
            'value': sums(list(dd['value']))
        })
    return jsonStr({
        'name': '',
        'children': s
    })


"""
既往史
"""


@app.route('/<x>/_md1', methods=['POST', 'GET'])
def _md1(x):
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    data = data1[data1['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    data = data[data['器官名称'] == x]
    names1 = list(data['就诊编码'])
    names2 = list(data['患者编码'])
    xbs = list(data['性别'])
    ages = list(data['年龄'])
    zdmcs = list(data['诊断名称'])
    qgmcs = list(data['器官名称'])
    r1s = list(data['r1'])
    r2s = list(data['r2'])
    r3s = list(data['r3'])
    r4s = list(data['r4'])
    x = list(data['x'])
    y = list(data['y'])
    z = list(data['z'])
    types = list(data['人员类别'])
    s = []
    for i in range(len(names1)):
        s.append({
            'name1': names1[i],
            'name2': names2[i],
            'xb': xbs[i],
            'age': ages[i],
            'zdmc': zdmcs[i],
            'qgmc': qgmcs[i],
            'type': types[i],
            'r1': r1s[i],
            'r2': r2s[i],
            'r3': r3s[i],
            'r4': r4s[i],
            'jd': x[i],
            'wd': y[i],
        })
    return jsonStr(s)


@app.route('/<x>/md8', methods=['POST', 'GET'])
def md8(x):
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    data = data1[data1['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    data = data[data['器官名称'] == x]
    names = list(data['就诊编码'].unique())
    data = data3[data3['就诊编码'].isin(names)]
    data = drop(data, ['就诊编码'])
    s = []
    L = []
    headers = []
    for header in list(data.head(0)):
        if not header in ['入院年', '入院月', '入院日', '入院时', '入院分',
                          '入院秒', '出院年', '出院月', '出院日', '出院时', '出院分', '出院秒', '器官名称',
                          ]:
            headers.append(header)
    columns = []
    for header in headers:
        L.append(list(data[header]))
        columns.append({
            "prop": header,
            "label": header,
            "width": 150
        })
    for i in range(min(len(L[0]), 100)):
        _s = {}
        for j in range(len(L)):
            _s.update({
                headers[j]: str(L[j][i]).replace('"', "").replace("'", "")
            })
        s.append(_s)
    return jsonStr({
        "data": s,
        "columns": columns
    })


@app.route('/<x>/jzidToGfqg')
def jzidToGfqg(x):
    data = data3[data3['就诊编码'] == x]
    return jsonStr({
        'names': list(data['器官名称'].unique())
    })


@app.route('/<x>/md9', methods=['POST', 'GET'])
def md9(x):
    data = data3[data3['就诊编码'] == x]
    gfqg = list(data['器官名称'].unique())
    zdmc = list(data['主诊断名称'].unique())
    xb = firstValue(data, '性别')
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    datas = []
    for age in range(age1, age2 + 1):
        for qg in gfqg:
            try:
                datas.append(readCsv(dataUrl + 'd2_1/' + xb + '/' + str(age) + '/' + qg + '/d2_1.csv'))
            except:
                continue
    data = pd.concat(datas)
    data = data.sort_values(by=['value'], ascending=False)
    data = data[: 30]
    s = []
    name1 = list(data.head(0))[0]
    name2 = list(data.head(0))[1]
    for i in list(data[name1].unique()):
        dd = data[data[name1] == i]
        for j in list(dd[name2].unique()):
            ddd = dd[dd[name2] == j]
            s.append({
                'name1': i,
                'name2': j,
                'type': int(i in zdmc or j in zdmc),
                'value': returnValue(ddd, 'value', 'sum')
            })
    return jsonStr(s)


@app.route('/<x>/md10')
def md10(x):
    data = data4[data4['就诊编码'] == x]
    s = []
    for i in list(data['器官名称'].unique()):
        dd = data[data['器官名称'] == i]
        for j in list(dd['出院病区'].unique()):
            ddd = dd[dd['出院病区'] == j]
            s.append({
                'name1': i,
                'name2': j,
                'value': returnValue(ddd, '住院次数', 'sum')
            })
            for k in list(ddd['主诊断名称'].unique()):
                dddd = ddd[ddd['主诊断名称'] == k]
                s.append({
                    'name1': j,
                    'name2': k,
                    'value': returnValue(dddd, '住院次数', 'sum')
                })
            for c in range(1, 5):
                for k in list(ddd['其它诊断名称' + str(c)].unique()):
                    dddd = ddd[ddd['其它诊断名称' + str(c)] == k]
                    s.append({
                        'name1': j,
                        'name2': k,
                        'value': returnValue(dddd, '住院次数', 'sum')
                    })
    return jsonStr(s)


@app.route('/<x>/md11', methods=['POST', 'GET'])
def md11(x):
    rFile = request.json
    age1 = int(rFile['age1'])
    age2 = int(rFile['age2'])
    data = data1[data1['年龄'] >= int(age1)]
    data = data[data['年龄'] <= int(age2)]
    data = data[data['器官名称'] == x]
    names = list(data['就诊编码'].unique())
    data = data3[data3['就诊编码'].isin(names)]
    s = []
    L = list(data['就诊编码'].unique())
    for i in range(len(L)):
        dd = data[data['就诊编码'] == L[i]]
        s.append({
            'name': cntMaxI(list(dd['主诊断名称'])) + '_' + str(i),
            'id': L[i],
            'value': returnValue(dd, '住院次数', 'sum')
        })
    return jsonStr(s)


@app.route('/<x>/md12')
def md12(x):
    data = data2[data2['诊断名称'] == x]
    names = list(data['就诊编码'].unique())
    data = data6[data6['就诊编码'].isin(names)]
    s = ""
    for i in list(data['检查结论'].unique()):
        dd = data[data['检查结论'] == i]
        s += i * len(dd)
    _k = keys(s, 50, deles)
    _w = weights(s, 50, deles)
    s = []
    for i in range(len(_k)):
        s.append({
            'name': _k[i],
            'value': _w[i]
        })
    return jsonStr(s)


"""
第四页
"""


@app.route('/jyxm')
def jyxm():
    data = data7.sort_values(by=['检验明细项目'])
    return jsonStr({
        'jyxm': list(data['检验明细项目'].unique())
    })


@app.route('/<x>/<y>/ycbs')
def ycbs(x, y):
    data = data7[data7['检验明细项目'] == x]
    value = firstValue(data, '参考范围').split('-')
    y = float(y)
    try:
        minL = float(value[0])
        maxL = float(value[2])

    except:
        minL = 0
        maxL = 1
    if y < minL:
        return jsonStr({
            'ycbs': '↓'
        })
    elif y > maxL:
        return jsonStr({
            'ycbs': '↑'
        })


@app.route('/preZdmc', methods=['POST', 'GET'])
def preZdmc():
    rFile = request.json
    _jyxm = rFile['jyxm']
    _ycbs = rFile['ycbs']
    _age = rFile['age']
    _xb = rFile['xb']
    data = data7[data7['检验明细项目'] == _jyxm]
    if _ycbs == '↑':
        data = data[data['异常结果标识'].isin(['↑', 'H'])]
    elif _ycbs == '↓':
        data = data[data['异常结果标识'].isin(['↓', 'L'])]
    names = list(data['就诊编码'].unique())
    data = data3[data3['就诊编码'].isin(names)]
    data = data[data['年龄'] >= int(_age) - 5]
    data = data[data['年龄'] <= int(_age) + 5]
    data = data[data['性别'] == _xb]
    data = data[['器官名称', '主诊断名称']]
    s = []
    for i in list(data['主诊断名称'].unique()):
        dd = data[data['主诊断名称'] == i]
        s.append({
            '诊断名称': i,
            'value': returnValue(dd)
        })
    s = pd.DataFrame(s).sort_values(by=['value'], ascending=False)
    zdmcs = list(s['诊断名称'].unique())
    zdmcValues = list(s['value'].unique())
    s = []
    for i in list(data['器官名称'].unique()):
        dd = data[data['器官名称'] == i]
        s.append({
            '器官名称': i,
            'value': returnValue(dd)
        })
    s = pd.DataFrame(s).sort_values(by=['value'], ascending=False)
    qgmcs = list(s['器官名称'].unique())[: 5]
    qgmcValues = list(s['value'].unique())[: 5]
    """
    共病预警
    """
    age1 = _age - 5
    age2 = _age + 5
    datas = []
    for age in range(age1, age2 + 1):
        for qg in qgmcs:
            try:
                datas.append(readCsv(dataUrl + 'd2_1/' + _xb + '/' + str(age) + '/' + qg + '/d2_1.csv'))
            except:
                continue
    data = pd.concat(datas)
    data = data.sort_values(by=['value'], ascending=False)
    data = data[: 30]
    s = []
    name1 = list(data.head(0))[0]
    name2 = list(data.head(0))[1]
    for i in list(data[name1].unique()):
        dd = data[data[name1] == i]
        for j in list(dd[name2].unique()):
            ddd = dd[dd[name2] == j]
            s.append({
                'name1': i,
                'name2': j,
                'type': int(i in zdmcs or j in zdmcs),
                'value': returnValue(ddd, 'value', 'sum')
            })
    """
    器官保养建议
    """
    ss = []
    data = data8[data8['器官名称'].isin(qgmcs[: 3])]
    for qgmc in list(data['器官名称'].unique()):
        dd = data[data['器官名称'] == qgmc]
        for i in range(1, 6):
            for j in range(6 - i):
                ss.append({
                    'name': str(firstValue(dd, '建议食物' + str(i))),
                    'value': (6 - i)
                })
    """
    疗养建议
    """
    sss = []
    for qgmc in list(data['器官名称'].unique()):
        dd = data[data['器官名称'] == qgmc]
        for i in range(1, 5):
            sss.append(str(firstValue(dd, '疗养建议' + str(i))))
    return jsonStr({
        'zdmcs': zdmcs,
        'zdmcValues': zdmcValues,
        'zdmcMax': maxs(zdmcValues),
        'qgmcs': qgmcs,
        'qgmcValues': qgmcValues,
        'qgmcMax': maxs(qgmcValues),
        'gbyj': s,  # 共病预警数据
        'ysjy': ss,  # 饮食建议
        'lyjy': sss,  # 疗养建议
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # 允许从外部访问，监听所有网络接口

# app.run(host='127.0.0.1', port=5002)
