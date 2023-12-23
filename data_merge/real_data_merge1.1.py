import glob
import pandas as pd

def merge_csv(filenames):
    """Merge CSV files."""
    frames = [pd.read_csv(filename, encoding='utf-8') for filename in filenames]
    merged_data = pd.concat(frames, ignore_index=True)
    return merged_data

if __name__ == '__main__':
    # Example filenames, replace with your actual file paths
    filenames = ['cleaned_boss.csv', 'cleaned_猎聘.csv', 'unified_智联.csv']

    # Merge data
    merged_data = merge_csv(filenames)

    # 总共合并的数据项
    print(f'Total merged data: {len(merged_data)} rows')
    
    # Assuming you want to drop duplicates based on all columns
    merged_data_no_duplicates = merged_data.drop_duplicates()

    # 删除数据后的数据总和
    print(f'Total data after removing duplicates: {len(merged_data_no_duplicates)} rows')

    # Save merged and deduplicated data to a new CSV file
    merged_data_no_duplicates.to_csv('merged_data_1222.csv', index=False, encoding='utf-8')