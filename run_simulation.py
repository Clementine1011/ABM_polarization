from opinion_dynamics.opinion_system import OpinionSystem
from opinion_dynamics.ai_agent import AIAgent
from opinion_dynamics.config import *
import csv

# 运行舆论模拟实验
def run_simulation(num_agents, max_steps, ai_role=None, epsilon=0.01, stability_window=5):
    """
    运行舆论模拟实验
    :param num_agents: 普通 agents 的数量
    :param max_steps: 最大时间步数
    :param ai_role: AI 的角色类型（None 表示无 AI 干预；其他为干预策略）
    :param epsilon: 情感极端化稳定检测的阈值
    :param stability_window: 检测稳定性的时间步窗口大小
    :return: 每一步的系统状态列表
    """
    print(f"Running simulation with {num_agents} agents. AI role: {ai_role if ai_role else 'None'}")
    
    # 初始化舆论系统
    system = OpinionSystem(
        num_agents=num_agents,
        network_structure=NETWORK_STRUCTURE,
        opinion_range=OPINION_RANGE,
        emotion_range=EMOTION_RANGE,
        connection_probability=CONNECTION_PROBABILITY
    )
    
    # 初始化 AI Agent（如果有）
    ai_agent = AIAgent(role=ai_role) if ai_role else None

    # 用于存储每一步的系统状态
    results = []
    stability_check = []  # 存储最近若干步的情感极端化值，用于检测稳定性

    # 运行若干时间步
    for step in range(max_steps):
        print(f"Step {step + 1}/{max_steps}...")
        
        # 获取当前系统状态
        state = system.get_system_state()
        emotional_extremity = state[1]  # 当前情感极端化值

        # 记录当前状态
        results.append({
            "step": step + 1,
            "opinion_polarization": state[0],
            "emotional_extremity": state[1]
        })

        # 检查情感极端化的稳定性
        stability_check.append(emotional_extremity)
        if len(stability_check) > stability_window:
            stability_check.pop(0)  # 保留最近 stability_window 个时间步的值
            # 检查最近窗口内的变化是否小于 epsilon
            if max(abs(stability_check[i] - stability_check[i - 1]) for i in range(1, len(stability_check))) < epsilon*10:
                print("System has stabilized based on emotional_extremity.")
                break

        # AI 干预（如果有）
        if ai_agent:
            ai_agent.intervene(state, system.agents)

        # 系统更新
        system.step()

    print("Simulation complete.")
    return results

# 保存实验结果到 CSV 文件
def save_results(results, filename):
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["step", "opinion_polarization", "emotional_extremity"])
        writer.writeheader()
        writer.writerows(results)

# 主程序入口
if __name__ == "__main__":
    # 运行基线实验（无 AI 干预）
    baseline_results = run_simulation(
        num_agents=NUM_AGENTS,
        max_steps=NUM_STEPS,
        ai_role=None,                # 无 AI 干预
        epsilon=0.01,
        stability_window=5
    )
    save_results(baseline_results, "baseline_results.csv")

    # 运行 AI 干预实验
    ai_results = run_simulation(
        num_agents=NUM_AGENTS,
        max_steps=NUM_STEPS,
        ai_role=AI_ROLE,             # 有 AI 干预
        epsilon=0.01,
        stability_window=5
    )
    save_results(ai_results, "ai_results.csv")

    print("All experiments completed. Results saved.")
