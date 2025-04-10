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

import arcade
from button import Button
from gameobjects import *
import math

#from scratchpad import WINDOW_WIDTH, WINDOW_HEIGHT


class PlayerState(Enum):
    DEFAULT = 1
    ROLL = 2
    ABLE_TO_TRADE = 3
    # OPEN_TRADE = 4
    TRADING = 4
    MENU = 5

# TODO: convert all camelcase to snakecase for pep 8 purposes
class Player:

    UI_COLOR = (75, 110, 150)
    UI_OUTLINE_COLOR = (40, 80, 140)
    BUTTON_COLOR = (40, 80, 140)

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15


    #adding these directly into player class as it seems constant throughout
    screen_width, screen_height = arcade.get_display_size()
    WINDOW_WIDTH = screen_width - 100
    WINDOW_HEIGHT = screen_height - 100

    #testing this out, not even sure if it works
    # global Bank
    # global GameDevCards

    # edit from Sam
    # these are class variables that are shared for each instance of the class
    # global is not needed here (keeps the bank encapsulated in the Player class, theoretically better for security)
    # these are being set to the same instance that was created in main.__init__() in that function
    # reference from inside player functions as Player.bank
    bank = None
    game_dev_cards = None
    trade_function = None
    finish_turn_function = None

    ROAD_COST = {
        Resource.BRICK:1,
        Resource.WOOD:1
    }

    SETTLEMENT_COST = {
        Resource.BRICK:1,
        Resource.SHEEP:1,
        Resource.WHEAT:1,
        Resource.WOOD:1
    }

    CITY_COST = {
        Resource.WHEAT:2,
        Resource.STONE:3
    }

    DEV_CARD_COST = {
        Resource.WHEAT:1,
        Resource.STONE:1,
        Resource.SHEEP:1,
    }

    def __init__(self, color):
        # inventory
        self.roads = []  # used for calculating longest road is a list of nodes
        self.color = color

        self.resources = {
            Resource.BRICK:99,
            Resource.SHEEP:99,
            Resource.STONE:99,
            Resource.WHEAT:99,
            Resource.WOOD:99
        }


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

        #adding these so player class can consult bank and dev cards
        #TODO: right now these are separate instances for each player.  We will need to create bank instance in main
        # and pass the same instance to each player, or create a global bank instance.
        # easily done in main gameBank = Bank(), then in player global gameBank
        #self.bank = Bank()
        #self.devCardStack = DevCardStack()

        # UI positional fields
        self.left = 0
        self.right = 0
        self.bottom = 0
        self.top = 0
        self.color_tab_width = 30
        self.resource_sprite_width = 0

        self.active_player = False
        self.game_state = None
        self.player_state = PlayerState.DEFAULT

        # UI elements
        self.show_resources = True # TODO: change this to False when done testing
        self.sprites = arcade.SpriteList()
        self.resource_sprites = {
            Resource.BRICK: arcade.Sprite("sprites/resources/brick.png"),
            Resource.SHEEP: arcade.Sprite("sprites/resources/sheep.png"),
            Resource.STONE: arcade.Sprite("sprites/resources/stone.png"),
            Resource.WHEAT: arcade.Sprite("sprites/resources/wheat.png"),
            Resource.WOOD: arcade.Sprite("sprites/resources/wood.png")
        }
        for s in self.resource_sprites.values():
            self.sprites.append(s)

        self.finish_turn_button = Button("Finish turn", Player.BUTTON_COLOR)
        self.trade_button = Button("Trade", Player.BUTTON_COLOR)
        self.reject_trade_button = Button("Reject", Player.BUTTON_COLOR)
        self.accept_trade_button = Button("Accept", Player.BUTTON_COLOR)

        self.view_dev_cards_button = Button("Show dev cards", Player.BUTTON_COLOR)
        self.view_dev_cards_button.on_click = Player.draw_view_dev_cards

        self.view_resources_button = Button("View resources", Player.BUTTON_COLOR)
        self.view_resources_button.on_click = Player.draw_player_resources

        self.finish_turn_button.on_click = Player.finish_turn_function
        self.trade_button.on_click = Player.trade_function

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


    def set_state(self, game_state):
        if game_state == GameState.ROLL:
            self.player_state = PlayerState.ROLL
        elif game_state == GameState.TRADE:
            self.player_state = PlayerState.ABLE_TO_TRADE
        elif game_state == GameState.BUILD:
            self.player_state = PlayerState.DEFAULT
        elif game_state == PlayerState.MENU:
            self.player_state = PlayerState.MENU

        self.finish_turn_button.set_visible(False)
        self.trade_button.set_visible(False)
        self.reject_trade_button.set_visible(False)
        self.accept_trade_button.set_visible(False)

        self.view_dev_cards_button.set_visible(False)
        self.view_resources_button.set_visible(False)


        #always able to view your cards
        #self.view_dev_cards_button.set_visible(True)

        if self.player_state == PlayerState.ABLE_TO_TRADE:
            self.trade_button.set_visible(True)
            self.finish_turn_button.set_visible(True)
            self.view_dev_cards_button.set_visible(True)
            self.view_resources_button.set_visible(True)

        elif self.player_state == PlayerState.TRADING:
            self.reject_trade_button.set_visible(True)
            self.accept_trade_button.set_visible(True)
            self.view_dev_cards_button.set_visible(True)
            self.view_resources_button.set_visible(True)

        elif self.player_state == PlayerState.DEFAULT:
            self.finish_turn_button.set_visible(True)
            self.view_dev_cards_button.set_visible(True)
            self.view_resources_button.set_visible(True)
        elif self.player_state == PlayerState.MENU:
            self.close_menu_button.set_visible(True)



    # positions the player representation UI and it's components on the screen
    def set_pos(self, l, r, b, t):
        self.left = l
        self.right = r
        self.bottom = b
        self.top = t

        usable_width = self.right - self.left - self.color_tab_width

        self.resource_sprite_width = usable_width / 8
        spacing = self.resource_sprite_width * 1.5

        x = self.left + self.resource_sprite_width
        y = self.top - self.resource_sprite_width

        #setting dev card button

        self.dev_card_stack_button.set_pos(self.dev_card_stack_button_params[0],
                                           self.dev_card_stack_button_params[1],
                                           self.dev_card_stack_button_params[2],
                                           self.dev_card_stack_button_params[3])

        for res, n in self.resources.items():
            self.resource_sprites[res].center_x = x
            self.resource_sprites[res].center_y = y
            self.resource_sprites[res].width = self.resource_sprite_width
            self.resource_sprites[res].height = self.resource_sprite_width
            x += spacing

        if self.active_player:
            button_height = (self.top - self.bottom) // 8
            button_width = usable_width * 0.4
            x1 = usable_width * 0.25
            x2 = usable_width * 0.75
            y = self.bottom + (button_height * 0.8)
            y2 = self.bottom + (3 * (button_height * 0.8))

            self.trade_button.set_pos(x1, y, button_width, button_height)
            self.reject_trade_button.set_pos(x1, y, button_width, button_height)
            self.finish_turn_button.set_pos(x2, y, button_width, button_height)
            self.accept_trade_button.set_pos(x2, y, button_width, button_height)

            self.view_dev_cards_button.set_pos(x1, y2, button_width, button_height)
            self.view_resources_button.set_pos(x2, y2, button_width, button_height)


    def add_road(self,start_node, end_node):
        if start_node not in self.roads:
            self.roads.append(start_node)
        if end_node not in self.roads:
            self.roads.append(end_node)

    def get_roads(self):
        return self.roads

    def add_resources(self, amts: dict):
        taken_from_bank = Player.bank.TakeResources(amts)
        for r, val in taken_from_bank.items():
            self.resources[r] += val

    #decrements resources if possible and returns true, else returns false
    def use_resources(self, amts: dict):
        for r, val in amts.items():
            if self.resources[r] - val < 0:
                return False
        for r, val in amts.items():
            self.resources[r] -= val
        #no idea if these are the same
        #Player.bank.ReturnResources(amts)
        self.bank.ReturnResources(amts)
        return True

    # returns True if the player owns at least a certain set of resources, and False otherwise
    def has_resources(self, amts: dict):
        for r, req in amts.items():
            if self.resources[r] < req:
                return False
        return True

    def get_color(self):
        return self.color

    # can build functions
    # return True is the player hasn't exceeded the limit per building and has the resources to build, and False otherwise
    # TODO: override limitations by resource if dev card owned
    def can_build_road(self):
        return (self.has_resources(self.ROAD_COST) and
                self.road_count < self.MAX_ROADS)

    def can_build_settlement(self):
        return (self.has_resources(self.SETTLEMENT_COST) and
                self.settlement_count < self.MAX_SETTLEMENTS)

    def can_build_city(self):
        return (self.has_resources(self.CITY_COST) and
                self.city_count < self.MAX_CITIES)

    def can_buy_dev_card(self):
        return self.has_resources(self.DEV_CARD_COST)

    # build functions
    # update the player's resources in the event that they build
    # return True if build is successful, and False otherwise
    # NOTE: these functions should not actually build things, they just update the player's resources
    def build_road(self, start_node, end_node):
        if self.can_build_road():
            self.use_resources(self.ROAD_COST)
            self.road_count += 1
            self.add_road(start_node, end_node)
            return True
        return False

    # TODO: connect board logic for valid build move
    def BuildRoad2(self, start_node, end_node):
        if self.UseResources(self.ROAD_COST):
            #build the road
            print("Road built")
        else:
            print("Not enough resources")

    def build_settlement(self):
        if self.can_build_settlement():
            self.use_resources(self.SETTLEMENT_COST)
            self.settlement_count += 1
            return True
        return False

    def BuildSettlement2(self):
        if self.UseResources(self.SETTLEMENT_COST):
            #build the settlement
            print("Settlement built")
        else:
            print("Not enough resources")

    def build_city(self):
        if self.can_build_city():
            self.use_resources(self.CITY_COST)
            self.city_count += 1
            self.settlement_count -= 1
            return True
        return False

    def BuildCity2(self):
        if self.UseResources(self.CITY_COST):
            print("City built")
        else:
            print("Not enough resources")

    def buy_dev_card(self):
        if self.can_buy_dev_card():
            self.use_resources(self.DEV_CARD_COST)
            return True
        return False

    def BuyDevCard(self):
        if self.use_resources(self.DEV_CARD_COST):
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
        arcade.draw_lrbt_rectangle_filled(self.left, self.right, self.bottom, self.top,
                                          Player.UI_COLOR)
        arcade.draw_lrbt_rectangle_outline(self.left, self.right, self.bottom, self.top,
                                           Player.UI_OUTLINE_COLOR, 6)
        arcade.draw_lrbt_rectangle_filled(self.right - self.color_tab_width, self.right + 3,
                                          self.bottom + 3, self.top - 3, self.color)

        #visible_points_text = arcade.Text(f"Victory Points: {self.visible_points}")

        #self.view_dev_cards_button.on_draw()
        # draw resources
        if self.show_resources:
            for res, n in self.resources.items():
                arcade.draw_text(f"x{n}", self.resource_sprites[res].center_x,
                                 self.resource_sprites[res].center_y - self.resource_sprite_width,
                                 arcade.color.BLACK, font_size=(self.resource_sprite_width / 3),
                                 anchor_x="center")

            self.sprites.draw()

        if self.active_player:
            self.finish_turn_button.on_draw()
            self.trade_button.on_draw()
            self.reject_trade_button.on_draw()
            self.accept_trade_button.on_draw()

            self.view_dev_cards_button.on_draw()
            self.view_resources_button.on_draw()
        else:
            pass

    def on_mouse_press(self, mouse_sprite):
        self.finish_turn_button.on_mouse_press(mouse_sprite)
        self.trade_button.on_mouse_press(mouse_sprite)
        self.reject_trade_button.on_mouse_press(mouse_sprite)
        self.accept_trade_button.on_mouse_press(mouse_sprite)

        self.view_dev_cards_button.on_mouse_press(mouse_sprite)
        self.view_resources_button.on_mouse_press(mouse_sprite)

        self.close_menu_button.on_mouse_press(mouse_sprite)

    def on_mouse_motion(self, mouse_sprite):
        self.finish_turn_button.on_mouse_motion(mouse_sprite)
        self.trade_button.on_mouse_motion(mouse_sprite)
        self.reject_trade_button.on_mouse_motion(mouse_sprite)
        self.accept_trade_button.on_mouse_motion(mouse_sprite)

        self.view_dev_cards_button.on_mouse_motion(mouse_sprite)
        self.view_resources_button.on_mouse_motion(mouse_sprite)

        self.close_menu_button.on_mouse_motion(mouse_sprite)

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

