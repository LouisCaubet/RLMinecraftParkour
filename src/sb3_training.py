"""
Created on Feb 19, 2023

@author: LouisCaubet
"""
import os
import gym
import malmoenv
from stable_baselines3 import DQN
import time
import logging

from parkour_env import MinecraftParkourEnv
from wrapped_malmo_env import WrappedEnv

XML_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"

# Override the default mission template
import minerl.herobraine.env_spec
minerl.herobraine.env_spec.MISSION_TEMPLATE = os.path.join("assets", "mission.xml.j2")

logging.basicConfig(level=logging.DEBUG)


def create_env():
    os.environ['MINERL_PARKOUR_MAP'] = "assets/ines_map.csv"
    malmo_version = '0.37.0'

    malmo_env = malmoenv.make()
    mission_xml = MinecraftParkourEnv().to_xml()
    mission_xml = XML_HEADER + mission_xml

    malmo_env.init(mission_xml, 9000,
                   server='127.0.0.1',
                   server2='127.0.0.1', port2=None,
                   role=0,
                   exp_uid='test1',
                   episode=0, resync=0, reshape=True)

    wrapped_env = WrappedEnv(malmo_env)

    return wrapped_env


if __name__ == "__main__":
    env = create_env()
    model = DQN('MlpPolicy', env, verbose=1, buffer_size=100)
    model.learn(total_timesteps=10000)
    model.save("dqn_minecraft_parkour")

    # for i in range(10):
    #     print("reset " + str(i))
    #     obs = env.reset()
    #
    #     steps = 0
    #     done = False
    #     while not done and steps < 10000:
    #         action = env.action_space.sample()
    #
    #         obs, reward, done, info = env.step(action)
    #         steps += 1
    #         print("reward: " + str(reward))
    #         # print("done: " + str(done))
    #         print("obs: " + str(obs))
    #         # print("info" + info)
    #
    #         time.sleep(.05)

    env.env.close()
