"""
Created on Feb 19, 2023

@author: LouisCaubet
"""
import time

import gym
from malmoenv import VisualObservationSpace
from torchvision import transforms
from PIL import Image
import numpy as np


class WrappedEnv(gym.Env):

    def __init__(self, malmo_env):
        self.env = malmo_env
        self.action_space = self.env.action_space
        self.observation_space = VisualObservationSpace(64, 64, 3)

        self.obs_transform = transforms.Resize((64, 64))

    def step(self, action: int):
        obs, reward, done, info = self.env.step(action)
        # SB3 expects a dict
        info = {'info': info}

        # Add a small negative reward when turning (to encourage moving forward)
        # if action > 1:
        #     reward -= 1

        if reward > 0:
            print("Reward: " + str(reward))

        img = Image.fromarray(obs)
        img = self.obs_transform(img)
        obs = np.array(img)

        time.sleep(0.1)

        return obs, reward, done, info

    def reset(self):
        obs = self.env.reset()
        img = Image.fromarray(obs)
        img = self.obs_transform(img)
        obs = np.array(img)
        return obs

    def render(self, mode='human'):
        return self.env.render(mode)

    def close(self):
        return self.env.close()
