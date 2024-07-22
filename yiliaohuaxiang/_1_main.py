from _0_base import *


def main():
    """
    :return:
    """
    """
    1. 提取主要病症
    """
    # data = readCsv(rowDataUrl + "患者门诊诊断表.csv")
    # data = data[data['诊断标识'] == '主诊断']
    # data = drop(data, ['就诊编码', '诊断名称'])
    # s = []
    # for i in list(data['诊断名称'].unique()):
    #     dd = data[data['诊断名称'] == i]
    #     s.append({
    #         '诊断名称': i,
    #         'value': returnValue(dd)
    #     })
    # data = pd.DataFrame(s)
    # data = data.sort_values(by=['value'], ascending=False)
    # names = list(data['诊断名称'])
    # values = list(data['value'])
    # Len = sums(values)
    # Cnt = 0
    # s = []
    # for i in range(len(names)):
    #     Cnt += values[i]
    #     s.append({
    #         '诊断名称': names[i],
    #         '患病人数': values[i]
    #     })
    #     if Cnt / Len > 0.99 or values[i] < 50:
    #         break
    # data = pd.DataFrame(s)
    # data.to_csv(dataUrl + '主要诊断名称.csv', index=False)

    """
    2. 筛选非主要诊断名称的就诊编码
    """
    # zdmcData = readCsv(dataUrl + '主要诊断名称.csv')
    # data = readCsv(rowDataUrl + '患者门诊诊断表.csv')
    # data = data[data['诊断标识'] == '主诊断']
    # data = drop(data, ['就诊编码', '诊断名称'])
    # names = list(zdmcData['诊断名称'])
    # data = data[data['诊断名称'].isin(names)]
    # data = drop(data, ['就诊编码'])
    # data[['就诊编码']].to_csv(dataUrl + '主要就诊编码.csv', index=False)

    """
    3. 主要患者编码
    """
    # data = readCsv(rowDataUrl + '患者就诊表.csv')
    # jzbm = readCsv(dataUrl + '主要就诊编码.csv')
    # names = list(jzbm['就诊编码'])
    # data = data[data['就诊编码'].isin(names)]
    # data = drop(data, ['患者编码'])
    # data[['患者编码', '就诊编码']].to_csv(dataUrl + '主要患者编码.csv', index=False)

    """
    4. 主要患者信息
    """
    # data = readCsv(rowDataUrl + '患者信息表.csv')
    # hzbm = readCsv(dataUrl + '主要患者编码.csv')
    # names = list(hzbm['患者编码'])
    # data = data[data['患者编码'].isin(names)]
    # data = drop(data, ['患者编码'])
    # data = mergeLR(data, hzbm, ['患者编码'])
    # data.to_csv(dataUrl + '主要患者.csv', index=False)

    """
    5. 主要患者信息序列
    """
    # zdmcData = readCsv(rowDataUrl + '患者门诊诊断表.csv')
    # zdmcData = zdmcData[zdmcData['诊断标识'] == '主诊断']
    # data = readCsv(dataUrl + "主要患者.csv")
    # names = list(data['就诊编码'])
    # zdmcData = zdmcData[zdmcData['就诊编码'].isin(names)]
    # data = mergeLR(data, zdmcData, ['就诊编码'])
    # data = data[['患者编码', '就诊编码', '性别', '年龄', '诊断名称', '器官名称']]
    # data.to_csv(dataUrl + '主要患者.csv', index=False)

    """
    6. 将患者分类数据进行进一步过滤
    """
    # data = readCsv(rowDataUrl + '包含坐标的患者信息.csv')
    # for csvName in csvLists(dataUrl):
    #     dd = readCsv(dataUrl + csvName)
    #     if '诊断' in csvName:
    #         names = list(data['诊断名称'])
    #         dd = dd[dd['诊断名称'].isin(names)]
    #         dd.to_csv(dataUrl + csvName, index=False)
    #     elif '患者' in csvName:
    #         names = list(data['患者编码'])
    #         dd = dd[dd['患者编码'].isin(names)]
    #         dd.to_csv(dataUrl + csvName, index=False)
    #     elif '就诊' in csvName:
    #         names = list(data['就诊编码'])
    #         dd = dd[dd['就诊编码'].isin(names)]
    #         dd.to_csv(dataUrl + csvName, index=False)

    """
    7. 主要研究患者群体中的主要诊断名称、器官以及院区
    """
    # jzbm = readCsv(rowDataUrl + '包含坐标的患者信息.csv')
    # names = list(jzbm['就诊编码'])
    # data = readCsv(rowDataUrl + '病案首页表.csv')
    # data = data[['就诊编码', '住院次数', '出院病区', '入院月', '入院日']]
    # data = data[data['就诊编码'].isin(names)]
    # data = mergeLR(jzbm, data, ['就诊编码'])
    # data.to_csv(dataUrl + '病案首页表1.csv', index=False)

    """
    8. 包含信息的病案首页表
    """
    # data1 = readCsv(rowDataUrl + '患者就诊表.csv')[['患者编码', '就诊编码']]
    # data2 = readCsv(rowDataUrl + '患者信息表.csv')
    # data3 = readCsv(rowDataUrl + '病案首页表.csv')
    # data = mergeLR(data1, data2, ['患者编码'])
    # data = mergeLR(data, data3, ['就诊编码'])
    # data.to_csv(dataUrl + "病案首页表2.csv", index=False)




main()
