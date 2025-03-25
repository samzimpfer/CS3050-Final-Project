"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from enum import Enum

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
WINDOW_WIDTH = screen_width - 100
WINDOW_HEIGHT = screen_height - 100
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

        self.sprites = arcade.SpriteList()

        self.background = arcade.Sprite("sprites/background.png")
        self.background.width = WINDOW_WIDTH
        self.background.height = WINDOW_HEIGHT
        self.background.center_x = WINDOW_WIDTH // 2
        self.background.center_y = WINDOW_HEIGHT // 2
        self.sprites.append(self.background)

        self.margin = 20
        self.logo_space = WINDOW_HEIGHT * 0.2
        self.board_space = WINDOW_HEIGHT - self.logo_space - self.margin

        self.logo = arcade.Sprite("sprites/logo.png")
        scale = self.logo_space / self.logo.height
        self.logo.scale = (scale, scale)
        self.logo.center_x = WINDOW_WIDTH // 2
        self.logo.center_y = WINDOW_HEIGHT - (self.logo_space // 2)
        self.sprites.append(self.logo)

        board_center_x = WINDOW_WIDTH // 2
        board_center_y = (self.board_space // 2) + self.margin
        self.board = Board(board_center_x, board_center_y, height=self.board_space)
        # TODO: initialize bank

        self.num_players = 4
        self.players = []
        for i in range(self.num_players):
            # TODO: also pass bank into Player constructors
            p = Player(PLAYER_COLORS[i])
            self.players.append(p)

        self.currentState = GameState.SETUP


    def on_draw(self):
        """
        Render the screen.
        """

        self.clear()
        self.sprites.draw()
        self.board.draw()


    def on_update(self, delta_time: float):
        # manage game state
        if (self.currentState == GameState.ROLL):
            # roll() ?
            self.currentState = GameState.WAITING
        elif (self.currentState == GameState.GET_RESOURCES):
            # maybe unneeded depending on how roll is handled
            pass
        elif (self.currentState == GameState.TRADE):
            pass
        elif (self.currentState == GameState.BUILD):
            # board.build ?
            self.currentState = GameState.WAITING

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


if __name__ == "__main__":
    main()