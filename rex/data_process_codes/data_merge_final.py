import pandas as pd

# 读取包含12列数据的 CSV 文件
df = pd.read_csv('merged_data_all.csv')

# 打印删除前的数据项总数
print(f'删除前的数据项总数: {len(df)}')

# 删除前10列重复的数据项
df_no_duplicates = df.drop_duplicates(subset=df.columns[:10])

# 打印删除后的数据项总数
print(f'删除后的数据项总数: {len(df_no_duplicates)}')

# 保存删除重复项后的数据到新的 CSV 文件
df_no_duplicates.to_csv('merged_data_final.csv', index=False)

