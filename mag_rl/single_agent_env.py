import gym
from gym import spaces
import numpy as np
from task_simulator import TaskSimulator
from single_scheduling_env import SingleAgentSchedulingEnv

class SingleAgentEnv(gym.Env):
    def __init__(self):
        super(SingleAgentEnv, self).__init__()
        self.simulator = TaskSimulator()
        self.tasks, self.edges = self.simulator.generate_dag()  # 生成任务及依赖边
        self.env = SingleAgentSchedulingEnv(
            tasks=self.tasks,
            edges=self.edges,
            resource_pool={"CPU": 2, "GPU": 2, "QPU": 1}
        )

        obs_dim = len(self.env._get_obs())
        self.observation_space = spaces.Box(low=0, high=100, shape=(obs_dim,), dtype=np.float32)
        self.action_space = spaces.Discrete(len(self.tasks))  # 每个任务一个动作

    def reset(self):
        self.tasks, self.edges = self.simulator.generate_dag()
        self.env = SingleAgentSchedulingEnv(
            tasks=self.tasks,
            edges=self.edges,
            resource_pool={"CPU": 2, "GPU": 2, "QPU": 1}
        )
        return self.env.reset()

    def step(self, action):
        obs, reward, done, info = self.env.step(int(action))  # 确保 action 是 int
        return obs, reward, done, info

    def render(self, mode="human"):
        self.env.render()