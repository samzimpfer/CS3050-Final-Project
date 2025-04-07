import arcade

class Tile:
    def __init__(self, x=0, y=0, size=6):
        self.x = x
        self.y = y
        self.number = 0
        self.connections = []
        self.nodes = []
        self.color = arcade.color.BLACK
        self.size = size  # size of the node that is drawn
        self.originalSize = size  # size of the node with no effects
        self.resource = None
        self.robber = False
        self.number = None

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_color(self, color):
        self.color = color

    def set_resource(self, resource):
        self.resource = resource

    def set_robber(self, has_robber):
        self.robber = has_robber

    def set_number(self, number):
        self.number = number

    def set_nodes(self, new_nodes):
        self.nodes = new_nodes

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def add_connection(self, n):
        self.connections.append(n)

    def get_nodes(self):
        return self.nodes

    def get_connections(self):
        return self.connections

    def get_resource(self):
        return self.resource

    def has_robber(self):
        return self.robber

    def get_number(self):
        return self.number

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)