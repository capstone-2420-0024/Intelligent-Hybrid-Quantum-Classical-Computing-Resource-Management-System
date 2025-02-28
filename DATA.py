import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def data_vis(df):
    df['datetime'] = pd.to_datetime(df['datetime'])  # transform the time format
    df = df.sort_values("datetime")  # rank according to the time series

    # load all the sensor channels
    channels = df['channel'].unique()

    # set the font size
    plt.rcParams.update({'font.size': 5})  

    # set the figure size
    fig, axes = plt.subplots(nrows=len(channels), ncols=1, figsize=(6, len(channels) * 1.5), sharex=True)

    if len(channels) == 1:
        axes = [axes]

    # Traverse each channel, drawing the separate subgraph
    for i, channel in enumerate(channels):
        sub_df = df[df['channel'] == channel]  # select the data for a specific channel
        axes[i].plot(sub_df['datetime'], sub_df['value'], label=f"Channel {channel}", color='b')

        # set time format
        axes[i].xaxis.set_major_locator(mdates.HourLocator(interval=12)) # every 12hs
        axes[i].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))  # time format

        # Get all scales for the current X-axis
        tick_labels = [label.get_text() for label in axes[i].get_xticklabels()]
    
        # Keep only part of the label, 1 out of every 4 labels
        for j, label in enumerate(axes[i].get_xticklabels()):
            if j % 4 != 0: 
                label.set_visible(False)

        axes[i].set_ylabel("Value")
        axes[i].set_title(f"Time Series for Channel {channel}")
        axes[i].legend()
        axes[i].grid(True)

    # Format the X-axis
    plt.xlabel("Time")
    plt.xticks(rotation=15)  # Rotate the X-axis scale to prevent overlap
    plt.tight_layout()
    plt.show()


from data_visualization import data_vis
import pandas as pd

df = pd.read_csv("databases/data_csv/cd230831/maxigauge.csv")  # or maxigauge.csv / cooling.csv
data_vis(df)