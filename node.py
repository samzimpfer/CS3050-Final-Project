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
        self.size = size# size of the node that is drawn
        self.originalSize = size# size of the node with no effects
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
    
    # calculates if the x y point is touching the drawn area of the node
    def is_touching(self, x, y):
        if (x >= self.x - self.size and x <= self.x + self.size and 
            y >= self.y - self.size and y <= self.y + self.size):
            return True
        return False
    
    # checks if there was a mouse click on the node
    def on_mouse_press(self, x, y, button, modifiers, player):
        if self.is_touching(x, y) and button == arcade.MOUSE_BUTTON_LEFT:
            self.build_town(player)
            self.build_city(player)

    # checks if the mouse has stopped on the node after moving
    def on_mouse_motion(self, x, y):
        if self.is_touching(x, y) and self.size == self.originalSize:
            self.size = self.originalSize * 1.5
        elif not self.is_touching(x, y): 
            self.size = self.originalSize

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)