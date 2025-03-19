import arcade

class Node:

    def __init__(self, x=0, y=0, row=0):
        self.x = x
        self.y = y
        # for easy relation to position in board
        self.row = row
        self.connections = []
        self.size = 6
        self.building = "NONE"
        self.city = False
        

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def add_connection(self, n):
        self.connections.append(n)

    def get_connections(self):
        return self.connections

    def get_row(self):
        return self.row
    
    def build_town(self,player):
        return
    
    def build_city(self,player):
        return 

    def draw(self):
        arcade.draw_point(self.x, self.y, arcade.color.BLACK, self.size)