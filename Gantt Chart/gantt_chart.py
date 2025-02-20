import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Define updated project tasks and timelines based on the new provided image
tasks = [
    ("Data Understanding and Preprocessing", "2025-02-02", "2025-02-15"),
    ("Data Storage and Management", "2025-02-02", "2025-02-18"),
    ("Simulation Research", "2025-02-03", "2025-02-20"),
    ("Data Simulation & Augmentation", "2025-02-03", "2025-02-28"),
    ("Interim Report", "2025-02-03", "2025-03-26"),
    ("Reinforcement Learning for Resource Management", "2025-03-01", "2025-03-26"),
    ("Model Updates", "2025-03-26", "2025-03-31"),
    ("Integrate Models", "2025-03-31", "2025-04-07"),
    ("Dashboard Visualization & User Interaction", "2025-03-27", "2025-04-15"),
    ("Final Report", "2025-03-26", "2025-05-14"),
]

# Convert data to DataFrame
df = pd.DataFrame(tasks, columns=["Task", "Start", "End"])
df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])
df["Duration"] = df["End"] - df["Start"]

# Plot updated Gantt chart
fig, ax = plt.subplots(figsize=(12, 6))
for i, (task, start, end) in enumerate(zip(df["Task"], df["Start"], df["End"])):
    ax.barh(task, (end - start).days, left=start, color="lightblue")

# Format x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%Y"))
plt.xticks(rotation=45)
plt.xlabel("Timeline")
plt.ylabel("Tasks")
plt.title("Gantt Chart for Hybrid Quantum Resource Management System")
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Show plot
plt.show()

