"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
from encodings import search_function
from idlelib.run import install_recursionlimit_wrappers

from gameobjects import *
from board import Board
from player import *
from dice import Dice
from robot import Robot
from robot import Moves
import arcade


screen_width, screen_height = arcade.get_display_size()
WINDOW_WIDTH = screen_width - 100
WINDOW_HEIGHT = screen_height - 100
WINDOW_TITLE = "Settlers of Catan"

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

        self.zero_button = Button("0")
        self.one_button = Button("1")
        self.two_button = Button("2")
        self.three_button = Button("3")
        self.four_button = Button("4")

        # TODO: take these out
        # these are here only so board can create a player class for testing. More organized to
        # have them below
        self.bank = Bank()
        self.dev_card_stack = DevCardStack()

        Player.bank = self.bank
        Player.dev_card_stack = self.dev_card_stack
        Player.finish_turn_function = self.next_player_turn
        Player.update_all_player_states_function = self.update_player_states
        Player.update_all_player_can_trade_function = self.update_players_can_trade
        Player.accept_trade_function = self.execute_trade
        Player.rob_function = self.execute_rob
        Player.can_rob_function = self.player_can_rob
        Player.rob_nobody_function = self.exit_robber

        board_center_x = WINDOW_WIDTH // 2
        board_center_y = (self.board_space // 2) + self.margin

        # more sizing fields used for bank, dice, and player representations
        self.component_width = 0
        self.component_height = 0
        self.other_player_width = 0
        self.other_player_height = 0
        self.instructions_x = 0
        self.instructions_y = 0
        self.instructions_width = 0

        self.longest_road_sprite = arcade.Sprite("sprites/longest_road_card.png")
        self.largest_army_sprite = arcade.Sprite("sprites/largest_army_card.png")
        self.dev_card_sprite = arcade.Sprite("sprites/dev_card_img.png")
        arcade.load_font("fonts/Bavex.ttf")

        self.dice = None

        self.players = []
        self.num_players = 0
        self.num_bot_players = 0
        self.board = Board(board_center_x, board_center_y, self.players, height=self.board_space)

        #Player.bank = self.bank
        #Player.dev_card_stack = self.dev_card_stack

        # gameplay fields
        self.current_state = None
        self.active_player_index = 0
        self.active_player = None
        self.turn_direction = 0
        self.start_turn_number = 0
        self.start_turn_settlement = False

        # start game
        self.setup_players()


    # initiates the player select screen
    def setup_players(self):
        self.current_state = GameState.PLAYER_SELECT

        self.two_button.set_visible(True)
        self.three_button.set_visible(True)
        self.four_button.set_visible(True)

        button_size = WINDOW_HEIGHT // 8
        self.two_button.set_position_and_size((WINDOW_WIDTH // 2) - button_size * 1.1,
                                              (WINDOW_HEIGHT // 2) - button_size,
                                              button_size, button_size)
        self.three_button.set_position_and_size((WINDOW_WIDTH // 2),
                                                (WINDOW_HEIGHT // 2) - button_size,
                                                button_size, button_size)
        self.four_button.set_position_and_size((WINDOW_WIDTH // 2) + button_size * 1.1,
                                               (WINDOW_HEIGHT // 2) - button_size,
                                               button_size, button_size)

        self.two_button.on_click = lambda: self.setup_bots(2)
        self.three_button.on_click = lambda: self.setup_bots(3)
        self.four_button.on_click = lambda: self.setup_bots(4)


    # initiates the bot select screen
    def setup_bots(self, num_players):
        self.current_state = GameState.BOT_SELECT

        self.zero_button.set_visible(True)
        self.one_button.set_visible(True)
        self.two_button.set_visible(True)
        self.three_button.set_visible(False)
        self.four_button.set_visible(False)

        if num_players >= 3:
            self.three_button.set_visible(True)
        if num_players >= 4:
            self.four_button.set_visible(True)

        button_size = WINDOW_HEIGHT // 8
        self.zero_button.set_position_and_size((WINDOW_WIDTH // 2) - button_size * 2.2,
                                              (WINDOW_HEIGHT // 2) - button_size,
                                              button_size, button_size)
        self.one_button.set_position_and_size((WINDOW_WIDTH // 2) - button_size * 1.1,
                                                (WINDOW_HEIGHT // 2) - button_size,
                                                button_size, button_size)
        self.two_button.set_position_and_size((WINDOW_WIDTH // 2),
                                               (WINDOW_HEIGHT // 2) - button_size,
                                               button_size, button_size)
        self.three_button.set_position_and_size((WINDOW_WIDTH // 2) + button_size * 1.1,
                                              (WINDOW_HEIGHT // 2) - button_size,
                                              button_size, button_size)
        self.four_button.set_position_and_size((WINDOW_WIDTH // 2) + button_size * 2.2,
                                                (WINDOW_HEIGHT // 2) - button_size,
                                                button_size, button_size)

        self.zero_button.on_click = lambda: self.reset(num_players, 0)
        self.one_button.on_click = lambda: self.reset(num_players, 1)
        self.two_button.on_click = lambda: self.reset(num_players, 2)
        self.three_button.on_click = lambda: self.reset(num_players, 3)
        self.four_button.on_click = lambda: self.reset(num_players, 4)


    # resets the game
    def reset(self, num_players, num_bots):
        self.num_players = num_players
        self.num_bot_players = num_bots

        self.zero_button.set_visible(False)
        self.one_button.set_visible(False)
        self.two_button.set_visible(False)
        self.three_button.set_visible(False)
        self.four_button.set_visible(False)

        # set positions/sizes of components
        self.component_width = (WINDOW_WIDTH - self.board.width + self.board.x_spacing) // 2
        self.component_height = self.logo_space + self.margin + self.board.x_spacing
        self.other_player_width = (WINDOW_WIDTH - self.board.width) * 0.4
        self.other_player_height = ((WINDOW_HEIGHT - self.component_height - (self.margin * 5))
                                    // (self.num_players - 1))

        dice_width = (WINDOW_WIDTH - self.board.width - (self.margin * 2)) // 2
        dice_height = dice_width * 0.52
        dice_x = WINDOW_WIDTH - (self.margin * 2) - (dice_width // 2)
        dice_y = (self.margin * 2) + (dice_height // 2)

        self.instructions_width = (WINDOW_WIDTH - self.board.width - (self.margin * 4)) // 2
        self.instructions_x = WINDOW_WIDTH - self.margin - (self.instructions_width // 2)
        self.instructions_y = WINDOW_HEIGHT - self.component_height - (self.margin * 2)

        # longest road/army card stuff
        self.longest_road_sprite.center_x = WINDOW_WIDTH - ((5 * self.component_width) / 6)
        self.longest_road_sprite.center_y = WINDOW_HEIGHT - (self.component_height / 4)
        self.longest_road_sprite.width = self.component_width / 3
        self.longest_road_sprite.height = self.component_height / 2

        self.largest_army_sprite.center_x = WINDOW_WIDTH - ((5 * self.component_width) / 6)
        self.largest_army_sprite.center_y = WINDOW_HEIGHT - ((3 * self.component_height) / 4)
        self.largest_army_sprite.width = self.component_width / 3
        self.largest_army_sprite.height = self.component_height / 2

        self.dev_card_sprite.center_x = WINDOW_WIDTH - (self.component_width / 4)
        self.dev_card_sprite.center_y = WINDOW_HEIGHT - (self.component_height / 2)
        self.dev_card_sprite.width = self.component_width / 2
        self.dev_card_sprite.height = self.component_height

        # initialize game objects
        # self.bank = Bank()
        # self.dev_card_stack = DevCardStack()
        self.dice = Dice(dice_x, dice_y, dice_width, dice_height)

        self.players.clear()
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

            if i >= self.num_players - self.num_bot_players:
                p.set_robot(Robot(p, self.board))

            self.players.append(p)


        # gameplay fields
        self.current_state = GameState.START_TURN
        self.active_player_index = -1
        self.turn_direction = 1
        self.start_turn_number = 0
        self.start_turn_settlement = True
        self.next_player_turn()


    # advances to the next player's turn, updating player UIs and updating the game state
    def next_player_turn(self):
        # this happens once during turn transition

        # cycle active player
        if self.active_player_index < 0:
            self.turn_direction = 1
        self.active_player_index += self.turn_direction

        if self.current_state == GameState.START_TURN:
            if self.active_player_index >= self.num_players:
                self.active_player_index = self.num_players - 1
                self.turn_direction = -1
                self.start_turn_number += 1

            if self.active_player_index < 0:
                self.active_player_index = 0
                self.turn_direction = 1
                self.current_state = GameState.ROLL
        else:
            if self.active_player_index >= self.num_players:
                self.active_player_index = 0

            self.current_state = GameState.ROLL

        self.active_player = self.players[self.active_player_index]
        

        # set active player position
        self.active_player.set_active_player(True)
        self.active_player.set_position_and_size(0, self.component_width,
                                                 WINDOW_HEIGHT - self.component_height,
                                                 WINDOW_HEIGHT - self.margin)

        # set inactive player positions
        i = self.num_players - 2  # iterate through inactive player positions
        p = self.active_player_index + 1  # iterate through inactive players
        while (i >= 0):
            if p >= self.num_players:
                p = 0
            self.players[p].set_active_player(False)
            self.players[p].set_position_and_size(0, self.other_player_width,
                                                  self.margin + (i * (self.margin
                                                                      + self.other_player_height)),
                                                  (i + 1) * (self.margin + self.other_player_height))
            p += 1
            i -= 1

        self.update_player_states()

        # there is almost no way this works delete it if you need main
        # sorry for leaving this here
        if self.active_player.is_bot():
            if self.current_state == GameState.START_TURN:
                self.active_player.get_robot().play_first_turn()
                self.next_player_turn()
            elif self.current_state == GameState.ROLL:
                self.dice.roll()


    # updates each player's ability to accept a given trade based on whether they have enough
    # resources
    def update_players_can_trade(self, inventory):
        for p in self.players:
            p.update_can_trade(inventory)


    # swaps resources between the active player and another player
    def execute_trade(self, player2):
        player2.add_resources(self.active_player.give_inventory.get_amounts())
        player2.use_resources(self.active_player.get_inventory.get_amounts())
        self.active_player.add_resources(self.active_player.get_inventory.get_amounts())
        self.active_player.use_resources(self.active_player.give_inventory.get_amounts())

        self.current_state = GameState.BUILD
        self.update_player_states()


    # returns true if the robber is currently next to some player
    def player_can_rob(self):
        for p in self.players:
            if p != self.active_player:
                if p.is_next_to_robber():
                    return True
        return False


    # executes the active player taking a single random resource from another player
    def execute_rob(self, player2):
        self.active_player.add_resources(player2.rob())
        self.exit_robber()


    # exits the robber state without taking any resources from other players
    def exit_robber(self):
        self.current_state = GameState.TRADE
        self.update_player_states()


    # updates each players state, either based on the current game state, or to a specific
    # player state if specified
    def update_player_states(self, set_to=None):
        for p in self.players:
            if set_to is None:
                p.set_state(self.current_state)
            else:
                p.handle_state(set_to)


    # checks for a winner
    def check_winner(self):
        for p in self.players:
            if p.get_points() >= 11:
                print(f"{p.get_color()} player wins!")


    def on_draw(self):
        self.clear()
        self.sprites.draw()

        if self.current_state == GameState.PLAYER_SELECT:

            arcade.draw_text("Select number of total players", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.BLACK, font_size=WINDOW_WIDTH / 40, anchor_x="center",
                             anchor_y="center", font_name="Bavex")

            self.two_button.on_draw()
            self.three_button.on_draw()
            self.four_button.on_draw()

        elif self.current_state == GameState.BOT_SELECT:
            arcade.draw_text("Select number of bot players", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                             arcade.color.BLACK, font_size=WINDOW_WIDTH / 40, anchor_x="center",
                             anchor_y="center", font_name="Bavex")

            self.zero_button.on_draw()
            self.one_button.on_draw()
            self.two_button.on_draw()
            self.three_button.on_draw()
            self.four_button.on_draw()

        else:
            self.board.draw()
            if self.current_state in INSTRUCTIONS and not self.active_player.is_bot():
                arcade.draw_text(INSTRUCTIONS[self.current_state], self.instructions_x,
                                 self.instructions_y, TEXT_COLOR, font_size=20,
                                 width=self.instructions_width, anchor_x="center", anchor_y="top",
                                 multiline=True, font_name="Bavex")

            if self.current_state != GameState.START_TURN:
                self.dice.on_draw()

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
        # print(self.current_state)
        # this loops frequently

        # manage game state
        if self.current_state == GameState.ROLL:
            self.dice.on_update(delta_time)

            if self.dice.ready: # this happens once per turn
                # handle roll sum
                roll_value = self.dice.get_sum_and_reset()

                if self.active_player.is_bot():
                    self.active_player.get_robot().play_turn()
                    self.next_player_turn()

                if roll_value == 7:
                    self.current_state = GameState.ROBBER
                else:
                    self.board.allocate_resources(roll_value)
                    self.current_state = GameState.TRADE
                    self.update_player_states()

        self.check_winner()


    def on_mouse_press(self, x, y, button, modifiers):
        for p in self.players:
            p.on_mouse_press(x, y)

        self.board.find_longest_road()

        if self.current_state == GameState.PLAYER_SELECT or self.current_state == GameState.BOT_SELECT:
            self.zero_button.on_mouse_press(x, y)
            self.one_button.on_mouse_press(x, y)
            self.two_button.on_mouse_press(x, y)
            self.three_button.on_mouse_press(x, y)
            self.four_button.on_mouse_press(x, y)

        elif not self.active_player.is_bot():
            if self.current_state == GameState.START_TURN:
                if self.board.on_mouse_press(x, y, button, self.active_player,
                                             can_build_road=not self.start_turn_settlement,
                                             can_build_settlement=self.start_turn_settlement,
                                             start_turn=self.start_turn_number):
                    if self.start_turn_settlement:
                        self.start_turn_settlement = False
                    else:
                        self.start_turn_settlement = True
                        self.next_player_turn()

            elif self.current_state == GameState.ROLL:
                self.dice.on_mouse_press(x, y)

            elif self.current_state == GameState.TRADE or self.current_state == GameState.BUILD:
                if self.board.on_mouse_press(x, y, button, self.active_player):
                    self.current_state = GameState.BUILD
                    self.update_player_states()

            elif self.current_state == GameState.ROBBER:
                if self.board.on_mouse_press(x, y, button, self.active_player,
                                             can_build_road=False, can_build_settlement=False,
                                             can_rob=True):
                    self.update_player_states()


    def on_mouse_motion(self, x, y, dx, dy):
        if self.current_state == GameState.PLAYER_SELECT or self.current_state == GameState.BOT_SELECT:
            self.zero_button.on_mouse_motion(x, y)
            self.one_button.on_mouse_motion(x, y)
            self.two_button.on_mouse_motion(x, y)
            self.three_button.on_mouse_motion(x, y)
            self.four_button.on_mouse_motion(x, y)

        else:
            for p in self.players:
                p.on_mouse_motion(x, y)
            self.board.on_mouse_move(x, y)


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()