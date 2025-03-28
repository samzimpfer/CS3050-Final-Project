import arcade 
import math
from node import Node

class Edge:

    def __init__(self,start_node=Node(),end_node=Node()):
        self.start_node = start_node
        self.end_node = end_node
        self.road = False
        self.color = arcade.color.BLACK
        self.width = 6

    def set_width(self, width):
        self.width = width

    def get_start_node(self):
        return self.start_node
    
    def get_end_node(self):
        return self.end_node
    
    def get_color(self):
        return self.color
    
    def get_road(self):
        return self.road
    
    def build_road(self,player):
        if not self.road and player.canBuildRoad():
            self.road = True
            self.color = player.get_color()
            player.buildRoad(self.start_node, self.end_node)
            
            return True
        return False

    # helper function for center tile point calculations
    def edge_length(self):
        return math.sqrt(math.pow((self.end_node.get_x() - self.start_node.get_x()),2) + 
                         math.pow((self.end_node.get_y() - self.start_node.get_y()),2))
    
    # determines if the x y coordinate is touching the edge
    # reduced the size of the area so that the mouse can not hover over a node and edge at the same time
    def is_touching(self, x, y):
        # if the start and end node are on the same x axis
        if (self.get_start_node().get_x() == self.get_end_node().get_x() and y >= min(self.start_node.get_y()+6,self.end_node.get_y()+6) and 
            y <= max(self.start_node.get_y()-6,self.end_node.get_y()-6) and self.get_start_node().get_x() >= x - self.width and 
            self.get_start_node().get_x() <= x + self.width):
            return True
        # if the start and end node are not on the same x axis 
        elif (x >= min(self.start_node.get_x()+6,self.end_node.get_x()+6) and x <= max(self.start_node.get_x()-6,self.end_node.get_x()-6) and
            y >= min(self.start_node.get_y()+6,self.end_node.get_y()+6) and 
            y <= max(self.start_node.get_y()-6,self.end_node.get_y()-6)):
            return True
        return False
    
    def on_mouse_press(self, x, y, button, modifiers, player):
        if self.is_touching(x, y) and button == arcade.MOUSE_BUTTON_LEFT:
            self.build_road(player)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.is_touching(x, y) and self.width == 6:
            self.width += self.width * 0.5
        elif not self.is_touching(x, y):
            self.width = 6

    def draw(self):
        arcade.draw_line(self.start_node.get_x(), self.start_node.get_y(), 
                         self.end_node.get_x(), self.end_node.get_y(), self.color, self.width)
