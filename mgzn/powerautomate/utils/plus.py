import pandas as pd
import datetime
import os
import glob

def save_df_to_csv(df, filename):
    # 获取当前时间戳
    now = datetime.datetime.now()
    timestamp = now.strftime("%m%d%H%M")

    # 将文件名加上时间戳
    filename = f"D:\AI\AI-job-analysis\mgzn\{filename}_{timestamp}.csv"

    # 保存 df 到 CSV 文件
    df.to_csv(filename, index=False)

base_path = "d:\\AI\\bossbase" 

# 获取文件夹中所有的 CSV 文件
csv_base = glob.glob(os.path.join(base_path, 'boss_*.csv'))
latest_base = max(csv_base, key=os.path.getctime)

data = pd.read_csv(latest_base)
info = pd.read_csv("d:\AI\info.csv")
info.columns = ["岗位要求", "更新时间"]
# 合并两列
result = pd.concat([data, info], axis=1)
result.drop(['链接'], axis=1, inplace=True)
save_df_to_csv(result, "boin")
os.remove('d:/AI/info.csv')