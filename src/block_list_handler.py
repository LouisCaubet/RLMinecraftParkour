"""
Created on Feb 09, 2023

@author: LouisCaubet
"""
import jinja2
from minerl.herobraine.hero.handler import Handler


class BlockListHandler(Handler):

    def __init__(self, blocks: list):
        super().__init__()
        self.blocks = blocks

    def to_string(self) -> str:
        return "block_list_handler"

    def xml_template(self) -> str:
        # <DrawCuboid x1="-10000" y1="69" z1="-10000" x2="10000" y2="70" z2="10000" type="bedrock" />
        return str("""
        <DrawingDecorator>
            {% for block in blocks %}
                <DrawBlock type="{{block[3]}}" x="{{block[0]}}" y="{{block[1]}}" z="{{block[2]}}" />
            {% endfor %}
        </DrawingDecorator>
        """)
