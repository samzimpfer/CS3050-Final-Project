import arcade
from node import Node
from edge import Edge

# defines a board object that contains nodes representing appropriate positions for settlements
class Board:

    BOARD_SCALE_FACTOR = 0.92376 # height:width ratio of entire board
    Y_SPACING_FACTOR_A = 0.28867 # gap:tile-width ratio of first row
    Y_SPACING_FACTOR_B = 0.57735 # gap:tile-width ratio of second row

    ROW_SIZES = [3, 4, 4, 5, 5, 6, 6, 5, 5, 4, 4, 3] # number of nodes in each row
    NUM_ROWS = len(ROW_SIZES)


    # initialize the board centered at the given coordinates with a maximum width or height if specified
    def __init__(self, center_x, center_y, width=0, height=0):
        # board attributes
        self.center_x = center_x
        self.center_y = center_y
        self.x_pos = 0
        self.y_pos = 0
        self.width = 0
        self.height = 0
        self.tiles = arcade.SpriteList()
        self.tile_nodes = []

        # tile attributes
        self.x_spacing = 0

        #board components
        self.nodes = []
        self.edges = []

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
        while (row < Board.NUM_ROWS):
            row_node_list = []
            row_size = Board.ROW_SIZES[row]
            row_width = self.x_spacing * (row_size - 1)
            first_x = self.x_pos + ((self.width - row_width) // 2)

            for col in range(0, Board.ROW_SIZES[row]):
                x = first_x + (self.x_spacing * col)

                n = Node(x,y,row=row)
                row_node_list.append(n)
            self.nodes.append(row_node_list)

            if row % 2 == 0:
                y += (self.x_spacing * Board.Y_SPACING_FACTOR_A)
            else:
                y += (self.x_spacing * Board.Y_SPACING_FACTOR_B)
            
            row += 1
        self.generate_graph()
    
    # initializes a list of edges and assigns a start and end node
    def reset_edges(self):
        self.edges = []
        # uses the graph representation to create the edges between nodes
        for row in range(Board.NUM_ROWS - 1):
            for col in range(Board.ROW_SIZES[row]):
                for n in self.nodes[row][col].get_connections():
                    if n.get_row() > row:
                        self.edges.append(Edge(self.nodes[row][col],n))
    
    def reset_board(self):
        self.reset_nodes()
        self.reset_edges()
        self.reset_tiles()

    # creates a node that is located in the center of each tile
    def reset_tiles(self):
        # calculates the avg edge length to then find the center of each hexagon in the board
        avg_edge_length = 0
        for e in self.edges:
            avg_edge_length += e.edge_length()
        avg_edge_length = avg_edge_length / len(self.edges)

        # reference board-graph.pdf for this explanation
        # start at row index 3 as that is the first row containing the peak node of a tile
        for row in range(3,Board.NUM_ROWS):
            # same size as the previous row do not contain the top node of a tile so skip
            if Board.ROW_SIZES[row] == Board.ROW_SIZES[row-1]:
                continue
            for col in range(Board.ROW_SIZES[row]):
                # the center node is just the top node shifted down by the avg edge length
                pos_x = self.nodes[row][col].get_x()
                pos_y = self.nodes[row][col].get_y() - avg_edge_length
                # if the row index is less than 7 then the first and last nodes are not peaks
                if row < 7:
                    if col == 0 or col == Board.ROW_SIZES[row]-1:
                        continue
                    else:
                        self.tile_nodes.append(Node(pos_x,pos_y))
                # otherwise every node is a peak node
                else:
                    self.tile_nodes.append(Node(pos_x,pos_y))
        # add sprites to the SpriteList at the tile nodes
        for n in self.tile_nodes:
            sprite = arcade.Sprite("sprites/green_tile.png",scale=.6,
                                            center_x=n.get_x(),center_y=n.get_y(),angle=30)
            self.tiles.append(sprite)
                        

            
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
    
    # sets the size of the board and defines variables that can be used to track the 
    # position of the board
    def set_size(self, w, h):
        self.width = w
        self.height = h

        self.x_spacing = w / 5 # this will also be the width of tiles

        self.x_pos = self.center_x - (w // 2)
        self.y_pos = self.center_y - (h // 2)

        self.reset_board()

    
    # sets the size of the board according to a maximum width
    def set_max_width(self, w):
        self.set_size(w, w * Board.BOARD_SCALE_FACTOR)


    # sets the size of the board according to a maximum height
    def set_max_height(self, h):
        self.set_size(h / Board.BOARD_SCALE_FACTOR, h)


    # draw function for all components of the board 
    def draw(self):
        self.tiles.draw()
        for row in self.nodes:
            for n in row:
                n.draw()
        for e in self.edges:
            e.draw()
        for n in self.tile_nodes:
            n.draw()