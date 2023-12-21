import pandas as pd
import re
import chardet

# 地区格式: 北京·昌平区·回龙观-->北京-昌平
def clean_location(location):
    if len(location.split('·'))>=2:
        location = location.split('·')[0] + '-' + location.split('·')[1]
        location = location.replace('区', '')
    elif len(location.split('-'))>=2:
        location = location.replace('区', '')
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
    # Check if the date string contains "今天"
    if '今天' in date_str:
        # Replace "今天" with the current date
        date_str = date_str.replace('今天', pd.to_datetime('today').strftime('%m月%d日'))

    # Extract the month and day from the string using regular expression
    match = re.search(r'(\d+)月(\d+)日', date_str)

    if match:
        month, day = map(int, match.groups())

        # Assume the year is the current year (you can replace this with a specific year if needed)
        current_year = pd.to_datetime('today').year

        # Format the date as "更新于：年-月-日"
        formatted_date = f"{current_year}-{month:02d}-{day:02d}"
        return formatted_date
    else:
        updated_date_str = date_str.replace("更新于：", "")
        return updated_date_str

# 工作年限统一：1年以内、一年以下-->1年以下
def clean_experience(experience):
    if '以内' in experience or '以下' in experience:
        return '1年以下'
    elif '无经验' in experience:
        return '经验不限'
    elif '应届生' in experience:
        return '应届生'
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
    """
    因为企业规模中有空值nan，nan属于浮点数，所以会出现这样的情况（对浮点数执行不可迭代的 in 操作）
    建议把nan直接换成字段“无”，方便后续处理
    """
    if isinstance(size, str) and '20人以下' in size:
        return '0-20人'
    else:
        return size

csv_file_path = '招聘数据处理\\boss_招聘信息.csv'
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
# 新增“来源”列并填充数据
df['来源'] = 'boss直聘'

# 保存修改后的文件
df.to_csv('cleaned_boss.csv', index=False, encoding='utf-8')
