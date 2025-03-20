import arcade

class Node:

    def __init__(self, x=0, y=0, row=0):
        self.x = x
        self.y = y
        # for easy relation to position in board
        self.row = row
        self.connections = []
        self.adjacentTiles = []
        self.color = arcade.color.BLACK
        self.size = 6
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
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            distance = ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5
            if distance <= 10:
                self.button_color = arcade.color.GREEN
    
    def build_city(self,player):
        if (player.canBuildCity() and self.building == player and not self.city):
            self.city = True
            player.buildCity()
            return True
        return False

    def draw(self):
        arcade.draw_point(self.x, self.y, self.color, self.size)