"""
Created on Feb 09, 2023

@author: LouisCaubet

Adapted from MineRL source code.
"""
import jinja2
from minerl.herobraine.hero.handler import Handler


class FlatWorldGenerator(Handler):
    """Generates a world that is a flat landscape."""

    def to_string(self) -> str:
        return "flat_world_generator"

    def xml_template(self) -> str:
        return str(
            """<FlatWorldGenerator
                forceReset="{{force_reset | string | lower}}"
                generatorString="{{generatorString}}"
                seed="{{seed}}"/>
            """
        )

    def __init__(self, force_reset: bool = True, generatorString: str = "", seed: int = 0):
        self.force_reset = force_reset
        self.generatorString = generatorString
        self.seed = seed
