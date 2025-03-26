"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from enum import Enum
from gameobjects import *
import tkinter as tk

from board import Board
from player import Player

class GameState(Enum):
    SETUP = 0
    ROLL = 1
    GET_RESOURCES = 2
    TRADE = 3
    BUILD = 4
    WAITING = 5

screen_width, screen_height = arcade.get_display_size()
root = tk.Tk()
root.withdraw()
usable_width = root.winfo_screenwidth()
usable_height = root.winfo_screenheight()
print(usable_width, usable_height)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Settlers of Catan"

PLAYER_COLORS = [arcade.color.BLUE, arcade.color.GREEN, arcade.color.RED, arcade.color.YELLOW]

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.margin = 20
        self.logo_space = WINDOW_HEIGHT * 0.18 - self.margin
        self.board_space = WINDOW_HEIGHT - self.logo_space - (self.margin * 3)

        self.num_players = 4

        self.sprites = arcade.SpriteList()

        self.background = arcade.Sprite("sprites/background.png")
        self.background.width = WINDOW_WIDTH
        self.background.height = WINDOW_HEIGHT
        self.background.center_x = WINDOW_WIDTH // 2
        self.background.center_y = WINDOW_HEIGHT // 2
        self.sprites.append(self.background)

        self.logo = arcade.Sprite("sprites/logo.png")
        scale = self.logo_space / self.logo.height
        self.logo.scale = (scale, scale)
        self.logo.center_x = WINDOW_WIDTH // 2
        self.logo.center_y = WINDOW_HEIGHT - self.margin - (self.logo_space // 2)
        self.sprites.append(self.logo)

        board_center_x = WINDOW_WIDTH // 2
        board_center_y = (self.board_space // 2) + self.margin
        self.board = Board(board_center_x, board_center_y, height=self.board_space)

        # used for sizing bank and active player representation
        self.component_width = (WINDOW_WIDTH - self.board.width + self.board.x_spacing) // 2
        self.component_height = self.logo_space + self.margin + (self.board.x_spacing * 1)
        self.other_player_width = (WINDOW_WIDTH - self.board.width) // 4
        self.other_player_height = (WINDOW_HEIGHT - self.component_height - (self.margin * 5)) // (self.num_players - 1)

        # TODO: initialize bank

        self.players = []
        for i in range(self.num_players):
            # TODO: also pass bank into Player constructors
            p = Player(PLAYER_COLORS[i])
            self.players.append(p)

        self.current_state = GameState.SETUP
        self.active_player_index = 0


    def on_draw(self):
        """
        Render the screen.
        """

        self.clear()
        self.sprites.draw()
        self.board.draw()

        # component placeholders TODO: replace these with actual component on_draw() functions
        # bank
        arcade.draw_lrbt_rectangle_filled(WINDOW_WIDTH - self.component_width, WINDOW_WIDTH, WINDOW_HEIGHT - self.component_height, WINDOW_HEIGHT, arcade.color.GRAY)

        # active player
        self.players[self.active_player_index].on_draw(True, 0, self.component_width, WINDOW_HEIGHT - self.component_height, WINDOW_HEIGHT - self.margin)

        i = 2 # iterate through inactive player positions
        p = self.active_player_index + 1 # iterate through inactive players
        if p >= self.num_players:
            p = 0
        while (p != self.active_player_index):
            self.players[p].on_draw(False, 0, self.other_player_width, self.margin + (i * (self.margin + self.other_player_height)), (i + 1) * (self.margin + self.other_player_height))

            i -= 1
            p += 1
            if p >= self.num_players:
                p = 0


    def on_update(self, delta_time: float):
        # manage game state
        if (self.current_state == GameState.ROLL):
            # roll() ?
            self.current_state = GameState.WAITING
        elif (self.current_state == GameState.GET_RESOURCES):
            # maybe unneeded depending on how roll is handled
            pass
        elif (self.current_state == GameState.TRADE):
            pass
        elif (self.current_state == GameState.BUILD):
            # board.build ?
            self.current_state = GameState.WAITING

    def on_mouse_press(self, x, y, button, modifiers):
        self.board.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.board.on_mouse_move(x, y, dx, dy)

def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()

    global Bank
    global GameDevCards

    Bank = Bank()
    GameDevCards = DevCardStack()

if __name__ == "__main__":
    main()