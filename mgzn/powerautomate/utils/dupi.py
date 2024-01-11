"""
本脚本用于处理爬取完毕的boss.CSV文件
主要功能是读取CSV文件
替换列名
去重
去空
然后将其保存为新的CSV文件，文件名包含当前的时间戳。
"""

# 导入所需的库
import pandas as pd
import numpy as np
import datetime
import os

# 定义一个函数，用于将DataFrame保存为CSV文件，文件名包含当前的时间戳
def save_df_to_csv(df, filename):
    # 获取当前时间戳
    now = datetime.datetime.now()
    timestamp = now.strftime("%m%d%H%M")

    # 将文件名加上时间戳
    filename = f"D:/AI/bossbase/{filename}_{timestamp}.csv"

    # 保存 df 到 CSV 文件
    df.to_csv(filename, index=False)

# 读取CSV文件
data = pd.read_csv("d:/AI/boss.csv")

# 重命名列名
data.columns = ["岗位名称", "区位", "薪资", "工作年限", "学历", "关键词", "公司名", "企业类别", "企业规模", "链接"]

columns_to_process = ["岗位名称", "区位", "薪资", "工作年限", "学历", "公司名", "关键词", "链接"]
data = data.drop_duplicates(subset=columns_to_process)

data = data.replace(to_replace="None", value=np.nan)
data.dropna(subset=["岗位名称", "区位", "薪资"], inplace=True)

data = data.reset_index(drop=True)

save_df_to_csv(data, "boss")
os.remove("d:/AI/boss.csv")
