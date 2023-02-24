"""
Created on Feb 19, 2023

@author: LouisCaubet
"""
import os
import gym
import malmoenv
from stable_baselines3 import DQN, A2C, PPO
import logging
from dotenv import load_dotenv

from parkour_env import MinecraftParkourEnv
from wrapped_malmo_env import WrappedEnv

XML_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"

# Override the default mission template
import minerl.herobraine.env_spec
minerl.herobraine.env_spec.MISSION_TEMPLATE = os.path.join("assets", "mission.xml.j2")

logging.basicConfig(level=logging.DEBUG)


def create_env():
    malmo_env = malmoenv.make()
    mission_xml = MinecraftParkourEnv().to_xml()
    mission_xml = XML_HEADER + mission_xml

    port = int(os.environ.get("MALMO_PORT", 9000))

    malmo_env.init(mission_xml, port,
                   server='127.0.0.1',
                   server2='127.0.0.1', port2=None,
                   role=0,
                   exp_uid='test1',
                   episode=0,
                   resync=0,
                   reshape=True,
                   action_filter={"move", "strafe", "jumpstrafe"}
                   )

    wrapped_env = WrappedEnv(malmo_env)

    return wrapped_env


if __name__ == "__main__":
    load_dotenv(".env")
    
    env = create_env()
    algorithm = os.environ.get("SB3_ALGO", "PPO")
    timesteps = int(os.environ.get("SB3_TIMESTEPS", 10000))
    export_name = os.environ.get("S3_TRAINED_MODEL_NAME", "dqn_minecraft_parkour")

    if algorithm == "DQN":
        model = DQN('MlpPolicy', env, verbose=1, buffer_size=100)
    elif algorithm == "A2C":
        model = A2C('MlpPolicy', env, verbose=1, tensorboard_log="./logs_mcparkour")
    elif algorithm == "PPO":
        model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./logs_mcparkour")
    else:
        raise ValueError(f"Unknown algorithm {algorithm}. Supported values: PPO, A2C, DQN")

    model.learn(total_timesteps=timesteps)
    model.save(export_name)

    env.close()
