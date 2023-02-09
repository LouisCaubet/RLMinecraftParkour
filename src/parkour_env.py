"""
Created on Feb 09, 2023

@author: LouisCaubet
"""
from typing import List
import csv
import os

from minerl.herobraine.env_specs.basalt_specs import BasaltBaseEnvSpec, MINUTE
from minerl.herobraine.env_specs.simple_embodiment import SimpleEmbodimentEnvSpec
from minerl.herobraine.hero.handler import Handler
import minerl.herobraine.hero.handlers as handlers
from minerl.herobraine.hero.mc import MS_PER_STEP

from block_list_handler import BlockListHandler
from flat_world_generator_handler import FlatWorldGenerator

NAVIGATE_STEPS = 6000


class MinecraftParkourEnv(BasaltBaseEnvSpec):

    def __init__(self):
        super().__init__(
            name="MinecraftParkour-v0",
            demo_server_experiment_name="minecraft_parkour",
            max_episode_steps=12 * MINUTE,
            preferred_spawn_biome="ocean",
            inventory=[],
        )
        self.blocks = []
        self.start_block = None

    def load_map(self, map_csv: str):
        # read csv and create list of blocks
        print("Called load map")
        self.blocks = []
        with open(map_csv, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # skip first line
            next(reader)
            for row in reader:
                x = int(row[0])
                y = int(row[1])
                z = int(row[2])
                block_type = row[3]
                self.blocks.append([x, y, z, block_type])

        self.start_block = self.blocks[0]

    def create_rewardables(self) -> List[handlers.TranslationHandler]:
        return [
            handlers.RewardForTouchingBlockType([
                       {'type': 'diamond_block', 'behaviour': 'onceOnly',
                        'reward': 100.0},
                   ]),
        ]

    def create_agent_start(self) -> List[Handler]:
        return super().create_agent_start() + [
            handlers.AgentStartPlacement(0, 128, 0)
        ]

    # def create_agent_handlers(self) -> List[Handler]:
    #     return [
    #         handlers.AgentQuitFromTouchingBlockType(
    #             ["diamond_block"]
    #         )
    #     ]

    # def create_server_initial_conditions(self) -> List[Handler]:
    #     return [
    #         handlers.TimeInitialCondition(
    #             allow_passage_of_time=False,
    #             start_time=6000
    #         ),
    #         handlers.WeatherInitialCondition('clear'),
    #         handlers.SpawningInitialCondition(False),
    #     ]

    # def create_server_decorators(self) -> List[Handler]:
    #     # Create XML string to draw blocks
    #     map_csv_path = os.environ['MINERL_PARKOUR_MAP']
    #     self.load_map(map_csv_path)
    #
    #     return [
    #         BlockListHandler(self.blocks)
    #     ]

    def create_server_world_generators(self) -> List[Handler]:
        path_to_world = os.path.abspath(os.path.join("assets", "empty_mc_world"))
        return [
            handlers.FileWorldGenerator(path_to_world)
        ]

    # def create_server_quit_producers(self) -> List[Handler]:
    #     return [
    #         handlers.ServerQuitFromTimeUp(NAVIGATE_STEPS * MS_PER_STEP),
    #         handlers.ServerQuitWhenAnyAgentFinishes()
    #     ]
