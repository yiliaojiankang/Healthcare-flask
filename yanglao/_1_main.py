from _0_base import *

# jwdInsert(readCsv(dataUrl + '养老机构信息表.csv'), '供应商名称').to_csv(
#     dataUrl + '养老机构信息表.csv', index=False
# )
#
#
# jwdInsert(readCsv(dataUrl + '养老机构设置医疗机构.csv'), '机构名称').to_csv(
#     dataUrl + '养老机构设置医疗机构.csv', index=False
# )


# jwdInsert(readCsv(dataUrl + '静安区独居养老服务.csv'), '安装地址（去掉室号）', '上海市').to_csv(
#     dataUrl + '静安区独居养老服务.csv', index=False
# )



jgxxb = readCsv(dataUrl + '养老机构信息表.csv')
jgrzb = readCsv(dataUrl + '养老机构入住表.csv')
# jgrzb = dropSpace(jgrzb, '供应商名称')
# jgrzb = splitHeader(jgrzb, '入院时间', ' ')
# jgrzb = modify(jgrzb, 0, '时间')
# jwd = jgxxb[['供应商名称', 'jd', 'wd']]
# ddddd = mergeLR(jgrzb, jwd, ['供应商名称'])
# drop(ddddd, '主键ID').to_csv(dataUrl + '养老机构入住表.csv', index=False)
yljgb = readCsv(dataUrl + '养老机构设置医疗机构.csv')
ylfw = readCsv(dataUrl + '静安区独居养老服务.csv')
ratios = ['床位数', '占地面积', '建筑面积', '绿化面积']
