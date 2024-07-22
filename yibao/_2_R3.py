from _2_L3 import *


@app.route('/r3_1', methods=['POST'])
def r3_1():
    rFile = request.json
    relationHeader = rFile['relationHeader']  # 需要研究的边的关系对象
    jzidL = rFile['jzidL']  # 就诊ID列表
    d = dataR3[['年龄', relationHeader, '就诊ID']]
    d = transHeaderType(d, '年龄', 'int32')
    d = drop(d, [relationHeader, '就诊ID'])
    d = d[d['就诊ID'].isin(jzidL)]
    """
    选取的群体内边关系对应数量
    """
    s = []
    for i in list(d[relationHeader].unique()):
        dd = d[d[relationHeader] == i]
        s.append({
            'name1': relationHeader,
            'name2': i,
            'value': returnValue(dd)
        })
    return jsonStr(s)


@app.route('/r3_2', methods=['POST'])
def r3_2():
    rFile = request.json
    relationHeader = rFile['relationHeader']  # 需要研究的边的关系对象
    relationValue = rFile['relationValue']  # 需要研究的边的关系的值
    ybjgmls = rFile['ybjgmls']  # 选中的医药目录名称列表
    d = dataR3[['年龄', relationHeader, '就诊ID', '医保目录名称', '明细项目费用总额', '单价']]
    d = drop(d, [relationHeader, '就诊ID', '医保目录名称'])
    d = d[d[relationHeader] == relationValue]
    jzidL = rFile['jzidL']  # 就诊ID列表
    d = d[d['就诊ID'].isin(jzidL)]
    """
    选取群体和边关系值中的医保目录名称个数分析
    """
    s = []
    L = list(d['医保目录名称'].unique())
    for i in range(len(L)):
        dd = d[d['医保目录名称'] == L[i]]
        s.append({
            'name1': str(L[i]),
            'name2': int(checkLInclude([L[i]], ybjgmls)),
            'value': math.ceil(sums(list(dd['明细项目费用总额'])) / firstValue(dd, '单价'))
        })
    return jsonStr(s)


@app.route('/r3_3', methods=['POST'])
def r3_3():
    rFile = request.json
    relationHeader = rFile['relationHeader']  # 需要研究的边的关系对象
    relationValue = rFile['relationValue']  # 需要研究的边的关系的值
    ybjgmls = rFile['ybjgmls']  # 选中的医药目录名称列表
    d = dataR3[['年龄', relationHeader, '就诊ID', '医保目录名称', '明细项目费用总额', '单价']]
    d = transHeaderType(d, '年龄', 'int32')
    d = drop(d, [relationHeader, '就诊ID', '医保目录名称'])
    d = d[d[relationHeader] == relationValue]
    jzidL = rFile['jzidL']  # 就诊ID列表
    d = d[d['就诊ID'].isin(jzidL)]
    """
    选取的某一群体边关系涉及到的用户的医保目录名称个数
    """
    s = []
    for i in list(d['就诊ID'].unique()):
        dd = d[d['就诊ID'] == i]
        for j in ybjgmls:
            ddd = dd[dd['医保目录名称'] == j]
            try:
                s.append({
                    'name1': i,
                    'name2': j,
                    'value': math.ceil(firstValue(ddd, '明细项目费用总额') / firstValue(ddd, '单价'))
                })
            except:
                continue
    return jsonStr(s)


@app.route('/r3_4', methods=['POST'])
def r3_4():
    rFile = request.json
    yljgml = rFile['yljgml']  # 选中的医药目录名称列表
    d = dataR3[['年龄', '就诊ID', '医保目录名称', '明细项目费用总额', '符合范围金额']]
    d = transHeaderType(d, '年龄', 'int32')
    d = d[d['医保目录名称'] == yljgml]
    d = drop(d, ['就诊ID', '医保目录名称', '明细项目费用总额', '符合范围金额'])
    jzidL = rFile['jzidL']  # 就诊ID列表
    d = d[d['就诊ID'].isin(jzidL)]
    """
    选取的医保目录名称涉及到的人员的符合范围金额和费用总额对比
    """
    s = []
    for i in list(d['就诊ID'].unique()):
        dd = d[d['就诊ID'] == i]
        s.append({
            'name1': i,
            'name2': '明细项目费用总额',
            'value': firstValue(dd, '明细项目费用总额')
        })
        s.append({
            'name1': i,
            'name2': '实际支付费用',  # 这里是有点东西的，二次计算实际费用
            'value': round(firstValue(dd, '明细项目费用总额') - firstValue(dd, '符合范围金额'), 2)
        })
    return jsonStr(s)



# app.run(host='192.168.30.160', port=5001)