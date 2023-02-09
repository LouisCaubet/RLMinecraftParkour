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
        return str("""
        <DrawingDecorator>
            {% for block in blocks %}
                <Block type="{{block[3]}}" x="{{block[0]}}" y="{{block[1]}}" z="{{block[2]}}" />
            {% endfor %}
        </DrawingDecorator>
        """)
