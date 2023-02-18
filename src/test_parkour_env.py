"""
Created on Feb 09, 2023

@author: LouisCaubet
"""
import os
import numpy as np
import minerl
import malmoenv
import parser
import argparse
import stable_baselines3
import tensorflow as tf
# Override the default mission template
import minerl.herobraine.env_spec
minerl.herobraine.env_spec.MISSION_TEMPLATE = os.path.join("assets", "mission.xml.j2")


# Define the network architecture
def create_model(env):
    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(6400,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(env.action_space), activation='linear')
    ])

    return model

# Define the epsilon-greedy exploration strategy
def epsilon_greedy_policy(state, epsilon, env, model):
    if np.random.rand() < epsilon:
        return env.action_space.sample()
    else:
        Q_values = model.predict(state)
        return np.argmax(Q_values)

# Train the agent
def train(num_episodes, env,  model, discount_factor=0.95, epsilon=0.1, epsilon_decay=0.99):
    for episode in range(num_episodes):
        # Initialize the environment
        state = env.reset()

        # Convert the state to a vector
        state = state.reshape((1, 6400))

        done = False
        while not done:
            # Choose the next action using the epsilon-greedy policy
            action = epsilon_greedy_policy(state, epsilon, env)

            # Take a step in the environment
            next_state, reward, done, info = env.step(action)
            next_state = next_state.reshape((1, 6400))

            # Update the Q-value for the taken action
            Q_values = model.predict(state)
            Q_values[0][action] = reward + discount_factor * np.max(model.predict(next_state))
            model.fit(state, Q_values, verbose=0)

            state = next_state

            if done:
                print("Episode {}/{} finished after {} steps".format(episode + 1, num_episodes, info['steps']))

        # Decay the exploration rate
        epsilon *= epsilon_decay

if __name__ == "__main__":
    import gym
    import time

    from parkour_env import MinecraftParkourEnv

    import logging
    logging.basicConfig(level=logging.DEBUG)

    os.environ['MINERL_PARKOUR_MAP'] = "assets/ines_map.csv"
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
    mission_xml = MinecraftParkourEnv().to_xml()

    env.init(mission_xml, args.port,
             server=args.server,
             server2=args.server2, port2=args.port2,
             role=args.role,
             exp_uid=args.experimentUniqueId,
             episode=args.episode, resync=args.resync)
    

    model = create_model(env)
    model.compile(loss='mean_squared_error', optimizer='adam')


    train(100, env, model)

    

    env.close()
    with open("assets/mission.xml", "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        f.write(mission_xml)

    # Send to Malmo (which must be started separately)
    os.chdir("../malmo/MalmoEnv")

    # Replace this with a custom script for training
    os.system("python run.py --mission ../../RLMinecraftParkour/assets/mission.xml --port 9000")
