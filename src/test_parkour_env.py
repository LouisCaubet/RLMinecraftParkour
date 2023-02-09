"""
Created on Feb 09, 2023

@author: LouisCaubet
"""

if __name__ == "__main__":
    import gym
    import time
    import os

    import minerl
    from parkour_env import MinecraftParkourEnv

    import logging
    logging.basicConfig(level=logging.DEBUG)

    os.environ['MINERL_PARKOUR_MAP'] = "assets/dev_map.csv"

    env = MinecraftParkourEnv()
    if env.name not in gym.envs.registry.env_specs:
        env.register()

    env = gym.make('MinecraftParkour-v0')
    env.reset()

    done = False
    while not done:
        env.step(env.action_space.noop())
        time.sleep(0.1)
        env.render()

    env.close()
