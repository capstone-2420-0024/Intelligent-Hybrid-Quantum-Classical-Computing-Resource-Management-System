from task_simulator import TaskSimulator
from scheduling_env import SchedulingEnv
from pprint import pprint

def main():
    # 1. 生成任务图
    sim = TaskSimulator(num_tasks=6, quantum_ratio=0.3, hybrid_ratio=0.2)
    dag = sim.generate_dag(isolated_ratio=0.2)

    # 2. 初始化环境
    env = SchedulingEnv(dag)
    obs = env.reset()

    # 3. 打印初始状态
    print("==== 初始任务图状态 ====")
    pprint(obs)

    # 4. 每一步调度一个可调度任务（手动 rule-based）
    done = False
    total_reward = 0

    while not done:
        avail = env.get_avail_actions()
        if not avail:
            print("当前无可调度任务，时间推进...")
            env._tick()
            continue

        action = avail[0]
        print(f"\nTime {obs['time']} | 调度任务: {action}")
        obs, reward, done = env.step(action)
        total_reward += reward
        print(f" reward={reward} | done={done}")
        pprint(obs)

    print(f"\n 所有任务完成，总 reward: {total_reward}")

# ✅ 加上这个执行入口
if __name__ == "__main__":
    main()
    