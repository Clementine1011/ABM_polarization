import numpy as np
class Agent:
    def __init__(self, opinion, emotion):
        self.opinion = opinion
        self.emotion = emotion

    def update_opinion(self, neighbors_opinions, influence_factor=0.5):
        self.opinion += influence_factor * (np.mean(neighbors_opinions) - self.opinion)
        self.opinion = np.clip(self.opinion, -1, 1)

    def update_emotion(self, neighbors_opinions):
        disagreement = np.mean([abs(self.opinion - o) for o in neighbors_opinions])
        self.emotion += 10 * disagreement
        self.emotion = np.clip(self.emotion, 0, 100)

class OpinionSystem:
    def __init__(self, num_agents, network_structure="random", opinion_range=(-1, 1), emotion_range=(0, 100), connection_probability=0.1):
        self.num_agents = num_agents
        self.opinion_range = opinion_range
        self.emotion_range = emotion_range
        self.connection_probability = connection_probability
        self.agents = self._initialize_agents()  # 调用 _initialize_agents 方法
        self.network = self._initialize_network(network_structure)


    def _initialize_agents(self):
        agents = [
            Agent(
                opinion=np.random.uniform(self.opinion_range[0], self.opinion_range[1]),
                emotion=np.random.uniform(self.emotion_range[0], self.emotion_range[1])
            )
            for _ in range(self.num_agents)
        ]

        # 增加极端个体
        num_extreme = int(0.1 * self.num_agents)  # 设置 10% 个体为极端观点
        extreme_indices = np.random.choice(range(self.num_agents), num_extreme, replace=False)
        for idx in extreme_indices[:num_extreme // 2]:
            agents[idx].opinion = 1  # 极端正观点
        for idx in extreme_indices[num_extreme // 2:]:
            agents[idx].opinion = -1  # 极端负观点

        return agents

    def _initialize_network(self, network_structure):
        if network_structure == "random":
            return np.random.rand(self.num_agents, self.num_agents) < self.connection_probability
        elif network_structure == "small_world":
            import networkx as nx
            G = nx.watts_strogatz_graph(self.num_agents, k=10, p=self.connection_probability)  # k=每节点邻居数，p=随机重连概率
            return nx.to_numpy_array(G) > 0  # 将网络转换为邻接矩阵
        else:
            raise ValueError("Unsupported network structure")


    def get_system_state(self):
        opinions = [agent.opinion for agent in self.agents]
        emotions = [agent.emotion for agent in self.agents]
        return np.mean(opinions), np.mean(emotions)

    def step(self):
        for agent in self.agents:
            neighbors = [self.agents[i] for i in range(self.num_agents) if self.network[self.agents.index(agent), i]]
            neighbors_opinions = [neighbor.opinion for neighbor in neighbors]
            agent.update_opinion(neighbors_opinions)
            agent.update_emotion(neighbors_opinions)

        # 随机扰动一部分个体
        num_perturbed = int(0.05 * self.num_agents)  # 设置 5% 的个体受随机扰动
        perturbed_indices = np.random.choice(range(self.num_agents), num_perturbed, replace=False)
        for idx in perturbed_indices:
            self.agents[idx].opinion += np.random.uniform(-0.1, 0.1)  # 随机扰动
            self.agents[idx].opinion = np.clip(self.agents[idx].opinion, -1, 1)  # 限制范围

