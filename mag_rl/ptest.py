import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from single_agent_env import SingleAgentEnv

env = SingleAgentEnv()
model = PPO("MlpPolicy", env, verbose=1, learning_rate=1e-4)

# ---- Train ----
model.learn(total_timesteps=50000)

# ---- Evaluate ----
print("\n Evaluation Result:")
rewards = []
for _ in range(10):
    obs = env.reset()
    total_reward = 0
    done = False
    step_count = 0
    while not done and step_count < 100:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        step_count += 1
    rewards.append(total_reward)

mean_reward = np.mean(rewards)
std_reward = np.std(rewards)
print(f"Mean reward = {mean_reward:.2f}, Std = {std_reward:.2f}")

# ---- Test with Logging ----
obs = env.reset()
done = False
total_reward = 0
time_steps, completed_tasks, avg_wait_times = [], [], []
step_count = 0

while not done and step_count < 100:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _ = env.step(action)
    total_reward += reward
    step_count += 1

    time_steps.append(env.env.time)
    completed = env.env.task_status.count("done")
    waiting = [env.env.time - t['duration'] for i, t in enumerate(env.env.tasks)
               if env.env.task_status[i] == "waiting"]
    avg_wait = np.mean(waiting) if waiting else 0
    completed_tasks.append(completed)
    avg_wait_times.append(avg_wait)

print("\nTotal reward from this episode:", total_reward)

# ---- Plot ----
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(time_steps, completed_tasks, label='Completed Tasks', color='blue', marker='o')
ax1.set_xlabel("Time Step")
ax1.set_ylabel("Completed Tasks", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(time_steps, avg_wait_times, label='Avg Waiting Time', color='red', marker='x')
ax2.set_ylabel("Avg Waiting Time", color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title("Task Completion and Average Waiting Time Over Time")
plt.tight_layout()
plt.savefig("ppo_task_progress.png")
print(" 图像已保存为 'ppo_task_progress.png'")
plt.show()


