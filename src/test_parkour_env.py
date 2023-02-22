"""
Created on Feb 09, 2023

@author: LouisCaubet
"""
import os
import logging
from dotenv import load_dotenv
# noinspection PyUnresolvedReferences
import gym

# Override the default mission template
import minerl.herobraine.env_spec
minerl.herobraine.env_spec.MISSION_TEMPLATE = os.path.join("assets", "mission.xml.j2")

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    import time
    load_dotenv(".env")

    from parkour_env import MinecraftParkourEnv

    malmo_version = '0.37.0'

    env = MinecraftParkourEnv()
    mission_xml = env.to_xml()

    with open("assets/mission.xml", "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        f.write(mission_xml)

    # Send to Malmo (which must be started separately)
    os.chdir("malmo/MalmoEnv")

    # Replace this with a custom script for training
    os.system("python run.py --mission ../../assets/mission.xml --port 9000")
