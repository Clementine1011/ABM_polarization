# config.py
NUM_AGENTS = 1000                      # 普通 agents 的数量
NETWORK_STRUCTURE = "small_world"     # 网络结构：random 或 small_world
OPINION_RANGE = (-1, 1)               # 初始意见值范围
EMOTION_RANGE = (0, 100)              # 初始情感强度范围
CONNECTION_PROBABILITY = 0.3          # 随机网络的连接概率
NUM_STEPS = 200                       # 每次实验的时间步数
NUM_EXPERIMENTS = 5                  # 实验重复次数
AI_ROLE = "guider"                    # AI 的角色：neutral, generator, guider
CSV_FILENAME = "experiment_results.csv"  # 保存结果的文件名
