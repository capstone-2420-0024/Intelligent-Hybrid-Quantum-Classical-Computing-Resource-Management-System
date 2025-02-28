import pandas as pd
import numpy as np

# 1️⃣ 读取数据
file_path = "databases/data_csv/cd230831/cooling.csv"
df = pd.read_csv(file_path)

if "io" in df.columns:

    # 1️⃣ 确保 datetime 是正确格式
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S.%f") 

    # 2️⃣ 更新 channel 的值
    df["channel"] = df.apply(lambda row: 0 if (row["channel"] == 0 and row["io"] == 0) else
                                        1 if (row["channel"] == 0 and row["io"] == 1) else
                                    10 if (row["channel"] == 1 and row["io"] == 0) else
                                    11, axis=1)

    # 3️⃣ 只保留所需的列
    df = df[["datetime", "channel", "value"]]

df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S.%f") # 确保 datetime 格式正确
df = df.set_index("datetime")  # 设置 datetime 为索引

# 确保 datetime 是索引
df.index = pd.to_datetime(df.index)  # 确保索引是 datetime 类型


# 1️⃣ 使用 pivot_table 将 channel 作为列
df_pivot = df.pivot_table(index="datetime", columns="channel", values="value")

# 2️⃣ 重命名列名为 "channel1", "channel2" 等
df_pivot.columns = [f"channel{int(col)}" for col in df_pivot.columns]

# 1️⃣ 读取数据
df_pivot.index = pd.to_datetime(df_pivot.index)  # 确保索引是 datetime 类型

# 2️⃣ 获取起点时间
start_time = df.index.min().floor("30S")  # 向下取整到最接近的 00 或 30 秒
end_time = df.index.max().ceil("30S")  # 向上取整到最近的 00 或 30 秒

# 3️⃣ 生成新的时间序列，每 30 秒一个点
new_time_stamps = [start_time]  # 存储新时间戳
while new_time_stamps[-1] + pd.Timedelta(seconds=30) <= end_time:
    new_time_stamps.append(new_time_stamps[-1] + pd.Timedelta(seconds=30))

# 4️⃣ 创建新 DataFrame，并进行插值
new_df = pd.DataFrame({"datetime": new_time_stamps})  # 生成 DataFrame

# 5️⃣ 对每个 channel 进行插值
for col in df_pivot.columns:
    new_df[col] = np.interp(
        new_df["datetime"].astype(int),  # 新时间序列的数值表示
        df_pivot.index.astype(int),  # 原始时间的数值表示
        df_pivot[col]  # 原始值
    )

# 6️⃣ 设置索引
new_df.set_index("datetime", inplace=True)

print(new_df.head)
