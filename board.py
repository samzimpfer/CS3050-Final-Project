import arcade
from player import Player
from node import Node
from edge import Edge
from tile import Tile
from gameobjects import *
import random
from robot import Robot

# defines a board object that contains nodes representing appropriate positions for settlements
class Board:

    BOARD_SCALE_FACTOR = 0.92376 # height:width ratio of entire board
    Y_SPACING_FACTOR_A = 0.28867 # gap:tile-width ratio of first row
    Y_SPACING_FACTOR_B = 0.57735 # gap:tile-width ratio of second row (also side-length:tile-width ratio)

    ROW_SIZES = [3, 4, 4, 5, 5, 6, 6, 5, 5, 4, 4, 3] # number of nodes in each row
    NUM_ROWS = len(ROW_SIZES)




    # initialize the board centered at the given coordinates with a maximum width or height if specified
    def __init__(self, center_x, center_y, players, width=0, height=0):
        # board attributes
        self.center_x = center_x
        self.center_y = center_y
        self.x_pos = 0
        self.y_pos = 0
        self.width = 0
        self.height = 0
        self.tiles = arcade.SpriteList()
        self.tile_nodes = []
        self.resources = [Resource.WHEAT, Resource.WHEAT, Resource.WHEAT, Resource.WHEAT, Resource.WOOD, Resource.WOOD, Resource.WOOD, Resource.WOOD, Resource.SHEEP, Resource.SHEEP, Resource.SHEEP, Resource.SHEEP, Resource.STONE, Resource.STONE, Resource.STONE, Resource.BRICK, Resource.BRICK, Resource.BRICK, 'desert']
        self.numbers = [5, 2, 6, 8, 10, 9, 3, 3, 11, 4, 8, 4, 6, 5, 10, 11, 12, 9]
        self.players = players
        self.robber_tile = None # the tile that has the robber on it        

        # tile attributes
        self.x_spacing = 0 # this is the tile width

        #board components
        self.nodes = []
        self.edges = []
        self.avg_edge_length = 0

        # setup
        if (width != 0):
            self.set_max_width(width)
        elif (height != 0):
            self.set_max_height(height)
        else:
            print("Error creating board: no width of height given")


    # initializes a list of nodes and assigns each a position within the board
    def reset_nodes(self):
        self.nodes = []
        row = 0
        y = self.y_pos
        while (row < Board.NUM_ROWS): # iterates through each row of nodes to be drawn
            row_node_list = []
            row_size = Board.ROW_SIZES[row]
            row_width = self.x_spacing * (row_size - 1)
            first_x = self.x_pos + ((self.width - row_width) // 2) # defines the position of the leftmost node in the row

            for col in range(0, Board.ROW_SIZES[row]): # creates a node at each appropriate column in the row
                x = first_x + (self.x_spacing * col)

                n = Node(x,y,row=row, col=col)
                row_node_list.append(n)
            self.nodes.append(row_node_list)

            # increments the row spacing according to hexagon geometry
            if row % 2 == 0:
                y += (self.x_spacing * Board.Y_SPACING_FACTOR_A)
            else:
                y += (self.x_spacing * Board.Y_SPACING_FACTOR_B)
            
            row += 1

        # generates a graph to keep track of adjacent nodes
        self.generate_graph()

    # calculates the avg edge length to help with placement of tiles and relating to other objects
    def calc_avg_edge_length(self):
        self.avg_edge_length = 0
        for e in self.edges:
            self.avg_edge_length += e.edge_length()
        self.avg_edge_length = self.avg_edge_length / len(self.edges)
    
    # initializes a list of edges and assigns a start and end node
    def reset_edges(self):
        self.edges = []
        # uses the graph representation to create the edges between nodes
        for row in range(Board.NUM_ROWS - 1):
            for col in range(Board.ROW_SIZES[row]):
                for n in self.nodes[row][col].get_connections():
                    if n.get_row() > row:
                        self.edges.append(Edge(self.nodes[row][col],n))
        self.calc_avg_edge_length()
    
    def reset_board(self):
        self.reset_nodes()
        self.reset_edges()
        self.reset_tiles()

    # creates a node that is located in the center of each tile
    def reset_tiles(self):
        # reference board-graph.pdf for this explanation
        # start at row index 3 as that is the first row containing the peak node of a tile
        for row in range(3,Board.NUM_ROWS):
            # rows of the same size as the previous row do not contain the top node of a tile so skip
            if Board.ROW_SIZES[row] == Board.ROW_SIZES[row-1]:
                continue
            for col in range(Board.ROW_SIZES[row]):
                # the center node is just the top node shifted down by the avg edge length
                pos_x = self.nodes[row][col].get_x()
                pos_y = self.nodes[row][col].get_y() - self.avg_edge_length
                # if the row index is less than 7 then the first and last nodes are not peaks
                if row < 7:
                    if col == 0 or col == Board.ROW_SIZES[row]-1:
                        continue
                    else:
                        self.tile_nodes.append(Tile(pos_x,pos_y,size=20))
                # otherwise every node is a peak node
                else:
                    self.tile_nodes.append(Tile(pos_x,pos_y,size=20))

        #assign resources to the tiles
        random.shuffle(self.resources)
        for index, resource in enumerate(self.resources):
            self.tile_nodes[index].set_resource(resource)
        # add sprites to the SpriteList at the tile nodes depending on resource
        #also set numbers
        seen_desert = False
        for n in self.tile_nodes:
            self.set_tile_edge_nodes(n)
            if n.get_resource() != 'desert':
                if not seen_desert:
                    n.set_number(self.numbers[self.tile_nodes.index(n)])
                else:
                    n.set_number(self.numbers[self.tile_nodes.index(n) - 1])
            if n.get_resource() == Resource.WOOD:
                #testing scale, old value .65
                sprite = arcade.Sprite("sprites/green_tile.png",scale=self.x_spacing/180,
                                                center_x=n.get_x(),center_y=n.get_y())
                self.tiles.append(sprite)
            elif n.get_resource() == Resource.WHEAT:
                sprite = arcade.Sprite("sprites/wheat_tile.png", scale=self.x_spacing/180,
                                       center_x=n.get_x(), center_y=n.get_y())
                self.tiles.append(sprite)
            elif n.get_resource() == Resource.SHEEP:
                sprite = arcade.Sprite("sprites/sheep_tile.png", scale=self.x_spacing/180,
                                       center_x=n.get_x(), center_y=n.get_y())
                self.tiles.append(sprite)
            elif n.get_resource() == Resource.STONE:
                sprite = arcade.Sprite("sprites/ore_tile.png", scale=self.x_spacing/180,
                                       center_x=n.get_x(), center_y=n.get_y())
                self.tiles.append(sprite)
            elif n.get_resource() == Resource.BRICK:
                sprite = arcade.Sprite("sprites/brick_tile.png", scale=self.x_spacing/180,
                                       center_x=n.get_x(), center_y=n.get_y())
                self.tiles.append(sprite)
            else:
                sprite = arcade.Sprite("sprites/desert_tile.png", scale=self.x_spacing/180,
                                       center_x=n.get_x(), center_y=n.get_y())
                self.tiles.append(sprite)
                seen_desert = True

        self.find_touching_tiles()

    # finds the nodes that are touching/make up the edge of a tile 
    def set_tile_edge_nodes(self, tile):
        edge_nodes = []
        for row in self.nodes:
            for node in row:
                # the tile center node(pos) should be within one edge length from any node that is touching the tile
                # this makes a range and if pos is in that range that tile is touching the node
                node_x_range = [node.get_x() - self.avg_edge_length, node.get_x() + self.avg_edge_length]
                node_y_range = [node.get_y() - self.avg_edge_length, node.get_y() + self.avg_edge_length]
                if tile.get_x() >= node_x_range[0] and tile.get_x() <= node_x_range[1]:
                    if tile.get_y() >= node_y_range[0] and tile.get_y() <= node_y_range[1]:
                        edge_nodes.append(node)

        tile.set_nodes(edge_nodes)

            
    # adds nodes that share an edge to the connections list within each node
    # reference board-graph.pdf for this explanation
    def generate_graph(self):
        for row in range(Board.NUM_ROWS-1):
            for col in range(Board.ROW_SIZES[row]):
                # when the number of nodes per row is increasing nodes on the far ends have two edges
                if len(self.nodes[row+1]) > len(self.nodes[row]):
                    self.undirected_edge(self.nodes[row][col],self.nodes[row+1][col])
                    self.undirected_edge(self.nodes[row][col],self.nodes[row+1][col+1])
                # when the number of nodes per row is decreasing nodes on the far ends have one edge
                # and the edge is to the right for the far left and to the left for the far right
                elif len(self.nodes[row+1]) < len(self.nodes[row]):
                    if col != 0:
                        self.undirected_edge(self.nodes[row][col],self.nodes[row+1][col-1])
                    if col != len(self.nodes[row])-1:
                        self.undirected_edge(self.nodes[row][col],self.nodes[row+1][col])
                # when the number of nodes per row is the same it is one to one for all nodes
                else:
                    self.undirected_edge(self.nodes[row][col],self.nodes[row+1][col])
                    
    # helper function so that edges are symmetric/undirected
    def undirected_edge(self,n1,n2):
        n1.add_connection(n2)
        n2.add_connection(n1)

    # populates the adjacentTiles list in for each node in nodes
    def find_touching_tiles(self):
        for row in self.nodes:
            for node in row:
                for pos in self.tile_nodes:
                    # the tile center node(pos) should be within one edge length from any node that is touching the tile
                    # this makes a range and if pos is in that range that tile is touching the node
                    node_x_range = [node.get_x() - self.avg_edge_length, node.get_x() + self.avg_edge_length]
                    node_y_range = [node.get_y() - self.avg_edge_length, node.get_y() + self.avg_edge_length]
                    if pos.get_x() >= node_x_range[0] and pos.get_x() <= node_x_range[1]:
                        if pos.get_y() >= node_y_range[0] and pos.get_y() <= node_y_range[1]:
                            node.add_adjacent_tile(pos)
                            pos.set_color(arcade.color.WHITE)
        #self.test_find_touching_tiles()
        return
    
    # most tiles should have 3 adjacent tiles this will print the edges cases need to check manually
    # using board-graph.pdf
    def test_find_touching_tiles(self):
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[x])):
                if len(self.nodes[x][y].get_adjacentTiles()) != 3:
                    print(f'{[x,y]} has {len(self.nodes[x][y].get_adjacentTiles())} adjacent tiles')
    
    # sets the size of the board and defines variables that can be used to track the 
    # position of the board
    def set_size(self, w, h):
        self.width = w
        self.height = h

        self.x_spacing = w / 5 # this will also be the width of tiles

        self.x_pos = self.center_x - (w // 2)
        self.y_pos = self.center_y - (h // 2)

        self.reset_board()

    # allocates resources for the start turn
    def allocate_resources_start(self, player):
        for row in self.nodes:
            for node in row:
                if node.get_building() == player:
                    for tile in node.get_adjacent_tiles():
                        if tile.get_resource() != "desert":
                            player.add_resources({tile.get_resource() : 1})
    
    # gives out resources to the players that have buildings touching a tile with the number rolled
    def allocate_resources(self, roll):
        target_tiles = [tile for tile in self.tile_nodes if tile.get_number() == roll and not tile.has_robber()]
        for tile in target_tiles:
            for node in tile.get_nodes():
                if node.get_building():
                    player = node.get_building()
                    # adds an extra resource if the building is a city
                    if node.is_city():
                        player.add_resources({tile.get_resource() : 1 })
                    player.add_resources({tile.get_resource() : 1 })
                

    # main function that calls the sub functions on all players
    # TODO: Fix the path_length function recursion is not work right 
    def find_longest_road(self):
        for player in self.players:
            nodes_of_interest = self.find_nodes_of_intrest(player)
            segments = self.find_segment_lengths(nodes_of_interest, player.get_roads())

            endpoints = self.find_endpoints(player)
            lengths = []
            for segment in segments:
                if segment[0] in endpoints:
                    segments_2 = segments.copy()
                    lengths_2 = (self.construct_longest_path(segment[0], segments_2))
                    for length in lengths_2:
                        lengths.append(length)
            if lengths != []:
                longest_road = max(lengths)
            else:
                longest_road = 0
            player.set_longest_road_value(longest_road)
        for player in self.players:
            max_len = 0
            changes = []
            if player.get_longest_road_value() > 5 and player.get_longest_road_value() > max_len:
                max_len = player.get_longest_road_value()
                changes.append(player)
        if changes != []:
            for player in self.players:
                player.set_longest_road(False)
            changes[-1].set_longest_road(True)



    #connect segments starting from a seed node
    def construct_longest_path(self, seed, segments, length=0, lengths=None):
        if lengths is None:
            lengths = []
        for segment in segments:
            if segment[0] == seed:
                length += segment[1]
                lengths.append(length)
                segments.pop(segments.index(segment))
                segments.pop(segments.index([segment[2], segment[1], segment[0]]))
                return self.construct_longest_path(segment[2],segments, length, lengths)
        return lengths

    def find_endpoints(self, player):
        endpoints = []
        roads = player.get_roads()
        for node in roads:
            count = len([connection for connection in node.get_connections() if connection in roads])
            # if a node has one road connection it is an endpoint
            if count == 1:
                endpoints.append(node)
        return endpoints

    #finds all nodes that are either an endpoint or an intersection
    def find_nodes_of_intrest(self, player):
        nodes_of_intrest = []
        roads = player.get_roads()
        for node in roads:
            count = len([connection for connection in node.get_connections() if connection in roads])
            # if a node does not have two road connections then it is either an endpoint or an intersection
            if count != 2:
                nodes_of_intrest.append(node)
        return nodes_of_intrest
    
    # finds the lengths of all segments which is just a path between two nodes_of_intrest
    def find_segment_lengths(self, nodes_of_importance, roads):
        checked_segments = []
        for node in nodes_of_importance:
            connections = [connection for connection in node.get_connections() if connection in roads]
            for connection in connections:
                path = self.path_length(node, connection, nodes_of_importance, roads)
                checked_segments.append([path[0],len(path) - 1,path[-1]])
        return checked_segments

    # finds the length of a path given a direction(the next param) until the next node_of_intrest
    # still WIP
    def path_length(self, start, next, nodes_of_importance, roads, path=None):
        if path is None:
            path = [start]
        if next in nodes_of_importance:
            path.append(next)
            return path
        else:
            path.append(next)
            new_next = None
            for node in next.get_connections():
                if node in roads and node != start:
                    new_next = node
            return self.path_length(next, new_next, nodes_of_importance, roads, path)


    # returns the edge with the matching start_node and end_node
    def get_edge(self, start_node, end_node):
        for edge in self.edges:
            if edge.get_start_node() == start_node or edge.get_start_node() == end_node:
                if edge.get_end_node() == start_node or edge.get_end_node() == end_node:
                    return edge
        return 
    
    # sets the size of the board according to a maximum width
    def set_max_width(self, w):
        self.set_size(w, w * Board.BOARD_SCALE_FACTOR)


    # sets the size of the board according to a maximum height
    def set_max_height(self, h):
        self.set_size(h / Board.BOARD_SCALE_FACTOR, h)

    # calls on_mouse_press on all objects that are on the board and interactable
    # start turn = -1 indicates regular gameplay
    # start turn = 0 indicates the first start turn
    # start turn = 1 indicates the second start turn
    def on_mouse_press(self, x, y, button, player, can_build_road=True, can_build_settlement=True, can_rob=False, start_turn=-1):
        did_build_settlement = False
        did_build_road = False

        if can_build_settlement:
            for row in self.nodes:
                for node in row:
                    if node.on_mouse_press(x, y, button, player, self, (start_turn >= 0)):
                        did_build_settlement = True

        if can_build_road:
            for edge in self.edges:
                if edge.on_mouse_press(x, y, button, player, (start_turn >= 0)):
                    did_build_road = True

        if can_rob:
            for tile in self.tile_nodes:
                robber_location = tile.on_mouse_press(x, y, button)
                if robber_location:
                    if self.robber_tile:
                        self.robber_tile.set_robber(False)
                    self.robber_tile = robber_location
                    return True

        if start_turn == 0 and did_build_settlement:
            self.allocate_resources_start(player)

        return did_build_settlement or did_build_road

    # calls on_mouse_motion on all objects that should have a hover effect
    def on_mouse_move(self, x, y):
        for edge in self.edges:
            edge.on_mouse_motion(x, y)
        for row in self.nodes:
            for node in row:
                node.on_mouse_motion(x,y)

    # draw function for all components of the board 
    def draw(self):
        self.tiles.draw()
        for e in self.edges:
            e.draw()
        for row in self.nodes:
            for n in row:
                n.draw()
        for n in self.tile_nodes:
            n.draw()
            if n.get_resource() != 'desert':
                arcade.draw_text(str(n.get_number()), n.get_x(), n.get_y(),arcade.color.BLACK,
                                 20, anchor_x='center', anchor_y='center')

    def get_nodes(self):
        return self.nodes
    
    def get_tiles(self):
        return self.tile_nodes
    
    def bot_build_settlement(self, node, player, start_turn, is_first=False):
        node.build_settlement(player, self, start_turn=start_turn)
        if start_turn and is_first:
            self.allocate_resources_start(player)

    def bot_build_road(self, edge, player, start_turn):
        edge.build_road(player, start_turn=start_turn)
        
