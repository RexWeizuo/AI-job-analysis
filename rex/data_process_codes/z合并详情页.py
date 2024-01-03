from bs4 import BeautifulSoup
import pandas as pd

# 读取第一个CSV文件
df1 = pd.read_csv('大致页数据1228.csv')
# # 加上列名
# df1.columns = ['岗位名称', '区位', '薪资', '工作年限', '学历', '关键词1', '关键词2', '关键词3', '链接']

# 定义一个函数来解析 HTML 数据并提取文本
def parse_html(html):
    if pd.notna(html) and isinstance(html, str):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='iteminfo__line3__welfare__item')
        return [item.get_text() for item in items]
    else:
        return []

# 将 HTML 数据的第六列应用解析函数并覆盖原始数据
df1.iloc[:, 5] = df1.iloc[:, 5].apply(parse_html)

# 丢弃原始的'链接'列
# 删除最后一列
df1 = df1.drop(df1.columns[-1], axis=1)


# 读取第二个CSV文件
df2 = pd.read_csv('详情页数据1228.csv')
# # 加上列名
# df2.columns = ['公司名', '企业类别', '企业规模', '岗位要求', '更新时间']

# 保存合并后的数据框
merged_df = pd.concat([df1, df2], axis=1)

# 保存合并后的文件
merged_df.to_csv('智联1228.csv', index=False)