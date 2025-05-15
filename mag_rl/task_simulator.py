import random

class TaskSimulator:
    def __init__(self, num_tasks=6, quantum_ratio=0.3, hybrid_ratio=0.2, max_duration=5):
        self.num_tasks = num_tasks
        self.quantum_ratio = quantum_ratio
        self.hybrid_ratio = hybrid_ratio
        self.max_duration = max_duration

    def generate_dag(self):
        tasks = []
        for i in range(self.num_tasks):
            task_type = random.choices(
                ["classical", "quantum", "hybrid"],
                weights=[
                    1.0 - self.quantum_ratio - self.hybrid_ratio,
                    self.quantum_ratio,
                    self.hybrid_ratio
                ]
            )[0]

            if task_type == "quantum":
                need = ["QPU"]
            elif task_type == "classical":
                need = ["CPU"] if random.random() < 0.5 else ["GPU"]
            else:  # hybrid
                classical = "CPU" if random.random() < 0.5 else "GPU"
                need = ["QPU", classical]

            task = {
                "id": f"T{i}",
                "type": task_type,
                "need": need,
                "duration": random.randint(1, self.max_duration),
                "priority": random.randint(1, 3)
            }
            tasks.append(task)

        # 随机生成 acyclic 边（依赖关系）
        edges = []
        for i in range(self.num_tasks):
            for j in range(i + 1, self.num_tasks):
                if random.random() < 0.3:  # 30% 概率生成依赖边
                    edges.append((i, j))  # i 是 j 的前置任务

        return tasks, edges