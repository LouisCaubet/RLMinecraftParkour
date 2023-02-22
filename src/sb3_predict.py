"""
Created on Feb 22, 2023

@author: LouisCaubet
"""
from sb3_training import create_env
from stable_baselines3 import DQN, A2C, PPO

if __name__ == "__main__":
    env = create_env()
    obs = env.reset()

    model = PPO.load("dqn_minecraft_parkour_level1_v1", print_system_info=True)

    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()

        print("Reward: ", reward)

        if done:
            obs = env.reset()

    env.close()
