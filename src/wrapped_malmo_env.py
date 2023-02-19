"""
Created on Feb 19, 2023

@author: LouisCaubet
"""
import gym


class WrappedEnv(gym.Env):

    def __init__(self, malmo_env):
        self.env = malmo_env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        # SB3 expects a dict
        info = {'info': info}
        return obs, reward, done, info

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        return self.env.render(mode)

    def close(self):
        return self.env.close()
