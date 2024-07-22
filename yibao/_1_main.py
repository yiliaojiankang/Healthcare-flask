from _0_base import *

dataUrl = './data/'  # 工作文件
rowDataUrl = './rowData/'  # 原始数据路径
tempDataUrl = './tempData/' # 临时数据路径

def main():
    def main1():
        """
        1. 人员信息特征数据
        """
        data1 = readCsv(rowDataUrl + '住院明细.csv')
        headers1 = ['就诊ID', '定点医药机构编号', '参保所属医保区划', '支付地点类别', '创建人ID', '经办人ID']
        data1 = data1[headers1]
        data1 = drop(data1, ['就诊ID'])
        data1 = data1.sort_values(by=['就诊ID']).reset_index(drop=True)
        data2 = readCsv(rowDataUrl + '住院流水.csv')
        headers2 = ['就诊ID', '人员证件类型', '性别', '民族', '年龄', '人员类别', '公务员标志',
                    '灵活就业标志', '单位类型', '经济类型', '账户使用标志']
        data2 = data2[headers2]
        data2 = drop(data2, ['就诊ID'])
        data2 = data2.sort_values(by=['就诊ID']).sort_values(by=['就诊ID'])
        data = mergeLR(data1, data2, ['就诊ID'])
        data.to_csv(dataUrl + 'data1.csv', index=False)

    # main1()

    def main2():
        """
        :return: 行为特征序列提取
        """
        data1 = readCsv(rowDataUrl + '住院流水.csv')
        data1 = data1[['就诊ID', '医疗费总额',
                       '全自费金额', '超限价自费费用', '符合范围金额', '先行自付金额',
                       '清算方式', '个人结算方式', '清算类别'
                       ]]
        data1.loc[:, '全自费占比'] = round(
            data1['全自费金额'] / data1['医疗费总额'],
            2
        )
        data1.loc[:, '超限价自费占比'] = round(
            data1['超限价自费费用'] / data1['医疗费总额'],
            2
        )
        data1.loc[:, '符合范围占比'] = round(
            data1['符合范围金额'] / data1['医疗费总额'],
            2
        )
        data1.loc[:, '先行自付占比'] = round(
            data1['先行自付金额'] / data1['医疗费总额'],
            2
        )
        data1 = quality(data1, '清算方式')
        data1 = quality(data1, '个人结算方式')
        data1 = quality(data1, '清算类别')
        data1.to_csv(dataUrl + 'data2.csv', index=False)

    # main2()


main()