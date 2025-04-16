from pprint import pprint
from task_simulator import TaskSimulator 
import random

class SchedulingEnv:
    def __init__(self, dag, resource_pool=None, max_time=50):
        self.task_graph = dag["tasks"]
        self.edges = dag["edges"]
        self.num_tasks = len(self.task_graph)
        self.max_time = max_time
        self.time = 0

        # 默认资源池
        self.resources = resource_pool or {
            "CPU": 2,
            "GPU": 2,
            "QPU": 1
        }

        # 初始化状态
        self.resource_status = {r: [0] * self.resources[r] for r in self.resources}
        self.task_status = ["waiting"] * self.num_tasks  # waiting, running, done
        self.remaining_time = [0] * self.num_tasks
        self.in_degrees = self._compute_in_degrees()

    def _compute_in_degrees(self):
        in_deg = [0] * self.num_tasks
        for u, v in self.edges:
            in_deg[v] += 1
        return in_deg

    def reset(self):
        self.time = 0
        self.resource_status = {r: [0] * self.resources[r] for r in self.resources}
        self.task_status = ["waiting"] * self.num_tasks
        self.remaining_time = [0] * self.num_tasks
        self.in_degrees = self._compute_in_degrees()
        return self.get_obs()

    def step(self, task_id):
        reward = 0

        if not self.is_task_ready(task_id):
            return self.get_obs(), -5, False  # penalize illegal action

        task = self.task_graph[task_id]
        resources_needed = task["need"]
        assigned = []

        # 分配资源
        for r in resources_needed:
            slots = self.resource_status[r]
            found = False
            for i in range(len(slots)):
                if slots[i] == 0:
                    slots[i] = task["duration"]
                    assigned.append((r, i))
                    found = True
                    break
            if not found:
                return self.get_obs(), -3, False  # penalize if resources not available

        # 启动任务
        self.task_status[task_id] = "running"
        self.remaining_time[task_id] = task["duration"]
        reward += 5  # 正常调度得分

        # 模拟时间前进一小步
        self._tick()

        done = all(s == "done" for s in self.task_status)
        return self.get_obs(), reward, done

    def _tick(self):
        self.time += 1

        # 更新资源状态
        for r in self.resource_status:
            for i in range(len(self.resource_status[r])):
                if self.resource_status[r][i] > 0:
                    self.resource_status[r][i] -= 1

        # 更新任务状态
        for i in range(self.num_tasks):
            if self.task_status[i] == "running":
                self.remaining_time[i] -= 1
                if self.remaining_time[i] == 0:
                    self.task_status[i] = "done"
                    for u, v in self.edges:
                        if u == i:
                            self.in_degrees[v] -= 1

    def is_task_ready(self, task_id):
        return (
            self.task_status[task_id] == "waiting" and
            self.in_degrees[task_id] == 0 and
            all(any(slot == 0 for slot in self.resource_status[r]) for r in self.task_graph[task_id]["need"])
        )

    def get_obs(self):
        # 简化版：返回当前每个 task 的状态 + 当前资源状态
        task_info = [
            {
                "id": task["id"],
                "type": task["type"],
                "need": task["need"],
                "priority": task["priority"],
                "status": self.task_status[i],
                "ready": self.is_task_ready(i)
            }
            for i, task in enumerate(self.task_graph)
        ]

        return {
            "time": self.time,
            "tasks": task_info,
            "resource_status": self.resource_status
        }

    def get_avail_actions(self):
        return [i for i in range(self.num_tasks) if self.is_task_ready(i)]