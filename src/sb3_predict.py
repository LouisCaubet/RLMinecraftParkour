"""
Created on Feb 22, 2023

@author: LouisCaubet
"""
from sb3_training import create_env
from stable_baselines3 import DQN, A2C, PPO
import time
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv(".env")
    env = create_env()
    obs = env.reset()

    model_name = os.environ.get("SB3_INFERENCE_MODEL_NAME", "dqn_minecraft_parkour")
    algorithm = os.environ.get("SB3_ALGO", "PPO")
    steps = int(os.environ.get("SB3_INFERENCE_STEPS", 1000))

    if algorithm == "DQN":
        model = DQN.load(model_name, print_system_info=True)
    elif algorithm == "A2C":
        model = A2C.load(model_name, print_system_info=True)
    elif algorithm == "PPO":
        model = PPO.load(model_name, print_system_info=True)
    else:
        raise ValueError(f"Unknown algorithm {algorithm}. Supported values: PPO, A2C, DQN")

    time.sleep(2)

    for i in range(steps):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()

        print("Reward: ", reward)

        if done:
            obs = env.reset()

    env.close()
