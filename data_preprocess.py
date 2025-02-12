import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import StandardScaler

#  1. 读取数据 
# 请替换文件路径
temperature_file = r".\databases\cd230831\temperature.csv"
cooling_file = r".\databases\cd230831\cooling.csv"
maxigauge_file = r".\databases\cd230831\maxigauge.csv"

dfs = {
    "temperature": pd.read_csv(temperature_file),
    "cooling": pd.read_csv(cooling_file),
    "maxigauge": pd.read_csv(maxigauge_file)
}

# 解析时间列
for name, df in dfs.items():
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.sort_values("datetime", inplace=True)  # 按时间排序

# 2. 异常值检测 (IQR) 
def remove_outliers_iqr(df, column):
    """ 使用IQR方法去除异常值 """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df_filtered

for name, df in dfs.items():
    dfs[name] = remove_outliers_iqr(df, "value")

# 3. 移动平均滤波 
def moving_average_fixed(df, column, window_size=10):
    """ 应用移动平均滤波并填充缺失值 """
    df[column] = df[column].rolling(window=window_size, min_periods=1).mean()
    return df

for name, df in dfs.items():
    dfs[name] = moving_average_fixed(df, "value", window_size=10)

# 4. 低通滤波 
def low_pass_filter(values, cutoff=0.001, fs=1/60, order=6):
    """ 应用低通滤波器 """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, values)

for name, df in dfs.items():
    df['value'] = low_pass_filter(df['value'].values)

# 5. 数据标准化 
#scaler = StandardScaler()
#for name, df in dfs.items():
#    df['value'] = scaler.fit_transform(df[['value']])

# 6. 时间对齐 (重采样)
#resample_interval = '10S'  # 统一时间间隔

#for name, df in dfs.items():
#    df.set_index("datetime", inplace=True)  # 设定时间戳为索引
#    df = df.resample(resample_interval).mean()  # 取均值重采样
#    df.reset_index(inplace=True)  # 重新恢复索引
#    dfs[name] = df

# 7. 保存处理后数据到指定的路径 

output_path = r".\databases\cd230831"  # 目标存储路径

for name, df in dfs.items():
    df.to_csv(f"{output_path}\{name}_processed.csv", index=False)


# 8️.可视化数据
def visualize_data(df, title):
    """ 绘制原始 vs 处理后数据、分布图 """
    plt.figure(figsize=(12, 6))
    
    # 绘制数据趋势
    plt.subplot(2, 2, 1)
    plt.plot(df["datetime"], df["value"], label="Processed Data", color="blue")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(f"{title} - Time Series")
    plt.legend()

    # 绘制直方图
    plt.subplot(2, 2, 2)
    sns.histplot(df["value"], bins=30, kde=True, color="purple")
    plt.title(f"{title} - Histogram")

    # 绘制箱线图 (查看异常值)
    plt.subplot(2, 2, 3)
    sns.boxplot(y=df["value"], color="orange")
    plt.title(f"{title} - Box Plot")

    plt.tight_layout()
    plt.show()

# 可视化所有数据集
for name, df in dfs.items():
    visualize_data(df, name)
