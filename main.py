"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from board import Board

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Starting Template"


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.WHITE

        # If you have sprite lists, you should create them here,
        # and set them to None

        # centers the board on the canvas with a 20px margin
        # change these for a different positioning method
        margin = 20

        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        board_height = WINDOW_HEIGHT - (margin * 2)

        self.board = Board(center_x, center_y, height=board_height)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.board.draw()
        self.board.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.board.on_mouse_press(x, y, button, modifiers)
        pass

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