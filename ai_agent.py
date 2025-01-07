class AIAgent:
    def __init__(self, role="neutral"):
        self.role = role

    def intervene(self, system_state, agents):
        if self.role == "neutral":
            self.neutral_intervention(agents)
        elif self.role == "generator":
            self.generate_information(agents)
        elif self.role == "guider":
            self.guide_opinions(agents, system_state)

    def neutral_intervention(self, agents):
        for agent in agents:
            agent.opinion += np.random.uniform(-0.1, 0.1)
            agent.opinion = np.clip(agent.opinion, -1, 1)

    def generate_information(self, agents):
        for agent in agents:
            generated_opinion = np.random.uniform(-0.5, 0.5)
            agent.opinion += 0.2 * (generated_opinion - agent.opinion)
            agent.opinion = np.clip(agent.opinion, -1, 1)

    def guide_opinions(self, agents, system_state):
        opinion_polarization, emotional_extremity = system_state
        if opinion_polarization > 0.3:
            for agent in agents:
                agent.opinion *= 0.9
