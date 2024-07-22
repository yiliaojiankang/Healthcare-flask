from _1_main import *


# 养老机构各项指标最大值
@app.route('/maxRatio', methods=['POST'])
def maxRatio():
    rFile = request.json
    lng1 = rFile['lng1']
    lat1 = rFile['lat1']
    lng2 = rFile['lng2']
    lat2 = rFile['lat2']
    d = jgxxb[jgxxb['jd'] >= min(lng1, lng2)]
    d = d[d['jd'] <= max(lng1, lng2)]
    d = d[d['wd'] >= min(lat1, lat2)]
    d = d[d['wd'] <= max(lat1, lat2)]
    names = list(d['供应商名称'].unique())
    _s = {}
    for i in ratios:
        _s.update({
            str(i): maxs(list(d[str(i)]))
        })
    maxRzrs = 0
    for i in names:
        d = jgrzb[jgrzb['供应商名称'] == i]
        maxRzrs = max(maxRzrs, len(list(d['供应商名称'])))
    _s.update({
        '入住人数': maxRzrs
    })
    return jsonStr(_s)


# 入住人员信息
@app.route('/rzryxx')
def rzryxx():
    d = jgrzb
    return jsonStr({
        '年龄等级': list(d['年龄等级'].unique()),
        '性别': list(d['性别'].unique()),
        '老人类型': list(d['老人类型'].unique()),
        '等级': list(d['等级'].unique()),
    })


# 单个养老机构地图信息
@app.route('/<name>/jgMap')
def jgMap_single(name):
    d = jgxxb[jgxxb['供应商名称'] == name]
    _s = {
        'name': name,
        'jd': firstValue(d, 'jd'),
        'wd': firstValue(d, 'wd'),
        'type': '养老机构',
    }
    for j in ['床位数', '占地面积', '建筑面积', '绿化面积', '联系电话', '邮编', '运营模式', '证照情况', '房屋权属证明', '有产证', '无产证']:
        _s.update({
            j: firstValue(d, j),
        })
    return jsonStr([_s])


# 养老机构地图信息
@app.route('/jgMap')
def jgMap():
    s = []
    for i in list(jgxxb['供应商名称']):
        d = jgxxb[jgxxb['供应商名称'] == i]
        _s = {
            'name': i,
            'jd': firstValue(d, 'jd'),
            'wd': firstValue(d, 'wd'),
            'type': '养老机构',
        }
        for j in ['床位数', '占地面积', '建筑面积', '绿化面积', '联系电话', '邮编', '运营模式', '证照情况', '房屋权属证明', '有产证', '无产证']:
            _s.update({
                j: firstValue(d, j),
            })
        s.append(_s)
    return jsonStr(s)


# 某一养老机构入住人数
@app.route('/<name>/rzrs')
def rzrs(name):
    d = jgrzb[jgrzb['供应商名称'] == name]
    return jsonStr({
        'value': len(list(d['供应商名称']))
    })


# 框选养老机构中的建筑面积、绿化面积、占地面积
@app.route('/d2', methods=['POST'])
def d2():
    rFile = request.json
    lng1 = rFile['lng1']
    lat1 = rFile['lat1']
    lng2 = rFile['lng2']
    lat2 = rFile['lat2']
    d = jgxxb[jgxxb['jd'] >= min(lng1, lng2)]
    d = d[d['jd'] <= max(lng1, lng2)]
    d = d[d['wd'] >= min(lat1, lat2)]
    d = d[d['wd'] <= max(lat1, lat2)]
    s = []
    for i in list(d['供应商名称'].unique()):
        dd = d[d['供应商名称'] == i]
        for j in ratios:
            s.append({
                'name1': i,
                'name2': j,
                'value': firstValue(dd, j)
            })
    return jsonStr(s)


# 所有养老机构的入住流量热度变化
@app.route('/d3_1')
def d3_1():
    d = jgrzb[jgrzb['时间'] != '0']
    d = d.sort_values(by=['时间'])
    s = []
    for i in list(d['时间'].unique()):
        dd = d[d['时间'] == i]
        s.append({
            'name1': i,
            'value': len(list(dd['时间']))
        })
    return jsonStr(s)


# 所选时间段入住流量占比
@app.route('/<x>/d3_2')
def d3_2(x):
    d = jgrzb[jgrzb['时间'] == x]
    s = []
    for i in list(d['供应商名称'].unique()):
        dd = d[d['供应商名称'] == i]
        s.append({
            'name1': i,
            'value': len(list(dd['供应商名称']))
        })
    return jsonStr(s)


