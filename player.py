"""
The main purpose of this class is to keep track of a player's inventory.
It includes a counter for each resource and dev card that the player might own.
It also includes counters for things that will count towards the player's score at the end, such as settlements and cities.

This class includes functions to increment or decrement resources by a specific amount.
It includes functions that reveal whether the player is able to build certain things, based on their inventory.
It also includes functions that simulate building, but these DO NOT actually build anything, they ONLY update the player's resources in the event that they build

Finally, this class includes functions to handle dev cards and the longest road, and a function to return the number of points the player currently has

NOTE: there are still some things to add, but this encompasses the basics
"""
from gameobjects import *
from button import Button
from inventory import Inventory
import arcade
import math
from menu_support import *
#from main import WINDOW_WIDTH, WINDOW_HEIGHT

class PlayerState(Enum):
    DEFAULT = 1
    START_TURN = 2
    ROLL = 3
    TRADE_OR_BUILD = 4
    ROBBER = 5
    OPEN_TRADE = 6
    DEVCARD_MENU = 7
    SINGLE_CARD_MENU = 8
    YOP_MENU = 9
    MONOPOLY_MENU = 10
    MONOPOLY_CONCLUSION = 11


# TODO: convert all camelcase to snakecase for pep 8 purposes
class Player:

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15

    # adding these directly into player class as it seems constant throughout
    screen_width, screen_height = arcade.get_display_size()
    WINDOW_WIDTH = screen_width - 100
    WINDOW_HEIGHT = screen_height - 100

    bank = None
    game_dev_cards = None
    finish_turn_function = None
    update_all_player_states_function = None
    update_all_player_can_trade_function = None
    accept_trade_function = None
    rob_function = None
    can_rob_function = None
    rob_nobody_function = None

    game_state = None


    def __init__(self, color, robot=None):
        # robot
        self.robot = robot
        self.robot_sprite = arcade.Sprite("sprites/robot.png")
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.robot_sprite)

        # inventory
        self.roads = []  # used for calculating longest road is a list of nodes
        self.buildings = [] # used primarily for start turns
        self.color = color

        self.knight_card_count = 0
        # add other dev card fields here
        self.YOP_first_selection = None
        self.YOP_second_selection = None
        self.monopoly_selection = None

        self.player_dev_cards = []


        self.settlement_count = 0
        self.city_count = 0
        self.road_count = 0

        self.has_longest_road = False
        self.has_largest_army = False

        self.longest_road = 0

        self.victory_points = 0

        self.dev_card_victory_points = 0

        # UI positional fields
        self.left = 0
        self.right = 0
        self.bottom = 0
        self.top = 0
        self.color_tab_width = 30
        self.resource_sprite_width = 0
        self.trading_panel_width_ratio = 0.7
        self.trading_panel_width = 0
        self.trading_title_height = 0
        self.center_y = 0

        self.active_player = False
        self.player_state = PlayerState.DEFAULT
        self.can_trade = False

        # UI elements
        self.show_resources = True # TODO: change this to False when done testing
        self.main_inventory = Inventory(False)
        self.main_inventory.reset()
        self.main_inventory.reset_limits()
        self.main_inventory.set_amounts(Inventory.DEFAULT_AMOUNTS) # TODO: take this out
        #self.main_inventory.set_amounts(Inventory.PRELOADED_RESOURCES) # TODO: take this out
        self.get_inventory = Inventory(not self.is_bot(), self.relay_inventory)
        self.give_inventory = Inventory(not self.is_bot())

        self.finish_turn_button = Button("Finish turn")
        self.trade_button = Button("Trade")
        self.cancel_trade_button = Button("Cancel trade")
        self.rob_nobody_button = Button("Rob nobody")
        self.accept_trade_button = Button("Accept")
        self.rob_button = Button("Rob")

        self.view_dev_cards_button = Button("Show dev cards")
        self.view_dev_cards_button.on_click = lambda: self.handle_state(PlayerState.DEVCARD_MENU)

        self.dev_card_stack_button = Button("", (255, 255, 255, 255))
        # 'visible' so button can be pressed
        # self.dev_card_stack_button.on_click = lambda: self.set_player_state(PlayerState.DRAWN_CARD_MENU)
        self.dev_card_stack_button.on_click = self.buy_dev_card

        self.view_resources_button = Button("View resources")
        self.view_resources_button.on_click = Player.draw_player_resources

        self.finish_turn_button.on_click = Player.finish_turn_function
        self.trade_button.on_click = self.open_trade
        self.cancel_trade_button.on_click = \
            lambda : Player.update_all_player_states_function(PlayerState.TRADE_OR_BUILD)
        self.rob_nobody_button.on_click = Player.rob_nobody_function
        self.accept_trade_button.on_click = lambda : Player.accept_trade_function(self)
        self.rob_button.on_click = lambda : Player.rob_function(self)

        self.dev_card_stack_button_params = []


        #universal close menu button, put in main?
        self.close_menu_button = Button("Close")
        self.close_menu_button.set_position_and_size((4*self.WINDOW_WIDTH) / 5, self.WINDOW_HEIGHT / 2, 200, 100)
        self.close_menu_button.on_click = self.close_menu

        self.resource_select_buttons = create_resource_select_buttons()
        for button in self.resource_select_buttons:
            button.on_click = lambda but=button: self.select_YOP_resource(but)

        self.devcard_buttons = create_devcard_select_buttons()
        for button in self.devcard_buttons:
            button.on_click = lambda but=button: self.use_devcard(but)





    def set_longest_road_value(self, longest_road):
        self.longest_road = longest_road
    def get_longest_road_value(self):
        return self.longest_road

    def is_bot(self):
        return self.robot is not None

    def get_robot(self):
        return self.robot

    def set_robot(self, robot):
        self.robot = robot

    def set_active_player(self, ap):
        self.active_player = ap

    def return_inventory(self):
        return self.main_inventory.get_amounts()


    # sets the state of the Player based on the current game state, updates the player's
    # current state
    def set_state(self, game_state):
        if game_state == GameState.START_TURN:
            self.player_state = PlayerState.START_TURN
        elif game_state == GameState.ROLL:
            self.player_state = PlayerState.ROLL
        elif game_state == GameState.TRADE:
            self.player_state = PlayerState.TRADE_OR_BUILD
        elif game_state == GameState.BUILD:
            self.player_state = PlayerState.DEFAULT
        elif game_state == GameState.ROBBER:
            self.player_state = PlayerState.ROBBER
        elif game_state == PlayerState.MENU:
            self.player_state = PlayerState.MENU

        self.handle_state()


    # sets properties of the player based on its current state
    def handle_state(self, set_to=None):
        self.finish_turn_button.set_visible(False)
        self.trade_button.set_visible(False)
        self.cancel_trade_button.set_visible(False)
        self.rob_nobody_button.set_visible(False)
        self.accept_trade_button.set_visible(False)
        self.rob_button.set_visible(False)
        self.dev_card_stack_button.set_visible(False)

        #set all devcard and resource select buttons to not visible
        set_buttons_not_visible(self.devcard_buttons)
        set_buttons_not_visible(self.resource_select_buttons)
        #set close menu button not visible
        self.close_menu_button.set_visible(False)
        if self.active_player:
            self.dev_card_stack_button.set_visible(True)

        if self.player_state == PlayerState.START_TURN or self.is_bot():
            self.view_dev_cards_button.set_visible(False)
            self.view_resources_button.set_visible(False)
        else:
            self.view_dev_cards_button.set_visible(True)
            self.view_resources_button.set_visible(True)

        if set_to is not None:
            self.player_state = set_to
        #if this is an actual player
        if not self.is_bot():

            match self.player_state:
                case PlayerState.TRADE_OR_BUILD:
                    self.trade_button.set_visible(True)
                    self.finish_turn_button.set_visible(True)
                    self.view_dev_cards_button.set_visible(True)
                    self.YOP_first_selection = None
                    self.YOP_second_selection = None
                    self.monopoly_selection = None
                case PlayerState.OPEN_TRADE:
                    if self.active_player:
                        self.cancel_trade_button.set_visible(True)
                        self.give_inventory.set_limits(self.main_inventory.get_amounts())
                    else:
                        self.accept_trade_button.set_visible(True)
                case PlayerState.ROBBER:
                    if self.active_player:
                        if Player.can_rob_function():
                            self.rob_nobody_button.set_visible(False)
                        else:
                            self.rob_nobody_button.set_visible(True)

                    else:
                        if self.is_next_to_robber() and not self.main_inventory.is_empty():
                            self.rob_button.set_visible(True)
                case PlayerState.DEVCARD_MENU:
                    set_buttons_visible(self.devcard_buttons)
                    self.close_menu_button.set_visible(True)
                case PlayerState.SINGLE_CARD_MENU:
                    self.close_menu_button.set_visible(True)
                case PlayerState.YOP_MENU:
                    set_buttons_visible(self.resource_select_buttons)
                case PlayerState.MONOPOLY_MENU:
                    set_buttons_visible(self.resource_select_buttons)
                case PlayerState.MONOPOLY_CONCLUSION:
                    pass
                case PlayerState.DEFAULT:
                    self.finish_turn_button.set_visible(True)

    def get_state(self):
        return self.player_state

    # positions the player representation UI and it's components on the screen
    def set_position_and_size(self, l, r, b, t):
        self.left = l
        self.right = r
        self.bottom = b
        self.top = t

        usable_width = self.right - self.left - self.color_tab_width
        self.center_y = (self.top + self.bottom) / 2
        self.main_inventory.set_position_and_size(usable_width / 2,
                                                  self.top - usable_width / 8,
                                                  usable_width)

        #setting dev card button
        self.dev_card_stack_button.set_position_and_size(self.dev_card_stack_button_params[0],
                                           self.dev_card_stack_button_params[1],
                                           self.dev_card_stack_button_params[2],
                                           self.dev_card_stack_button_params[3])

        if self.active_player:
            button_height = (self.top - self.bottom) // 8
            button_width = usable_width * 0.4
            x1 = usable_width * 0.25
            x2 = usable_width * 0.75
            y = self.bottom + (button_height * 0.8)
            y2 = self.bottom + (3 * (button_height * 0.8))

            self.trade_button.set_position_and_size(x1, y, button_width, button_height)
            self.cancel_trade_button.set_position_and_size(x2, y, button_width, button_height)
            self.rob_nobody_button.set_position_and_size(x2, y, button_width, button_height)
            self.finish_turn_button.set_position_and_size(x2, y, button_width, button_height)

            self.view_dev_cards_button.set_position_and_size(x1, y2, button_width, button_height)
            self.view_resources_button.set_position_and_size(x2, y2, button_width, button_height)

            self.trading_title_height = (self.top - self.bottom) * 0.1
            self.trading_panel_width = (self.right - self.left) * self.trading_panel_width_ratio
            self.get_inventory.set_position_and_size(self.right + (self.trading_panel_width / 2),
                                                      (self.top - self.trading_title_height
                                                       - self.trading_panel_width / 8),
                                                      self.trading_panel_width)
            self.give_inventory.set_position_and_size(self.right + (self.trading_panel_width / 2),
                                                      (self.center_y - self.trading_title_height
                                                       - self.trading_panel_width / 8),
                                                      self.trading_panel_width)
        else:
            self.accept_trade_button.set_position_and_size(self.left + (usable_width / 2),
                                                           self.center_y, usable_width * 0.7,
                                                           usable_width * 0.2)
            self.rob_button.set_position_and_size(self.left + (usable_width / 2), self.center_y,
                                                  usable_width * 0.5, usable_width * 0.2)

        if self.is_bot():
            size = usable_width / 5
            self.robot_sprite.center_x = l + size
            self.robot_sprite.center_y = b + size
            self.robot_sprite.width = size
            self.robot_sprite.height = size


    # resets the player's trading inventories and opens a trade to other players
    def open_trade(self):
        self.give_inventory.reset()
        self.get_inventory.reset()
        Player.update_all_player_states_function(PlayerState.OPEN_TRADE)


    # while trading, relays the "get" inventory to main class so other players know whether they
    # have the resources necessary to make the trade
    def relay_inventory(self):
        Player.update_all_player_can_trade_function(self.get_inventory)


    # updates the player's own ability to accept a trade
    def update_can_trade(self, inventory):
        if self.main_inventory.contains(inventory.get_amounts()):
            self.accept_trade_button.set_visible(True)
            self.can_trade = True
        else:
            self.accept_trade_button.set_visible(False)
            self.can_trade = False


    # adds a set of resources to the player's inventory
    def add_resources(self, amts):
        Player.bank.TakeResources(amts)
        self.main_inventory.change_amounts(amts)


    # subtracts a set of resources from the player's inventory
    def use_resources(self, a):
        amts = a.copy()
        #Player.bank.ReturnResources(amts)
        for r, a in amts.items():
            amts[r] = -a
        self.main_inventory.change_amounts(amts)


    # returns True if the player owns at least a certain set of resources, and False otherwise
    def has_resources(self, amts):
        return self.main_inventory.contains(amts)


    # returns true if this player has a settlement/city next to the robber
    def is_next_to_robber(self):
        for node in self.buildings:
            for tile in node.adjacent_tiles:
                if tile.has_robber():
                    return True
        return False


    # decrements a random resource from this player and returns it
    def rob(self):
        random_resource = self.main_inventory.get_random_resource()
        if random_resource:
            random_resource = { random_resource[0]: 1 }
            self.use_resources(random_resource)

        return random_resource

    def add_road(self,start_node, end_node):
        if start_node not in self.roads:
            self.roads.append(start_node)
        if end_node not in self.roads:
            self.roads.append(end_node)


    def add_building(self, node):
        if node not in self.buildings:
            self.buildings.append(node)


    def get_roads(self):
        return self.roads


    def get_color(self):
        return self.color

    # TODO: just here so I can test the bot
    def has_knight(self):
        return True


    # can build functions
    # return True is the player hasn't exceeded the limit per building and has the resources to
    # build, and False otherwise
    # TODO: override limitations by resource if dev card owned
    def can_build_road(self):
        return ((self.has_resources(ROAD_COST) and
                self.road_count < self.MAX_ROADS)) # or self.has_road_building_dev_card


    def can_build_settlement(self):
        return (self.has_resources(SETTLEMENT_COST) and
                self.settlement_count < self.MAX_SETTLEMENTS)


    def can_build_city(self):
        return (self.has_resources(CITY_COST) and
                self.city_count < self.MAX_CITIES)


    def can_buy_dev_card(self):
        return self.has_resources(DEV_CARD_COST)


    # build functions
    # update the player's resources in the event that they build
    # return True if build is successful, and False otherwise
    # NOTE: these functions should not actually build things, they just update the player's
    # resources
    def build_road(self, start_node, end_node):
        if self.can_build_road():
            self.use_resources(ROAD_COST)
            self.road_count += 1
            self.add_road(start_node, end_node)
            return True
        return False


    def build_settlement(self, node):
        if self.can_build_settlement():
            self.use_resources(SETTLEMENT_COST)
            self.settlement_count += 1
            self.add_building(node)
            return True
        return False


    def build_city(self, node):
        if self.can_build_city():
            self.use_resources(CITY_COST)
            self.city_count += 1
            self.settlement_count -= 1
            self.add_building(node)
            return True
        return False


    def buy_dev_card(self):
        if self.can_buy_dev_card():
            self.use_resources(DEV_CARD_COST)
            drawn_dev_card = self.game_dev_cards.DrawCard()
            print(drawn_dev_card)
            self.player_dev_cards.append(drawn_dev_card)
            self.handle_state(PlayerState.SINGLE_CARD_MENU)
            return True
        return False




    # sets the value of has_longest_road for this player
    def set_longest_road(self, value):
        self.has_longest_road = value

    def set_largest_army(self, value):
        self.has_largest_army = value


    # returns the number of points the player has based on settlements, cities, and longest road
    def get_points(self):
        total = 0
        total += self.settlement_count
        total += (self.city_count * 2)
        if self.has_longest_road:
            total += 2
        if self.has_largest_army:
            total += 2
        total += self.dev_card_victory_points
        # add in victory card points

        return total


    def on_draw(self):
        # draw player representation
        arcade.draw_lrbt_rectangle_filled(self.left, self.right, self.bottom, self.top, UI_COLOR)
        arcade.draw_lrbt_rectangle_outline(self.left, self.right, self.bottom, self.top,
                                           UI_OUTLINE_COLOR, 6)
        arcade.draw_lrbt_rectangle_filled(self.right - self.color_tab_width, self.right + 3,
                                          self.bottom + 3, self.top - 3, self.color)

        #visible_points_text = arcade.Text(f"Victory Points: {self.visible_points}")

        # draw resources
        if self.show_resources:
            self.main_inventory.on_draw()

        if self.active_player:
            self.finish_turn_button.on_draw()
            self.trade_button.on_draw()
            self.cancel_trade_button.on_draw()

            self.view_dev_cards_button.on_draw()
            self.view_resources_button.on_draw()

            match self.player_state:
                case PlayerState.OPEN_TRADE:
                    arcade.draw_lrbt_rectangle_filled(self.right, self.right + self.trading_panel_width,
                                                      self.bottom, self.top, UI_COLOR)
                    arcade.draw_lrbt_rectangle_outline(self.right, (self.right
                                                                    + self.trading_panel_width),
                                                       self.bottom, self.top, UI_OUTLINE_COLOR, 6)

                    arcade.draw_lrbt_rectangle_filled(self.right, self.right + self.trading_panel_width,
                                                      self.top - self.trading_title_height, self.top,
                                                      UI_OUTLINE_COLOR)
                    arcade.draw_lrbt_rectangle_filled(self.right, self.right + self.trading_panel_width,
                                                      self.center_y - self.trading_title_height,
                                                      self.center_y, UI_OUTLINE_COLOR)

                    arcade.draw_text("Get", self.right + (self.trading_panel_width / 2),
                                     self.top - (self.trading_title_height / 2), arcade.color.BLACK,
                                     self.trading_title_height / 2, anchor_x="center", anchor_y="center")
                    arcade.draw_text("Give", self.right + (self.trading_panel_width / 2),
                                     self.center_y - (self.trading_title_height / 2), arcade.color.BLACK,
                                     self.trading_title_height / 2, anchor_x="center", anchor_y="center")

                    self.give_inventory.on_draw()
                    self.get_inventory.on_draw()
                case PlayerState.ROBBER:
                    self.rob_nobody_button.on_draw()
                case PlayerState.DEVCARD_MENU:
                    set_buttons_visible(self.devcard_buttons)
                    self.draw_view_dev_cards()
                    for button in self.devcard_buttons:
                        button.on_draw()
                    self.close_menu_button.on_draw()
                case PlayerState.SINGLE_CARD_MENU:
                    self.render_single_card(self.player_dev_cards[-1])
                    self.close_menu_button.on_draw()
                case PlayerState.YOP_MENU:
                    draw_default_resource_view()
                    self.draw_YOP_selection()
                    for button in self.resource_select_buttons:
                        button.on_draw()
                case PlayerState.MONOPOLY_MENU:
                    draw_default_resource_view()
                    self.draw_monopoly_selection()
                    for button in self.resource_select_buttons:
                        button.on_draw()






        else:
            if self.player_state == PlayerState.OPEN_TRADE:
                self.accept_trade_button.on_draw()
            elif self.player_state == PlayerState.ROBBER:
                self.rob_button.on_draw()




        if self.is_bot():
            self.sprites.draw()


    def on_mouse_press(self, x, y):
        self.finish_turn_button.on_mouse_press(x, y)
        self.trade_button.on_mouse_press(x, y)
        self.cancel_trade_button.on_mouse_press(x, y)
        self.rob_nobody_button.on_mouse_press(x, y)

        self.accept_trade_button.on_mouse_press(x, y)
        self.rob_button.on_mouse_press(x, y)

        self.main_inventory.on_mouse_press(x, y)
        self.give_inventory.on_mouse_press(x, y)
        self.get_inventory.on_mouse_press(x, y)

        self.view_dev_cards_button.on_mouse_press(x, y)
        self.view_resources_button.on_mouse_press(x, y)

        self.close_menu_button.on_mouse_press(x, y)

        self.dev_card_stack_button.on_mouse_press(x, y)

        if self.player_state == PlayerState.DEVCARD_MENU:
            for button in self.devcard_buttons:
                button.on_mouse_press(x, y)
        if self.player_state == PlayerState.YOP_MENU:
            for button in self.resource_select_buttons:
                button.on_mouse_press(x, y)
        if self.player_state == PlayerState.MONOPOLY_MENU:
            for button in self.resource_select_buttons:
                button.on_mouse_press(x, y)

    def on_mouse_motion(self, x, y):
        self.finish_turn_button.on_mouse_motion(x, y)
        self.trade_button.on_mouse_motion(x, y)
        self.cancel_trade_button.on_mouse_motion(x, y)
        self.rob_nobody_button.on_mouse_motion(x, y)

        self.accept_trade_button.on_mouse_motion(x, y)
        self.rob_button.on_mouse_motion(x, y)

        self.main_inventory.on_mouse_motion(x, y)
        self.give_inventory.on_mouse_motion(x, y)
        self.get_inventory.on_mouse_motion(x, y)

        self.view_dev_cards_button.on_mouse_motion(x, y)
        self.view_resources_button.on_mouse_motion(x, y)

        self.close_menu_button.on_mouse_motion(x, y)

        if self.player_state == PlayerState.DEVCARD_MENU:
            for button in self.devcard_buttons:
                button.on_mouse_motion(x, y)
        if self.player_state == PlayerState.YOP_MENU:
            for button in self.resource_select_buttons:
                button.on_mouse_motion(x, y)
        if self.player_state == PlayerState.MONOPOLY_MENU:
            for button in self.resource_select_buttons:
                button.on_mouse_motion(x, y)

    def draw_view_dev_cards(self):
        # self.close_menu_button.on_draw()
        # just gonna hope no one draws more than 10 dev cards for now, scaling lowkey a pita

        self.close_menu_button.set_visible(True)
        draw_devcard_backing()
        l = self.WINDOW_WIDTH / 4
        r = (3 * self.WINDOW_WIDTH) / 4
        b = self.WINDOW_HEIGHT / 4
        t = (3 * self.WINDOW_HEIGHT) / 4
        display_width = r - l
        display_height = t - b
        sprite_width = display_width / 5
        sprite_x_offset = sprite_width / 2

        sprite_height = display_height / 2
        sprite_y_offset = sprite_height / 2

        arcade.draw_lrbt_rectangle_filled(self.WINDOW_WIDTH / 4, (3 * self.WINDOW_WIDTH) / 4, self.WINDOW_HEIGHT / 4,
                                          (3 * self.WINDOW_HEIGHT) / 4, arcade.color.GRAY)

        colCount = 1
        # this just draws the array of dev cards
        for card in self.player_dev_cards:
            dev_sprite = arcade.Sprite(card.pathname)
            dev_sprite.center_x = l + ((colCount * display_width) / 5) - sprite_x_offset
            if colCount > 5:
                dev_sprite.center_x = l + (((colCount - 5) * display_width) / 5) - sprite_x_offset
                dev_sprite.center_y = b + (display_height / 4)
            else:
                dev_sprite.center_y = b + (3 * (display_height / 4))
            dev_sprite.width = sprite_width
            dev_sprite.height = sprite_height
            # unsure where to add the drawing at this point, but this should be scaled properly and work. sprite path stored
            # in class instances
            arcade.draw_sprite(dev_sprite)
            colCount += 1
        for i in range(len(self.player_dev_cards)):
            self.devcard_buttons[i].set_visible(True)
            self.devcard_buttons[i].on_draw()
        # I will probably need some help getting this to work properly, but the idea is switch to menu state when viewing
        # cards so that the close menu button will appear
        self.handle_state(PlayerState.DEVCARD_MENU)

    def render_single_card(self, dev_card):
        single_sprite = arcade.Sprite(dev_card.pathname)
        single_sprite.center_x = self.WINDOW_WIDTH / 2
        single_sprite.center_y = self.WINDOW_HEIGHT / 2
        single_sprite.width = self.WINDOW_WIDTH / 5
        single_sprite.height = (3.5 * ((self.WINDOW_WIDTH / 5) / 2.5))
        arcade.draw_sprite(single_sprite)
        self.handle_state(PlayerState.SINGLE_CARD_MENU)



    #TODO: this correctly displays player resource count, it just needs to be properly implemented into the draw flow
    def draw_player_resources(self):
        l = self.WINDOW_WIDTH / 4
        r = (3 * self.WINDOW_WIDTH) / 4
        b = (2 * self.WINDOW_HEIGHT) / 5
        t = (3 * self.WINDOW_HEIGHT) / 5
        r_select_width = r - l
        r_select_height = t - b
        r_select_section = r_select_width / 5
        center_align_offset = r_select_height / 2
        arcade.draw_lrbt_rectangle_filled(l, r, b, t, arcade.color.GRAY)

        for i, (k, e) in enumerate(self.resource_sprites.items()):
            select_sprite = e
            select_sprite.center_x = (l + ((i+1) * r_select_section)) - center_align_offset
            select_sprite.center_y = self.WINDOW_HEIGHT / 2
            select_sprite.width = r_select_section
            select_sprite.height = r_select_height
            arcade.draw_sprite(select_sprite)

            #resource_val = arcade.Text(str(self.resources[i]), l + (i * r_select_section), b, arcade.color.BLACK, self.resource_sprite_width / 3)
            arcade.draw_text(f"x{self.resources[k]}", l + ((i+1) * r_select_section) - (r_select_section / 3), b, arcade.color.BLACK, self.resource_sprite_width / 2)
        self.set_state(PlayerState.MENU)

    def use_devcard(self, button):
        devcard_index = self.get_buttonarray_index(button, "devcards")
        print(devcard_index)
        devcard = self.player_dev_cards.pop(devcard_index)
        print(devcard)
        print(type(devcard))
        match devcard:
            case Knight():
                self.handle_state(PlayerState.ROBBER)
                self.knight_card_count += 1
            case RoadBuilding():
                #self.handle_state(PlayerState.ROADBUILDING_MENU)
                pass
            case Monopoly():
                self.handle_state(PlayerState.MONOPOLY_MENU)
            case YearOfPlenty():
                self.handle_state(PlayerState.YOP_MENU)
            case _:
                self.dev_card_victory_points += 1
                self.player_dev_cards.pop(devcard_index)
                self.handle_state(PlayerState.DEFAULT)
                self.close_menu()


    #return the index of the button which corresponds to the actual card object
    def get_buttonarray_index(self, button, flag):
        if flag == "devcards":
            return self.devcard_buttons.index(button)
        else:
            #print(self.resource_select_buttons.index(button))
            return self.resource_select_buttons.index(button)

    #hopefully this just resets the screen
    def close_menu(self):
        self.set_state(GameState.TRADE)
        #self.on_draw()


    def draw_YOP_selection(self):
        draw_YOP_selection_backing()
        if self.YOP_first_selection:
            sprite = get_YOP_selection_sprite(SPRITE_PATHS[self.YOP_first_selection], 1)
            arcade.draw_sprite(sprite)
        if self.YOP_second_selection:
            sprite2 = get_YOP_selection_sprite(SPRITE_PATHS[self.YOP_second_selection], 2)
            arcade.draw_sprite(sprite2)
            #TODO: somehow sleep this, not working for some reason
            #time.sleep(1)
        if self.YOP_first_selection and self.YOP_second_selection:
            self.add_resources({Resource(self.YOP_first_selection):2, Resource(self.YOP_second_selection):2})
            self.YOP_first_selection = None
            self.YOP_second_selection = None
            self.handle_state(GameState.TRADE)

    def select_YOP_resource(self, button):
        if not self.YOP_first_selection:
            print(f"first selection index: {self.get_buttonarray_index(button, 'resource')}")
            resource_index = self.get_buttonarray_index(button, "resource")
            self.YOP_first_selection = resource_index
        else:
            resource_index = self.get_buttonarray_index(button, "resource")
            self.YOP_second_selection = resource_index

    def draw_monopoly_selection(self):
        draw_single_selection_backing()
        if self.YOP_first_selection:
            print(self.YOP_first_selection)
            sprite = get_single_selection_sprite(SPRITE_PATHS[self.YOP_first_selection])
            arcade.draw_sprite(sprite)
            #sleep 1
            self.monopoly_selection = Resource(self.YOP_first_selection)
            self.YOP_first_selection = None
            self.handle_state(PlayerState.MONOPOLY_CONCLUSION)

    def get_monopoly_selection(self):
        return self.monopoly_selection