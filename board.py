from node import Node

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

        # tile attributes
        self.x_spacing

        #board components
        self.nodes = []

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
            row_size = Board.ROW_SIZES[row]
            row_width = self.x_spacing * (row_size - 1)
            first_x = self.x_pos + ((self.width - row_width) // 2)

            for col in range(0, Board.ROW_SIZES[row]):
                x = first_x + (self.x_spacing * col)

                n = Node(x, y)
                self.nodes.append(n)

            if row % 2 == 0:
                y += (self.x_spacing * Board.Y_SPACING_FACTOR_A)
            else:
                y += (self.x_spacing * Board.Y_SPACING_FACTOR_B)

            row += 1


    # sets the size of the board and defines variables that can be used to track the position of the board
    def set_size(self, w, h):
        self.width = w
        self.height = h

        self.x_spacing = w / 5 # this will also be the width of tiles

        self.x_pos = self.center_x - (w // 2)
        self.y_pos = self.center_y - (h // 2)

        self.reset_nodes()

    
    # sets the size of the board according to a maximum width
    def set_max_width(self, w):
        self.set_size(w, w * Board.BOARD_SCALE_FACTOR)


    # sets the size of the board according to a maximum height
    def set_max_height(self, h):
        self.set_size(h / Board.BOARD_SCALE_FACTOR, h)


    def draw(self):
        for n in self.nodes:
            n.draw()