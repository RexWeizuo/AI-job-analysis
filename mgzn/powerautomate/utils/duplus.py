# 导入所需的库
import pandas as pd
import os
import glob
import numpy as np

# 定义基础路径和新数据路径
base_path = "D:/AI/AI-job-analysis/mgzn/"
new_data_path = glob.glob(os.path.join(base_path, "boin_*.csv"))

# 获取最新的CSV文件
latest = max(new_data_path, key=os.path.getctime)

# 读取基础CSV文件和最新的CSV文件
data = pd.read_csv("d:/AI/bossbase/boin.csv")
new_data = pd.read_csv(latest)

# 合并两个数据集
result = pd.concat([data, new_data])

# 定义需要处理的列
columns_to_process = ["岗位名称", "区位", "薪资", "工作年限", "学历", "公司名", "关键词", "更新时间"]

# 删除这些列中的重复行
result = result.drop_duplicates(subset=columns_to_process)

# 将'data'数据集中的'None'值替换为numpy的nan
data = data.replace(to_replace="None", value=np.nan)

# 删除'岗位要求'列中包含nan的行
data.dropna(subset=["岗位要求"], inplace=True)

# 重置结果数据集的索引
result = result.reset_index(drop=True)

# 将结果数据集保存为CSV文件
result.to_csv("d:/AI/bossbase/boin.csv", index=False)

# 删除原始的CSV文件（此行代码已被注释掉）
# os.remove('d:/AI/boss.csv')
