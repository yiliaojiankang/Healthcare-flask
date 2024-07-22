from _2_L2 import *


@app.route('/r3_rela')
def r3_rela():
    data = readCsv(tempDataUrl + 'data2.csv')
    s = []
    for header in list(data.head(0)):
        if not header in ['就诊ID', 'x', 'y']:
            s.append({
                'name': header,
                'value': len(list(data[header].unique()))
            })
    s = pd.DataFrame(s)
    s = s.sort_values(by=['value'], ascending=True)
    return jsonStr({
        'r3_rela': list(s['name'])
    })


@app.route('/r3_size')
def r3_size():
    data = readCsv(tempDataUrl + 'data2.csv')
    s = []
    for header in list(data.head(0)):
        if not header in ['就诊ID', 'x', 'y']:
            s.append({
                'name': header,
                'value': len(list(data[header].unique()))
            })
    s = pd.DataFrame(s)
    s = s.sort_values(by=['value'], ascending=False)
    return jsonStr({
        'r3_size': list(s['name'])
    })


# 行为识别分类关系图
@app.route('/<x>/<y>/r3')
def r3(x, y):
    _data = readCsv(tempDataUrl + '_data1.csv')
    jzidL = list(_data['就诊ID'].unique())
    data = readCsv(tempDataUrl + '_data2.csv')
    data = data[data['就诊ID'].isin(jzidL)]
    data.loc[:, 'x'] = data['x']
    data.loc[:, 'y'] = data['y']
    s1 = []
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
        s1.append(_s)
    s2 = []
    for i in list(data[x].unique()):
        dd = data[data[x] == i]
        for j in list(data['就诊ID'].unique()):
            ddd = dd[dd['就诊ID'] == j]
            try:
                s2.append({
                    'x1': avr(list(dd['x'])),
                    'y1': avr(list(dd['y'])),
                    'x2': firstValue(ddd, 'x'),
                    'y2': firstValue(ddd, 'y'),
                    'color': firstValue(ddd, x),
                    'size': firstValue(ddd, y)
                })
            except:
                continue
    return jsonStr({
        's1': s1,
        's2': s2
    })


# 带有簇类标识的聚类图
@app.route('/l3_scatter', methods=['POST'])
def l3_scatter():
    rFile = request.json
    jzid = rFile['jzid']
    data = readCsv(tempDataUrl + 'data2.csv')
    L = list(data['就诊ID'])
    xL = list(data['x'])
    yL = list(data['y'])
    s = []
    for i in range(len(L)):
        _s = {
            'jzid': L[i],
            'x': xL[i],
            'y': yL[i],
        }
        if L[i] in jzid:
            _s.update({
                'type': '1',
                'size': 5,
            })
        else:
            _s.update({
                'type': '0',
                'size': 2,
            })
        s.append(_s)
    return jsonStr(s)


# 带有簇类标识的病种特征词云图
@app.route('/bzmcWords', methods=['POST'])
def bzmcWords():
    rFile = request.json
    jzidL = rFile['jzidL']
    data = dataR3[dataR3['就诊ID'].isin(jzidL)]
    s = []
    for i in list(data['病种名称'].unique()):
        dd = data[data['病种名称'] == i]
        if str(i) != '0':
            s.append({
                'name': i,
                'value': len(dd)
            })
    return jsonStr(s)


# 簇类关联关系热力缩影
@app.route('/relaHeat', methods=['POST'])
def relaHeat():
    rFile = request.json
    jzidL = rFile['jzidL']
    data = readCsv(tempDataUrl + 'data2.csv')
    s = []
    headers = []
    for header in list(data.head(0)):
        if not header in ['就诊ID', 'x', 'y']:
            headers.append(header)
    for i in jzidL:
        for j in jzidL:
            value = 0
            dd1 = data[data['就诊ID'] == i]
            dd2 = data[data['就诊ID'] == j]
            for header in headers:
                valueI = firstValue(dd1, header)
                valueJ = firstValue(dd2, header)
                value += 1 - round(
                    abs(valueI - valueJ) / max(max(valueI, valueJ), 1), 2
                )
            s.append({
                'name1': i,
                'name2': j,
                'value': round(value / len(headers), 2)
            })
    return jsonStr(s)

