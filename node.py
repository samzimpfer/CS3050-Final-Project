import arcade

class Node:

    def __init__(self, x=0, y=0, row=0, size=6):
        self.x = x
        self.y = y
        # for easy relation to position in board
        self.row = row
        self.connections = []
        self.adjacentTiles = []
        self.color = arcade.color.BLACK
        self.size = size
        self.building = "NONE"
        self.city = False
        

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_color(self, color):
        self.color = color

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def add_connection(self, n):
        self.connections.append(n)

    def add_adjacent_tile(self, t):
        self.adjacentTiles.append(t)

    def get_connections(self):
        return self.connections
    
    def get_adjacentTiles(self):
        return self.adjacentTiles

    def get_row(self):
        return self.row
    
    def build_town(self,player):
        if player.canBuildTown():
            return True
        return False
    
    def build_city(self,player):
        if (player.canBuildCity() and self.building == player and not self.city):
            self.city = True
            player.buildCity()
            return True
        return False
    
    def is_touching(self, x, y):
        if (x >= self.x - self.size and x <= self.x + self.size and 
            y >= self.y - self.size and y <= self.y + self.size):
            return True
        return False
    
    def on_mouse_press(self, x, y, button, modifiers, player):
        if self.is_touching(x, y):
            self.build_town(player)
            self.build_city(player)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)