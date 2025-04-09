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

from board import Board
from player import Player
from dice import Dice

screen_width, screen_height = arcade.get_display_size()
WINDOW_WIDTH = screen_width - 100
WINDOW_HEIGHT = screen_height - 100
WINDOW_TITLE = "Settlers of Catan"

PLAYER_COLORS = [arcade.color.BLUE, arcade.color.GREEN, arcade.color.RED, arcade.color.YELLOW]

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # general sizing fields for components
        self.margin = 20
        self.logo_space = WINDOW_HEIGHT * 0.18 - self.margin
        self.board_space = WINDOW_HEIGHT - self.logo_space - (self.margin * 3)

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

        # TODO: take these out
        # these are here only so board can create a player class for testing. More organized to have them below
        self.bank = Bank()
        self.dev_card_stack = DevCardStack()
        Player.bank = self.bank
        Player.dev_card_stack = self.dev_card_stack
        Player.finish_turn_function = self.next_player_turn

        board_center_x = WINDOW_WIDTH // 2
        board_center_y = (self.board_space // 2) + self.margin
        self.board = Board(board_center_x, board_center_y, height=self.board_space)

        # more sizing fields used for bank, dice, and player representations
        self.num_players = 4

        self.component_width = (WINDOW_WIDTH - self.board.width + self.board.x_spacing) // 2
        self.component_height = self.logo_space + self.margin + self.board.x_spacing
        self.other_player_width = (WINDOW_WIDTH - self.board.width) * 0.4
        self.other_player_height = (WINDOW_HEIGHT - self.component_height - (self.margin * 5)) // (self.num_players - 1)
        dice_width = (WINDOW_WIDTH - self.board.width - (self.margin * 2)) // 2
        dice_height = dice_width * 0.52
        dice_x = WINDOW_WIDTH - (self.margin * 2) - (dice_width // 2)
        dice_y = (self.margin * 2) + (dice_height // 2)


        #longest road/army card stuff
        self.longest_road_sprite = arcade.Sprite("sprites/longest_road_card.png")
        self.longest_road_sprite.center_x = WINDOW_WIDTH - ((5 * self.component_width) / 6)
        self.longest_road_sprite.center_y = WINDOW_HEIGHT - (self.component_height / 4)
        self.longest_road_sprite.width = self.component_width / 3
        self.longest_road_sprite.height = self.component_height / 2

        self.largest_army_sprite = arcade.Sprite("sprites/largest_army_card.png")
        self.largest_army_sprite.center_x = WINDOW_WIDTH - ((5 * self.component_width) / 6)
        self.largest_army_sprite.center_y = WINDOW_HEIGHT - ((3 * self.component_height) / 4)
        self.largest_army_sprite.width = self.component_width / 3
        self.largest_army_sprite.height = self.component_height / 2

        self.dev_card_sprite = arcade.Sprite("sprites/dev_card_img.png")
        self.dev_card_sprite.center_x = WINDOW_WIDTH - (self.component_width / 4)
        self.dev_card_sprite.center_y = WINDOW_HEIGHT - (self.component_height / 2)
        self.dev_card_sprite.width = self.component_width / 2
        self.dev_card_sprite.height = self.component_height

        # initialize game objects
        #self.bank = Bank()
        #self.dev_card_stack = DevCardStack()
        self.dice = Dice(dice_x, dice_y, dice_width, dice_height)

        self.players = []
        for i in range(self.num_players):
            p = Player(PLAYER_COLORS[i])
            #setting the bank/dev cards
            p.bank = self.bank
            p.dev_card_stack = self.dev_card_stack
            p.dev_card_stack_button_params = [
                self.dev_card_sprite.center_x,
                self.dev_card_sprite.center_y,
                self.dev_card_sprite.width,
                self.dev_card_sprite.height,
            ]
            #testing card stuff
            p.set_longest_road(True)
            p.set_largest_army(True)
            self.players.append(p)

        #Player.bank = self.bank
        #Player.dev_card_stack = self.dev_card_stack

        mouse_size = 5
        self.mouse_sprite = arcade.SpriteSolidColor(mouse_size, mouse_size, color=(0, 0, 0, 150))

        # gameplay fields
        self.current_state = None
        self.active_player_index = 0
        self.active_player = None

        # start game
        self.reset()

    def reset(self):
        self.current_state = GameState.ROLL
        self.active_player_index = -1
        self.next_player_turn()

    def next_player_turn(self):
        # cycle active player
        self.active_player_index += 1
        if self.active_player_index >= self.num_players:
            self.active_player_index = 0
        self.active_player = self.players[self.active_player_index]

        # set active player position
        self.active_player.set_active_player(True)
        self.active_player.set_pos(0, self.component_width,
                                   WINDOW_HEIGHT - self.component_height,
                                   WINDOW_HEIGHT - self.margin)

        # set inactive player positions
        i = 2  # iterate through inactive player positions
        p = self.active_player_index + 1  # iterate through inactive players
        while (i >= 0):
            if p >= self.num_players:
                p = 0
            self.players[p].set_active_player(False)
            self.players[p].set_pos(0, self.other_player_width,
                                    self.margin + (i * (self.margin + self.other_player_height)),
                                    (i + 1) * (self.margin + self.other_player_height))
            p += 1
            i -= 1

        self.current_state = GameState.ROLL

    def check_winner(self):
        for p in self.players:
            if p.get_points() >= 11:
                print(f"{p.get_color()} player wins!")

    def on_draw(self):
        self.clear()
        self.sprites.draw()
        self.board.draw()
        self.dice.on_draw()



        #bank won't be drawn, only dev card stack
        arcade.draw_lrbt_rectangle_filled(WINDOW_WIDTH - self.component_width, WINDOW_WIDTH, WINDOW_HEIGHT - self.component_height, WINDOW_HEIGHT, arcade.color.GRAY)
        arcade.draw_sprite(self.dev_card_sprite)
        for p in self.players:
            p.on_draw()
            if p.has_longest_road:
                arcade.draw_sprite(self.longest_road_sprite)
            if p.has_largest_army:
                arcade.draw_sprite(self.largest_army_sprite)
            #p.draw_player_resources()
            #p.BuyDevCard()
            #p.draw_view_dev_cards()

    def on_update(self, delta_time: float):
        for p in self.players:
            p.set_state(self.current_state)

        # manage game state
        if self.current_state == GameState.ROLL:
            self.dice.on_update(delta_time)

            if self.dice.ready:
                # handle roll sum
                # TODO: call board function to distribute resources based on dice roll
                roll_value = self.dice.get_sum_and_reset()
                print(f"Roll: {roll_value}") # replace with board.distribute_resources(self.dice.sum)
                if roll_value == 7:
                    self.current_state = GameState.ROBBER
                else:
                    self.board.allocate_resources(roll_value)
                    self.current_state = GameState.TRADE # TODO: change to GameState.TRADE once trading is developed

        self.check_winner()

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

        self.active_player.on_mouse_press(self.mouse_sprite)

        if self.current_state == GameState.ROLL:
            self.dice.on_mouse_press(self.mouse_sprite)
            
        elif self.current_state == GameState.TRADE or self.current_state == GameState.BUILD:
            if self.board.on_mouse_press(x, y, button, self.active_player):
                self.current_state = GameState.BUILD


        elif self.current_state == GameState.ROBBER:
            did_rob = self.board.on_mouse_press(x, y, button, self.active_player, can_build=False, can_rob=True)
            if did_rob:
                self.current_state = GameState.TRADE
            
                

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

        self.board.on_mouse_move(x, y)

        self.active_player.on_mouse_motion(self.mouse_sprite)

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()