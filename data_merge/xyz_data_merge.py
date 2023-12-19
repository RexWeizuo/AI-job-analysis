import pandas as pd
import re
import chardet

# 地区格式: 北京·昌平区·回龙观-->北京-昌平
def clean_location(location):
    location = location.split('·')[0]
    location = location.replace('·', '-')
    location = location.replace('区', '')
    """
    第一行是把输入的文本按照'·'分开，分开之后会变成['北京','昌平区','回龙观']，取索引为0的数，也就成了'北京'
    也就是说，到第二、第三行的时候，传入的数据里已经没有'·'，也没有'区'字
    """
    return location

# 薪资格式：50-80K·13薪（“薪资面议”，“面议”-->“薪资面议”）（保留“急聘”）
def convert_salary(salary):
    if '面议' in salary:
        return '薪资面议'
    elif '急聘' in salary:
        return '急聘'

    # Mapping for special cases
    special_cases = {
        '元/周': '元/周',
        '元/时': '元/时',
        '/天': '元/天',
    }

    for key, value in special_cases.items():
        if key in salary:
            salary = salary.replace(key, value)

    parts = salary.split('·')
    base_salary = parts[0].replace('K', '')
    multiplier = ''

    if len(parts) > 1:
        multiplier = '·' + parts[1]

    if '元/月' in salary:
        try:
            min_salary, max_salary = map(lambda x: int(int(x.replace('元/月', ''))/1000) if '元/月' in x else int(int(x)/1000), base_salary.split('-'))
            return f"{min_salary}k-{max_salary}k{multiplier}"
        except ValueError:
            return salary
    else:
        try:
            min_salary, max_salary = map(lambda x: int(x.replace('万', '')) * 10 if '万' in x else int(x), base_salary.split('-'))
            return f"{min_salary}k-{max_salary}k{multiplier}"
        except ValueError:
            # 处理 '2万-4万' 这样的情况
            if '万' in base_salary:
                min_salary, max_salary = map(lambda x: int(float(x) * 1000), base_salary.split('-'))
                return f"{min_salary}k-{max_salary}k"
            else:
                return salary
    
# 更新时间格式：year-month-day(xxxx-xx-xx)
def convert_update_date(date_str):
    if '今天' in date_str:
        date_str = date_str.replace('今天', pd.to_datetime('today').strftime('%m月%d日'))

    match = re.search(r'(\d+)月(\d+)日', date_str)
    if match:
        month, day = map(int, match.groups())
        current_year = pd.to_datetime('today').year
        formatted_date = f"{current_year}-{month:02d}-{day:02d}"
        return formatted_date
        """
        看起来只去掉了月日情况下的“更新于”，原本就是--格式的字段仍旧会保留“更新于”，最好统一一下，全都不保留
        """
    else:
        return date_str

# 工作年限统一：1年以内、一年以下-->1年以下
def clean_experience(experience):
    if '以内' in experience or '以下' in experience:
        return '1年以下'
    elif '无经验' in experience or '应届生' in experience:
        """
        应届生单独拿出来，因为应届生是一个硬性条件（非应届生不能报应届生岗，所以应届生不属于经验不限）
        """
        return '经验不限'
    else:
        return experience

# 学历统一：统招本科 --> 本科
def clean_education(education):
    if '统招本科' in education:
        return '本科'
    else:
        return education

# 文件编码格式统一：utf-8
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding'].lower()
    if encoding == 'gb2312':
        encoding = 'gb18030'  # Use 'gb18030' instead of 'gb2312'
    return encoding

# 企业规模统一：20人以下 --> 0-20人
def clean_company_size(size):
    # 只有在 size 是字符串时才执行包含 '20人以下' 的检查。这样可以避免对浮点数执行不可迭代的 in 操作。
    if isinstance(size, str) and '20人以下' in size:
        return '0-20人'
    else:
        return size

csv_file_path = 'boss_招聘信息.csv'
# 检测文件编码
file_encoding = detect_encoding(csv_file_path)
# 输出检测到的编码
print(f"Detected encoding: {file_encoding}")
# 读取CSV文件
df = pd.read_csv(csv_file_path, encoding=file_encoding)

# 检查数据有几列
print(f"Number of columns in the DataFrame: {df.shape[1]}")

# 添加列名
df.columns = ['岗位名称', '区位', '薪资', '工作年限', '学历', '关键词1', '关键词2', '关键词3', '公司名', '企业类别', '企业规模', '岗位要求', '更新时间']

# 统一处理列格式
df['区位'] = df['区位'].apply(clean_location)
df['薪资'] = df['薪资'].apply(convert_salary)
df['更新时间'] = df['更新时间'].apply(convert_update_date)
df['工作年限'] = df['工作年限'].apply(clean_experience)
df['学历'] = df['学历'].apply(clean_education)
df['企业规模'] = df['企业规模'].apply(clean_company_size)

# 保存修改后的文件
df.to_csv('cleaned_boss.csv', index=False, encoding='utf-8')
