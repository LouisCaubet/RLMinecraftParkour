"""
Created on Feb 09, 2023

@author: LouisCaubet
"""
import os
import numpy as np
import malmo
import malmoenv
import parser
import argparse
import stable_baselines3
# Override the default mission template
import minerl.herobraine.env_spec
minerl.herobraine.env_spec.MISSION_TEMPLATE = os.path.join("assets", "mission.xml.j2")


if __name__ == "__main__":
    import gym
    import time

    from parkour_env import MinecraftParkourEnv

    import logging
    logging.basicConfig(level=logging.DEBUG)

    os.environ['MINERL_PARKOUR_MAP'] = "assets/dev_map.csv"
    malmo_version = '0.37.0'

    # env = MinecraftParkourEnv()

    parser = argparse.ArgumentParser(description='malmovnv test')
    parser.add_argument('--mission', type=str, default='missions/mobchase_single_agent.xml', help='the mission xml')
    parser.add_argument('--port', type=int, default=9000, help='the mission server port')
    parser.add_argument('--server', type=str, default='127.0.0.1', help='the mission server DNS or IP address')
    parser.add_argument('--port2', type=int, default=None, help="(Multi-agent) role N's mission port. Defaults to server port.")
    parser.add_argument('--server2', type=str, default=None, help="(Multi-agent) role N's server DNS or IP")
    parser.add_argument('--episodes', type=int, default=1, help='the number of resets to perform - default is 1')
    parser.add_argument('--episode', type=int, default=0, help='the start episode - default is 0')
    parser.add_argument('--role', type=int, default=0, help='the agent role - defaults to 0')
    parser.add_argument('--episodemaxsteps', type=int, default=0, help='max number of steps per episode')
    parser.add_argument('--saveimagesteps', type=int, default=0, help='save an image every N steps')
    parser.add_argument('--resync', type=int, default=0, help='exit and re-sync every N resets'
                                                              ' - default is 0 meaning never.')
    parser.add_argument('--experimentUniqueId', type=str, default='test1', help="the experiment's unique id.")
    args = parser.parse_args()
    if args.server2 is None:
        args.server2 = args.server

    env = malmoenv.make()
    mission_xml = env.to_xml()

    env.init(mission_xml, args.port,
             server=args.server,
             server2=args.server2, port2=args.port2,
             role=args.role,
             exp_uid=args.experimentUniqueId,
             episode=args.episode, resync=args.resync)
    

    model = stable_baselines3.DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000) #Est-ce que je dois mettre le Timelimits du XML?

    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        # vec_env.render() Essaie ça stv 
        # VecEnv resets automatically
        # if done:
        #   obs = env.reset()

    env.close()
    with open("assets/mission.xml", "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        f.write(mission_xml)

    # Send to Malmo (which must be started separately)
    os.chdir("../malmo/MalmoEnv")

    # Replace this with a custom script for training
    os.system("python run.py --mission ../../RLMinecraftParkour/assets/mission.xml --port 9000")

    # env = gym.make('MinecraftParkour-v0')
    # env.reset()
    #
    # done = False
    # while not done:
    #     env.step(env.action_space.noop())
    #     time.sleep(0.1)
    #     env.render()
    #
    # env.close()
