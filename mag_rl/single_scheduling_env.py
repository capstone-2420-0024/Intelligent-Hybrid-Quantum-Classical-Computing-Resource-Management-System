import gym
import numpy as np

class SingleAgentSchedulingEnv(gym.Env):
    def __init__(self, tasks, edges, resource_pool):
        super(SingleAgentSchedulingEnv, self).__init__()

        self.tasks = tasks
        self.edges = edges
        self.resource_pool = resource_pool
        self.resource_status = {rtype: [0] * count for rtype, count in resource_pool.items()}
        self.task_status = ["waiting"] * len(tasks)
        self.task_remaining_time = [0] * len(tasks)
        self.time = 0
        self.resource_log = []

        self.dependency_map = {i: [] for i in range(len(tasks))}
        for parent, child in edges:
            self.dependency_map[child].append(parent)

        obs_dim = len(self._get_obs())
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(obs_dim,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(len(tasks))

    def reset(self):
        self.resource_status = {rtype: [0] * count for rtype, count in self.resource_pool.items()}
        self.task_status = ["waiting"] * len(self.tasks)
        self.task_remaining_time = [0] * len(self.tasks)
        self.time = 0
        self.resource_log = []
        return self._get_obs()

    def _dependencies_satisfied(self, task_id):
        return all(self.task_status[parent] == "done" for parent in self.dependency_map.get(task_id, []))

    def _get_obs(self):
        obs = [self.time]
        for i in range(len(self.tasks)):
            obs.extend([
                0 if self.task_status[i] == "waiting" else 1 if self.task_status[i] == "running" else 2,
                self.task_remaining_time[i],
                self.tasks[i]["priority"],
                self.tasks[i]["duration"],
                len(self.dependency_map.get(i, []))
            ])
        flat_resources = [val for res in self.resource_status.values() for val in res]
        obs.extend(flat_resources)
        return np.array(obs, dtype=np.float32)

    def _log_resource_usage(self):
        usage = {
            "time": self.time,
            "CPU": sum(self.resource_status.get("CPU", [])),
            "GPU": sum(self.resource_status.get("GPU", [])),
            "QPU": sum(self.resource_status.get("QPU", []))
        }
        self.resource_log.append(usage)

    def step(self, action):
        reward = 0
        info = {}
        done = False

        valid = self.task_status[action] == "waiting" and self._dependencies_satisfied(action)

        if not valid:
            reward -= 3  # 惩罚非法动作
        else:
            task = self.tasks[action]
            task_type = task['type']
            allocated = False

            if task_type == "quantum":
                qpu_free = next((i for i, val in enumerate(self.resource_status["QPU"]) if val == 0), None)
                if qpu_free is not None:
                    self.resource_status["QPU"][qpu_free] = task['duration']
                    self.task_status[action] = "running"
                    self.task_remaining_time[action] = task['duration']
                    allocated = True
            elif task_type == "classical":
                cpu_free = next((i for i, val in enumerate(self.resource_status["CPU"]) if val == 0), None)
                if cpu_free is not None:
                    self.resource_status["CPU"][cpu_free] = task['duration']
                    self.task_status[action] = "running"
                    self.task_remaining_time[action] = task['duration']
                    allocated = True
            elif task_type == "hybrid":
                qpu_free = next((i for i, val in enumerate(self.resource_status["QPU"]) if val == 0), None)
                gpu_free = next((i for i, val in enumerate(self.resource_status["GPU"]) if val == 0), None)
                if qpu_free is not None and gpu_free is not None:
                    self.resource_status["QPU"][qpu_free] = task['duration']
                    self.resource_status["GPU"][gpu_free] = task['duration']
                    self.task_status[action] = "running"
                    self.task_remaining_time[action] = task['duration']
                    allocated = True

            if allocated:
                reward += task['priority'] * 2  # 引导高优先级任务被调度
            else:
                reward -= 1  # 没有分配成功但任务合法

        self.time += 1
        for rtype in self.resource_status:
            for i in range(len(self.resource_status[rtype])):
                self.resource_status[rtype][i] = max(0, self.resource_status[rtype][i] - 1)

        for i, status in enumerate(self.task_status):
            if status == "running":
                self.task_remaining_time[i] -= 1
                if self.task_remaining_time[i] <= 0:
                    self.task_status[i] = "done"
                    reward += 10  # 完成奖励

        # 等待任务惩罚（降低等待时间快速增长带来的惩罚）
        for i, status in enumerate(self.task_status):
            if status == "waiting":
                reward -= 0.05 * self.tasks[i]['priority']

        # 任务全部完成
        if all(status == "done" for status in self.task_status):
            reward += 20
            done = True

        self._log_resource_usage()
        return self._get_obs(), reward, done, info

    def render(self, mode="human"):
        print(f"Time: {self.time}, Status: {self.task_status}, Resources: {self.resource_status}")