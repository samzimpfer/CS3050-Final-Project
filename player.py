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

class PlayerState(Enum):
    DEFAULT = 1
    ROLL = 2
    TRADE_OR_BUILD = 3
    OPEN_TRADE = 4

# TODO: convert all camelcase to snakecase for pep 8 purposes
class Player:

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15

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

        # UI elements
        self.show_resources = True # TODO: change this to False when done testing
        self.main_inventory = Inventory(False)
        self.main_inventory.change_amounts({
            Resource.BRICK: 1,
            Resource.SHEEP: 1,
            Resource.STONE: 1,
            Resource.WHEAT: 1,
            Resource.WOOD: 1
        })
        self.give_inventory = Inventory(True)
        self.get_inventory = Inventory(True, self.relay_inventory)

        self.finish_turn_button = Button("Finish turn")
        self.trade_button = Button("Trade")
        self.accept_trade_button = Button("Accept")

        self.finish_turn_button.on_click = Player.finish_turn_function
        self.trade_button.on_click = lambda : Player.update_all_player_states_function(PlayerState.OPEN_TRADE)
        self.accept_trade_button.on_click = lambda : Player.accept_trade_function(self)


    def set_active_player(self, ap):
        self.active_player = ap


    # sets the state of the Player based on the current game state, updates the player's current state
    def set_state(self, game_state):
        if game_state == GameState.ROLL:
            self.player_state = PlayerState.ROLL
        elif game_state == GameState.TRADE:
            self.player_state = PlayerState.TRADE_OR_BUILD
        elif game_state == GameState.BUILD:
            self.player_state = PlayerState.DEFAULT

        self.handle_state()


    # sets properties of the player based on its current state
    def handle_state(self, set_to=None):
        self.finish_turn_button.set_visible(False)
        self.trade_button.set_visible(False)
        self.accept_trade_button.set_visible(False)

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

        elif self.player_state == PlayerState.DEFAULT:
            self.finish_turn_button.set_visible(True)


    def relay_inventory(self):
        Player.update_all_player_can_trade_function(self.get_inventory)


    def update_can_trade(self, inventory):
        if self.main_inventory.contains(inventory.get_amounts()):
            self.accept_trade_button.set_visible(True)
        else:
            self.accept_trade_button.set_visible(False)


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

        if self.active_player:
            button_height = (self.top - self.bottom) // 8
            button_width = usable_width * 0.4
            x1 = usable_width * 0.25
            x2 = usable_width * 0.75
            y = self.bottom + (button_height * 0.8)

            self.trade_button.set_position_and_size(x1, y, button_width, button_height)
            self.finish_turn_button.set_position_and_size(x2, y, button_width, button_height)
            self.accept_trade_button.set_position_and_size(x2, y, button_width, button_height)

            self.trading_title_height = (self.top - self.bottom) * 0.1
            self.trading_panel_width = (self.right - self.left) * self.trading_panel_width_ratio
            self.give_inventory.set_position_and_size(self.right + (self.trading_panel_width / 2),
                                                      self.top - self.trading_title_height - self.trading_panel_width / 8,
                                                      self.trading_panel_width)
            self.get_inventory.set_position_and_size(self.right + (self.trading_panel_width / 2),
                                                      self.center_y - self.trading_title_height - self.trading_panel_width / 8,
                                                      self.trading_panel_width)
        else:
            self.accept_trade_button.set_position_and_size(self.left + (usable_width / 2),
                                                           self.center_y, usable_width * 0.7,
                                                           usable_width * 0.2)


    def add_road(self,start_node, end_node):
        if start_node not in self.roads:
            self.roads.append(start_node)
        if end_node not in self.roads:
            self.roads.append(end_node)


    def get_roads(self):
        return self.roads


    def add_resources(self, amts):
        Player.bank.TakeResources(amts)
        self.main_inventory.change_amounts(amts)


    #decrements resources if possible and returns true, else returns false
    def use_resources(self, amts):
        Player.bank.ReturnResources(amts)
        for r, a in amts.items():
            amts[r] = -a
        self.main_inventory.change_amounts(amts)


    # returns True if the player owns at least a certain set of resources, and False otherwise
    def has_resources(self, amts):
        return self.main_inventory.contains(amts)


    def get_color(self):
        return self.color


    # can build functions
    # return True is the player hasn't exceeded the limit per building and has the resources to build, and False otherwise
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
    # NOTE: these functions should not actually build things, they just update the player's resources
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
        if self.UseResources(self.DEV_CARD_COST):
            drawn_dev_card = GameDevCards.DrawCard()
            print(f"{drawn_dev_card.name}: {drawn_dev_card.description}")
            match drawn_dev_card:
                case Knight():
                    #TODO: add move robber
                    self.knight_card_count += 1
                case YearOfPlenty():
                    #TODO: not sure if we're doing UI display for resource and stuff so leaving this blank for now
                    pass
                case RoadBuilding():
                    #adding resources for roads, will need to add edge case for not enough resources as the card doesn't
                    # actually use resources
                    self.AddResources({Resource.WOOD:2, Resource.BRICK:2})
                case Monopoly():
                    pass
                case _:
                    pass
            self.player_dev_cards.append(GameDevCards.DrawCard())


    # sets the value of has_longest_road for this player
    def set_longest_road(self, value):
        self.has_longest_road = value


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
        arcade.draw_lrbt_rectangle_outline(self.left, self.right, self.bottom, self.top, UI_OUTLINE_COLOR, 6)
        arcade.draw_lrbt_rectangle_filled(self.right - self.color_tab_width, self.right + 3,
                                          self.bottom + 3, self.top - 3, self.color)

        # draw resources
        if self.show_resources:
            self.main_inventory.on_draw()

        if self.active_player:
            self.finish_turn_button.on_draw()
            self.trade_button.on_draw()

            if self.player_state == PlayerState.OPEN_TRADE:
                arcade.draw_lrbt_rectangle_filled(self.right, self.right + self.trading_panel_width,
                                                  self.bottom, self.top, UI_COLOR)
                arcade.draw_lrbt_rectangle_outline(self.right, self.right + self.trading_panel_width,
                                                   self.bottom, self.top, UI_OUTLINE_COLOR, 6)

                arcade.draw_lrbt_rectangle_filled(self.right, self.right + self.trading_panel_width,
                                                  self.top - self.trading_title_height, self.top, UI_OUTLINE_COLOR)
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


    def on_mouse_motion(self, x, y):
        self.finish_turn_button.on_mouse_motion(x, y)
        self.trade_button.on_mouse_motion(x, y)
        self.accept_trade_button.on_mouse_motion(x, y)

        self.main_inventory.on_mouse_motion(x, y)
        self.give_inventory.on_mouse_motion(x, y)
        self.get_inventory.on_mouse_motion(x, y)