# 区域入住人数特征分布
@app.route('/d4', methods=['POST'])
def d4():
    rFile = request.json
    lng1 = rFile['lng1']
    lat1 = rFile['lat1']
    lng2 = rFile['lng2']
    lat2 = rFile['lat2']
    d = jgrzb[jgrzb['jd'] >= min(lng1, lng2)]
    d = d[d['jd'] <= max(lng1, lng2)]
    d = d[d['wd'] >= min(lat1, lat2)]
    d = d[d['wd'] <= max(lat1, lat2)]
    d = d.sort_values(by=['年龄等级'])
    s = []
    for i in list(d['年龄等级'].unique()):
        if int(i) != 0:
            dd = d[d['年龄等级'] == i]
            for j in list(dd['性别'].unique()):
                ddd = dd[dd['性别'] == j]
                s.append({
                    'name1': str(i),
                    'name2': str(j),
                    'value': len(list(ddd['性别']))
                })
    return jsonStr(s)


# 区域内机构入住人数分布
@app.route('/<x>/d5', methods=['POST'])
def d5(x):
    rFile = request.json
    lng1 = rFile['lng1']
    lat1 = rFile['lat1']
    lng2 = rFile['lng2']
    lat2 = rFile['lat2']
    d = jgrzb[jgrzb['jd'] >= min(lng1, lng2)]
    d = d[d['jd'] <= max(lng1, lng2)]
    d = d[d['wd'] >= min(lat1, lat2)]
    d = d[d['wd'] <= max(lat1, lat2)]
    d = d.sort_values(by=['等级'])
    s = []
    for i in list(d[x].unique()):
        dd = d[d[x] == i]
        for j in list(dd['供应商名称'].unique()):
            ddd = dd[dd['供应商名称'] == j]
            s.append({
                'name1': j,
                'name2': str(i),
                'value': len(list(ddd['供应商名称']))
            })
    return jsonStr(s)


# 某一个养老机构入住人数变化
@app.route('/<name>/d6')
def d6(name):
    d = jgrzb[jgrzb['供应商名称'] == name]
    d = d.sort_values(by=['时间'])
    s = []
    for i in list(d['时间'].unique()):
        if str(i) != '0':
            dd = d[d['时间'] == i]
            s.append({
                'name1': i,
                'value': len(list(dd['时间']))
            })
    return jsonStr(s)


# 某一机构的年龄男女占比
@app.route('/<name>/<x>/d7')
def d7(name, x):
    d = jgrzb[jgrzb['供应商名称'] == name]
    d = d.sort_values(by=['年龄等级'])
    s = []
    for i in list(d['年龄等级'].unique()):
        if int(i) != 0:
            dd = d[d['年龄等级'] == i]
            for j in list(dd[x].unique()):
                ddd = dd[dd[x] == j]
                s.append({
                    'name1': str(i),
                    'name2': str(j),
                    'value': len(list(ddd[x]))
                })
    return jsonStr(s)


# 某一机构近些年硬件设施变化情况
@app.route('/<name>/d8')
def d8(name):
    d = jgxxb[jgxxb['供应商名称'] == name]
    d = d.sort_values(by=['月份'])
    s = []
    for i in list(d['月份'].unique()):
        dd = d[d['月份'] == i]
        for j in ratios:
            s.append({
                'name1': str(i),
                'name2': j,
                'value': firstValue(dd, j)
            })
    return jsonStr(s)


@app.route('/recommend', methods=['POST'])
def recommend():
    rFile = request.json
    ratio1 = float(rFile['ratio1'] + '.0')
    ratio2 = rFile['ratio2']
    ratio3 = rFile['ratio3']
    ratio4 = rFile['ratio4']
    s = []
    d = jgrzb[jgrzb['年龄等级'] == ratio1]
    d = d[d['性别'] == int(ratio2)]
    d = d[d['老人类型'] == int(ratio3)]
    d = d[d['等级'] == int(ratio4)]
    for i in list(d['供应商名称'].unique()):
        dd = d[d['供应商名称'] == i]
        s.append({
            'name': i,
            'value': len(list(dd['供应商名称']))
        })
    d = pd.DataFrame(s)
    try:
        d = d.sort_values(by=['value'], ascending=False)
        return jsonStr({
            'names': list(d['name'])
        })
    except:
        return jsonStr({
            'names': list(jgxxb['供应商名称'])
        })


# app.run(host='192.168.137.176', port=5000)
app.run(host='127.0.0.1', port=5002)
