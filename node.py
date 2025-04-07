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
        self.building = False
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
    
    def get_building(self):
        return self.building
    
    def is_city(self):
        return self.city
    
    # checks if there are any settlements within a road length from the node
    def has_space(self):
        for i in self.connections:
            if i.get_building():
                return False
        return True
    
    # checks if a road not build by the player runs through the node 
    # also checks that a player road touches the node
    def is_touching_road(self, board, player):
        other_player_road_count = 0
        player_can_build = False
        for node in self.connections:
            edge = board.get_edge(self, node)
            # checks if there are opposing roads touching this node
            if edge.get_road() and player.get_color() != edge.get_color():
                other_player_road_count += 1
            # checks if the player has a road touching the node
            if edge.get_road() and player.get_color() == edge.get_color():
                player_can_build = True
        
        if other_player_road_count > 1:
            return False
        return player_can_build
        
    # builds a town 
    def build_settlement(self, player, board):
        if self.has_space() and self.is_touching_road(board, player) and player.can_build_settlement():
            self.color = player.get_color()
            self.building = player
            player.build_settlement()
            return True
        return False

    
    def build_city(self,player):
        if (player.can_build_city() and self.building == player and not self.city):
            self.city = True
            player.build_city()
            return True
        return False
    
    # calculates if the x y point is touching the drawn area of the node
    def is_touching(self, x, y):
        if (x >= self.x - self.size and x <= self.x + self.size and 
            y >= self.y - self.size and y <= self.y + self.size):
            return True
        return False
    
    # checks if there was a mouse click on the node
    def on_mouse_press(self, x, y, button, modifiers, player, board):
        return_flag = False
        if self.is_touching(x, y) and button == arcade.MOUSE_BUTTON_LEFT:
            return_flag = self.build_settlement(player, board)
            if self.build_city(player):
                return_flag = True
        return return_flag

    # checks if the mouse has stopped on the node after moving
    def on_mouse_motion(self, x, y):
        if self.is_touching(x, y) and self.size == self.originalSize:
            self.size = self.originalSize * 1.5
        elif not self.is_touching(x, y): 
            self.size = self.originalSize

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)