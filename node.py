import arcade

class Node:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.size = 6

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        arcade.draw_point(self.x, self.y, arcade.color.BLACK, self.size)