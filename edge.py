import arcade 
import math
from node import Node

class Edge:

    def __init__(self,start_node=Node(),end_node=Node()):
        self.start_node = start_node
        self.end_node = end_node
        self.road = "NONE"
        self.width = 6

    def get_start_node(self):
        return self.start_node
    
    def get_end_node(self):
        return self.end_node
    
    def build_road(self,player):
        if self.road == "NONE" and player.woodCount > 0 and player.brickCount > 0:
            self.road = player
            player.useWood(1)
            player.useBrick(1)
            return True
        return False

    # helper function for center tile point calculations
    def edge_length(self):
        return math.sqrt(math.pow((self.end_node.get_x() - self.start_node.get_x()),2) + 
                         math.pow((self.end_node.get_y() - self.start_node.get_y()),2))

    def draw(self):
        arcade.draw_line(self.start_node.get_x(), self.start_node.get_y(), 
                         self.end_node.get_x(), self.end_node.get_y(), arcade.color.BLACK, self.width)
