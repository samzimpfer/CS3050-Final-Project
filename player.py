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
#from main import WINDOW_WIDTH, WINDOW_HEIGHT

class PlayerState(Enum):
    DEFAULT = 1
    ROLL = 2
    TRADE_OR_BUILD = 3
    OPEN_TRADE = 4
    MENU = 5

# TODO: convert all camelcase to snakecase for pep 8 purposes
class Player:

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15

    #adding these directly into player class as it seems constant throughout
    screen_width, screen_height = arcade.get_display_size()
    WINDOW_WIDTH = screen_width - 100
    WINDOW_HEIGHT = screen_height - 100

    bank = None
    game_dev_cards = None
    finish_turn_function = None
    update_all_player_states_function = None
    update_all_player_can_trade_function = None
    accept_trade_function = None

    game_state = None

    def __init__(self, color):
        # inventory
        self.roads = []  # used for calculating longest road is a list of nodes
        self.color = color

        self.knight_card_count = 0
        # add other dev card fields here

        self.player_dev_cards = []

        self.settlement_count = 0
        self.city_count = 0
        self.road_count = 0

        self.has_longest_road = False
        self.has_largest_army = False

        self.victory_points = 0

        self.visible_points = 0
        self.hidden_points = 0

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

        # UI elements
        self.show_resources = True # TODO: change this to False when done testing
        self.main_inventory = Inventory(False)
        self.main_inventory.change_amounts({
            Resource.BRICK: 99,
            Resource.SHEEP: 99,
            Resource.STONE: 99,
            Resource.WHEAT: 99,
            Resource.WOOD: 99
        })
        self.give_inventory = Inventory(True)
        self.get_inventory = Inventory(True, self.relay_inventory)

        self.finish_turn_button = Button("Finish turn")
        self.trade_button = Button("Trade")
        self.accept_trade_button = Button("Accept")

        self.view_dev_cards_button = Button("Show dev cards", Player.BUTTON_COLOR)
        self.view_dev_cards_button.on_click = Player.draw_view_dev_cards

        self.view_resources_button = Button("View resources", Player.BUTTON_COLOR)
        self.view_resources_button.on_click = Player.draw_player_resources

        self.finish_turn_button.on_click = Player.finish_turn_function
        self.trade_button.on_click = \
            lambda : Player.update_all_player_states_function(PlayerState.OPEN_TRADE)
        self.accept_trade_button.on_click = lambda : Player.accept_trade_function(self)

        self.dev_card_stack_button_params = []

        self.dev_card_stack_button = Button("", (0, 0, 0, 0))
        # 'visible' so button can be pressed
        self.dev_card_stack_button.set_visible(True)

        #universal close menu button, put in main?
        self.close_menu_button = Button("Close", Player.BUTTON_COLOR)
        self.close_menu_button.set_pos((4*self.WINDOW_WIDTH) / 5, self.WINDOW_HEIGHT / 2, 200, 100)
        self.close_menu_button.on_click = Player.close_menu



    def set_active_player(self, ap):
        self.active_player = ap


    # sets the state of the Player based on the current game state, updates the player's
    # current state
    def set_state(self, game_state):
        if game_state == GameState.ROLL:
            self.player_state = PlayerState.ROLL
        elif game_state == GameState.TRADE:
            self.player_state = PlayerState.TRADE_OR_BUILD
        elif game_state == GameState.BUILD:
            self.player_state = PlayerState.DEFAULT
        elif game_state == PlayerState.MENU:
            self.player_state = PlayerState.MENU

        self.handle_state()


    # sets properties of the player based on its current state
    def handle_state(self, set_to=None):
        self.finish_turn_button.set_visible(False)
        self.trade_button.set_visible(False)
        self.accept_trade_button.set_visible(False)

        self.view_dev_cards_button.set_visible(False)
        self.view_resources_button.set_visible(False)


        #always able to view your cards
        self.view_dev_cards_button.set_visible(True)
        self.view_resources_button.set_visible(True)

        if set_to is not None:
            self.player_state = set_to

        if self.player_state == PlayerState.TRADE_OR_BUILD:
            self.trade_button.set_visible(True)
            self.finish_turn_button.set_visible(True)

        elif self.player_state == PlayerState.OPEN_TRADE:
            if self.active_player:
                self.give_inventory.set_limits(self.main_inventory.get_amounts())
            else:
                self.accept_trade_button.set_visible(True)

        elif self.player_state == PlayerState.MENU:
            self.close_menu_button.set_visible(True)

        elif self.player_state == PlayerState.DEFAULT:
            self.finish_turn_button.set_visible(True)


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
        self.dev_card_stack_button.set_pos(self.dev_card_stack_button_params[0],
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
            self.finish_turn_button.set_position_and_size(x2, y, button_width, button_height)
            self.accept_trade_button.set_position_and_size(x2, y, button_width, button_height)

            self.view_dev_cards_button.set_pos(x1, y2, button_width, button_height)
            self.view_resources_button.set_pos(x2, y2, button_width, button_height)

            self.trading_title_height = (self.top - self.bottom) * 0.1
            self.trading_panel_width = (self.right - self.left) * self.trading_panel_width_ratio
            self.give_inventory.set_position_and_size(self.right + (self.trading_panel_width / 2),
                                                      (self.top - self.trading_title_height
                                                       - self.trading_panel_width / 8),
                                                      self.trading_panel_width)
            self.get_inventory.set_position_and_size(self.right + (self.trading_panel_width / 2),
                                                      (self.center_y - self.trading_title_height
                                                       - self.trading_panel_width / 8),
                                                      self.trading_panel_width)
        else:
            self.accept_trade_button.set_position_and_size(self.left + (usable_width / 2),
                                                           self.center_y, usable_width * 0.7,
                                                           usable_width * 0.2)

    # while trading, relays the "get" inventory to main class so other players know whether they
    # have the resources necessary to make the trade
    def relay_inventory(self):
        Player.update_all_player_can_trade_function(self.get_inventory)

    # updates the player's own ability to accept a trade
    def update_can_trade(self, inventory):
        if self.main_inventory.contains(inventory.get_amounts()):
            self.accept_trade_button.set_visible(True)
        else:
            self.accept_trade_button.set_visible(False)


    # adds a set of resources to the player's inventory
    def add_resources(self, amts):
        Player.bank.TakeResources(amts)
        self.main_inventory.change_amounts(amts)


    # subtracts a set of resources from the player's inventory
    def use_resources(self, amts):
        Player.bank.ReturnResources(amts)
        for r, a in amts.items():
            amts[r] = -a
        self.main_inventory.change_amounts(amts)


    # returns True if the player owns at least a certain set of resources, and False otherwise
    def has_resources(self, amts):
        return self.main_inventory.contains(amts)


    def add_road(self,start_node, end_node):
        if start_node not in self.roads:
            self.roads.append(start_node)
        if end_node not in self.roads:
            self.roads.append(end_node)


    def get_roads(self):
        return self.roads


    def get_color(self):
        return self.color


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


    def build_settlement(self):
        if self.can_build_settlement():
            self.use_resources(SETTLEMENT_COST)
            self.settlement_count += 1
            return True
        return False


    def build_city(self):
        if self.can_build_city():
            self.use_resources(CITY_COST)
            self.city_count += 1
            self.settlement_count -= 1
            return True
        return False


    def buy_dev_card(self):
        if self.can_buy_dev_card():
            self.use_resources(DEV_CARD_COST)
            return True
        return False


    def BuyDevCard(self):
        if self.use_resources(DEV_CARD_COST):
            drawn_dev_card = self.game_dev_cards.DrawCard()
            self.render_single_card(drawn_dev_card)
            #print(f"{drawn_dev_card.name}: {drawn_dev_card.description}")
            match drawn_dev_card:
                case Knight():
                    #note, unused knight cards do not count towards largest army
                    self.knight_card_count += 1
                case YearOfPlenty():

                    pass
                case RoadBuilding():
                    #TODO: add building function in directly
                    pass
                case Monopoly():
                    pass
                case _:
                    pass
            self.player_dev_cards.append(drawn_dev_card)


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

        #self.view_dev_cards_button.on_draw()
        # draw resources
        if self.show_resources:
            self.main_inventory.on_draw()

        if self.active_player:
            self.finish_turn_button.on_draw()
            self.trade_button.on_draw()

            self.view_dev_cards_button.on_draw()
            self.view_resources_button.on_draw()

            if self.player_state == PlayerState.OPEN_TRADE:
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

                arcade.draw_text("Give", self.right + (self.trading_panel_width / 2),
                                 self.top - (self.trading_title_height / 2), arcade.color.BLACK,
                                 self.trading_title_height / 2, anchor_x="center", anchor_y="center")
                arcade.draw_text("Get", self.right + (self.trading_panel_width / 2),
                                 self.center_y - (self.trading_title_height / 2), arcade.color.BLACK,
                                 self.trading_title_height / 2, anchor_x="center", anchor_y="center")

                self.give_inventory.on_draw()
                self.get_inventory.on_draw()
        else:
            if self.player_state == PlayerState.OPEN_TRADE:
                self.accept_trade_button.on_draw()


    def on_mouse_press(self, x, y):
        self.finish_turn_button.on_mouse_press(x, y)
        self.trade_button.on_mouse_press(x, y)
        self.accept_trade_button.on_mouse_press(x, y)

        self.main_inventory.on_mouse_press(x, y)
        self.give_inventory.on_mouse_press(x, y)
        self.get_inventory.on_mouse_press(x, y)

        self.view_dev_cards_button.on_mouse_press(x, y)
        self.view_resources_button.on_mouse_press(x, y)

        self.close_menu_button.on_mouse_press(x, y)


    def on_mouse_motion(self, x, y):
        self.finish_turn_button.on_mouse_motion(x, y)
        self.trade_button.on_mouse_motion(x, y)
        self.accept_trade_button.on_mouse_motion(x, y)

        self.main_inventory.on_mouse_motion(x, y)
        self.give_inventory.on_mouse_motion(x, y)
        self.get_inventory.on_mouse_motion(x, y)

        self.view_dev_cards_button.on_mouse_motion(x, y)
        self.view_resources_button.on_mouse_motion(x, y)

        self.close_menu_button.on_mouse_motion(x, y)


    def draw_view_dev_cards(self):
        #just gonna hope no one draws more than 10 dev cards for now, scaling lowkey a pita
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

        arcade.draw_lrbt_rectangle_filled(self.WINDOW_WIDTH / 4, (3 * self.WINDOW_WIDTH) / 4, self.WINDOW_HEIGHT / 4, (3 * self.WINDOW_HEIGHT) / 4, arcade.color.GRAY)

        colCount = 1
        #this just draws the array of dev cards
        for card in self.player_dev_cards:
            dev_sprite = arcade.Sprite(card.pathname)
            dev_sprite.center_x = l + ((colCount * display_width) / 5) - sprite_x_offset
            if colCount > 5:
                dev_sprite.center_y = b + (3 * (display_height / 4))
            else:
                dev_sprite.center_y = b + (display_height / 4)
            dev_sprite.width = sprite_width
            dev_sprite.height = sprite_height
            # unsure where to add the drawing at this point, but this should be scaled properly and work. sprite path stored
            # in class instances
            arcade.draw_sprite(dev_sprite)
            colCount += 1
        #I will probably need some help getting this to work properly, but the idea is switch to menu state when viewing
        # cards so that the close menu button will appear
        self.set_state(PlayerState.MENU)

    def render_single_card(self, dev_card):
        single_sprite = arcade.Sprite(dev_card.pathname)
        single_sprite.center_x = self.WINDOW_WIDTH / 2
        single_sprite.center_y = self.WINDOW_HEIGHT / 2
        single_sprite.width = self.WINDOW_WIDTH / 5
        single_sprite.height = (3.5 * ((self.WINDOW_WIDTH / 5) * 2.5))
        arcade.draw_sprite(single_sprite)

        self.set_state(PlayerState.MENU)

    #this is for monopoly and YOP
    #TODO: add buttons and functions
    def draw_resource_select(self):
        l = self.WINDOW_WIDTH / 4
        r = (3 * self.WINDOW_WIDTH) / 4
        b = (2 * self.WINDOW_HEIGHT) / 5
        t = (3 * self.WINDOW_HEIGHT) / 5
        r_select_width = r - l
        r_select_height = t - b
        r_select_section = r_select_width / 5
        center_align_offset = r_select_height / 2
        arcade.draw_lrbt_rectangle_filled(l, r, b, t, arcade.color.GRAY)
        for i, e in self.resource_sprites.values():
            select_sprite = e
            select_sprite.center_x = (l + (i * r_select_section)) - center_align_offset
            select_sprite.center_y = self.WINDOW_HEIGHT / 2
            select_sprite.width = r_select_section
            select_sprite.height = r_select_height
            arcade.draw_sprite(select_sprite)

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

    #hopefully this just resets the screen
    def close_menu(self):
        self.set_state(PlayerState.DEFAULT)
        self.on_draw()