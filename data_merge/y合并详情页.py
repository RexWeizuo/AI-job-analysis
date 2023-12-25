import pandas as pd
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding'].lower()
    if encoding == 'gb2312':
        encoding = 'gb18030'  # Use 'gb18030' instead of 'gb2312'
    return encoding

# 检测文件编码
file_encoding = detect_encoding('A20231224.csv')
# 输出检测到的编码
print(f"Detected encoding: {file_encoding}")
# 读取CSV文件
df1 = pd.read_csv('A20231224.csv', encoding=file_encoding)
# # 读取第一个CSV文件
# df1 = pd.read_csv('A20231224.csv', encoding='utf-8')
# 删除最后一列
df1 = df1.iloc[:, :-1]

# 检测文件编码
file_encoding = detect_encoding('B20231224.csv')
# 输出检测到的编码
print(f"Detected encoding: {file_encoding}")
# 读取CSV文件
df2 = pd.read_csv('B20231224.csv', encoding=file_encoding)
# # 读取第二个CSV文件
# df2 = pd.read_csv('B20231224.csv', encoding='utf-8')
# # 删除第一列
# df2 = df2.iloc[:, 1:]

# 保存合并后的数据框
merged_df = pd.concat([df1, df2], axis=1)

# 添加列名
merged_df.columns = ['岗位名称', '区位', '薪资', '工作年限', '学历', '公司名', '企业类别', '融资情况', '企业规模', '关键词', '岗位要求']

# 将 '融资情况' 列中的 NaN 值替换为 '无'
merged_df['融资情况'] = merged_df.apply(lambda row: '无' if pd.isna(row['融资情况']) else row['融资情况'], axis=1)
# 将 '融资情况' 列中不包含关键字 "人" 的数据项替换为空值
merged_df['融资情况'] = merged_df.apply(lambda row: '' if '人' not in row['融资情况'] else row['融资情况'], axis=1)
# 合并 '融资情况' 和 '企业规模'（第九）列
merged_df['融资情况_企业规模'] = merged_df['融资情况'].fillna('') + ' ' + merged_df['企业规模'].fillna('')

# 删除原始的 '融资情况' 和 '企业规模' 列
merged_df = merged_df.drop(['融资情况', '企业规模'], axis=1)

# 交换 '融资情况_企业规模' 和 '岗位要求' 列
merged_df = merged_df[['岗位名称', '区位', '薪资', '工作年限', '学历', '关键词', '公司名', '企业类别', '融资情况_企业规模', '岗位要求']]

# 更新列名
merged_df.columns = ['岗位名称', '区位', '薪资', '工作年限', '学历', '关键词', '公司名', '企业类别', '企业规模', '岗位要求']

# 加上更新时间列，统一填写20231220
merged_df['更新时间'] = '2023-12-24'

# 保存合并后的文件
merged_df.to_csv('猎聘_20231224.csv', index=False, encoding='utf-8')
