import arcade 
import math
from node import Node

class Edge:

    def __init__(self,start_node=Node(),end_node=Node()):
        self.start_node = start_node
        self.end_node = end_node
        self.road = "NONE"
        self.width = 6

    def set_width(self, width):
        self.width = width

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
    
    def is_touching(self, x, y):
        if self.start_node.get_x == self.end_node.get_x():
            if (x >= self.start_node.get_x() - self.width and x <= self.start_node.get_x() + self.width and 
                y >= min(self.start_node.get_y(),self.end_node.get_y()) and 
                y <= max(self.start_node.get_y(),self.end_node.get_y())):
                return True
        elif (x >= min(self.start_node.get_x(),self.end_node.get_x()) and x <= max(self.start_node.get_x(),self.end_node.get_x()) and
            y >= min(self.start_node.get_y(),self.end_node.get_y()) and 
            y <= max(self.start_node.get_y(),self.end_node.get_y())):
            return True
        return False
    
    def on_mouse_press(self, x, y, button, modifiers, player):
        if self.is_touching(x, y):
            self.build_road(player)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.is_touching(x, y) and self.width == 6:
            self.width += self.width * 0.5
        elif not self.is_touching(x, y):
            self.width = 6

    def draw(self):
        arcade.draw_line(self.start_node.get_x(), self.start_node.get_y(), 
                         self.end_node.get_x(), self.end_node.get_y(), arcade.color.BLACK, self.width)
