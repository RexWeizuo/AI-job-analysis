import glob
import pandas as pd

def merge_csv(filenames):
    """Merge CSV files."""
    frames = [pd.read_csv(filename, encoding='utf-8') for filename in filenames]
    merged_data = pd.concat(frames, ignore_index=True)
    # # 删除 '关键词1'、'关键词2'、'关键词3' 列
    # merged_data = merged_data.drop(['关键词1', '关键词2', '关键词3'], axis=1)
    return merged_data

if __name__ == '__main__':
    # Example filenames, replace with your actual file paths
    filenames = ['data_merge\\merged_data_1226.csv', 'data_merge\\merged_data_1227.csv','data_merge\\merged_data_1228.csv','data_merge\\merged_data_1230.csv']

    # Merge data
    merged_data = merge_csv(filenames)

    # 总共合并的数据项
    print(f'Total merged data: {len(merged_data)} rows')
    
    # Assuming you want to drop duplicates based on all columns
    merged_data_no_duplicates = merged_data.drop_duplicates()

    # 删除数据后的数据总和
    print(f'Total data after removing duplicates: {len(merged_data_no_duplicates)} rows')

    # Save merged and deduplicated data to a new CSV file
    merged_data_no_duplicates.to_csv('merged_data_all.csv', index=False, encoding='utf-8')