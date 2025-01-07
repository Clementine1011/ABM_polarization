import pandas as pd
import matplotlib.pyplot as plt

# 加载实验结果
baseline_data = pd.read_csv("baseline_results.csv")
ai_data = pd.read_csv("ai_results.csv")

# 绘制意见极化曲线
plt.figure(figsize=(10, 5))
plt.plot(baseline_data["step"], baseline_data["opinion_polarization"], label="Baseline (No AI)", color="blue")
plt.plot(ai_data["step"], ai_data["opinion_polarization"], label="With AI", color="red")
plt.title("Opinion Polarization Over Time")
plt.xlabel("Steps")
plt.ylabel("Opinion Polarization")
plt.legend()
plt.show()

# 绘制情感极端化曲线
plt.figure(figsize=(10, 5))
plt.plot(baseline_data["step"], baseline_data["emotional_extremity"], label="Baseline (No AI)", color="blue")
plt.plot(ai_data["step"], ai_data["emotional_extremity"], label="With AI", color="red")
plt.title("Emotional Extremity Over Time")
plt.xlabel("Steps")
plt.ylabel("Emotional Extremity")
plt.legend()
plt.show()
