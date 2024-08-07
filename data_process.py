import pandas as pd
from datetime import datetime

# 读取 Excel 文件
excel_file_path = './数据整合2.xlsx'
excel_df = pd.read_excel(excel_file_path)

# 文件名列表
file_names = [
    "weather_20220818_20220914.csv",
    "weather_20220915_20221010.csv",
    "weather_20221011_20221107.csv",
    "weather_20221108_20221201.csv",
    "weather_20221202_20221229.csv",
    "weather_20221230_20230120.csv",
    "weather_20230121_20230215.csv",
    "weather_20230216_20230310.csv",
    "weather_20230311_20230407.csv"
]

def is_within_date_range(date_obj, start_date, end_date):
    """检查日期是否在范围内"""
    return start_date <= date_obj <= end_date

def find_matching_file(date_obj, file_names):
    """根据日期找到匹配的文件"""
    for file_name in file_names:
        start_date_str, end_date_str = file_name.split('_')[1], file_name.split('_')[2].split('.')[0]
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
        if is_within_date_range(date_obj, start_date, end_date):
            return file_name
    return None

def extract_date(date_str):
    """从日期字符串中提取年月日"""
    date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
    return date_obj.strftime("%Y%m%d")

def getweatherdata(df, date, place):
    """根据日期和城市过滤气象数据"""
    date = datetime.strptime(date, "%Y%m%d")  # 转换日期为 datetime 对象
    df['stat_date'] = pd.to_datetime(df['stat_date'], format="%Y%m%d")  # 确保 'stat_date' 列为 datetime 对象
    filtered_df = df[(df['city'] == place) & (df['stat_date'] == date)]
    return filtered_df if not filtered_df.empty else None

cont = 1
# 循环处理每一行数据
for index, row in excel_df.iterrows():
    date = extract_date(str(row['提交答卷时间']))
    place = row['请选择省份城市与地区:'].split('-')[1]
    cont += 1
    print(cont)
    # 找到匹配的文件
    date_obj = datetime.strptime(date, "%Y%m%d")
    matching_file = find_matching_file(date_obj, file_names)

    if matching_file is not None:
        # 读取气象数据文件
        weather_df = pd.read_csv(f"./weatherdata/{matching_file}", encoding='GB2312')

        # 找到那一天和那个城市的气象数据
        filtered_data = getweatherdata(weather_df, date, place)
        if filtered_data is not None:
            # 添加气象数据到 Excel DataFrame
            excel_df = pd.concat([excel_df, filtered_data], ignore_index=True)

# 保存更新后的 Excel 文件
updated_excel_file_path = './updated_file1.xlsx'
excel_df.to_excel(updated_excel_file_path, index=False)
print(f"更新后的 Excel 文件已保存到: {updated_excel_file_path}")
