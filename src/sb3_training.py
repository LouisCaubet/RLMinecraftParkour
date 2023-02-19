"""
Created on Feb 19, 2023

@author: LouisCaubet
"""
import os
import gym
import malmoenv
from stable_baselines3 import DQN, A2C, PPO
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
    model = DQN('CnnPolicy', env, verbose=1, buffer_size=100)
    # model = PPO('CnnPolicy', env, verbose=1)
    model.learn(total_timesteps=1000000)
    model.save("dqn_minecraft_parkour")

    env.env.close()
