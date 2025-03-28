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

# TODO: convert all camelcase to snakecase for pep 8 purposes
class Player:

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15

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
            Resource.BRICK:1,
            Resource.SHEEP:0,
            Resource.STONE:0,
            Resource.WHEAT:0,
            Resource.WOOD:1
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

        # UI elements
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

        self.finish_turn_button = Button("Finish turn", (40, 80, 140))


    def add_road(self,edge):
        start_node = edge.get_start_node()
        end_node = edge.get_end_node()
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
        Player.bank.ReturnResources(amts)
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

    def set_active_player(self, ap):
        self.active_player = ap

    def set_pos(self, l, r, b, t):
        self.left = l
        self.right = r
        self.bottom = b
        self.top = t

        if self.active_player:
            self.resource_sprite_width = (self.right - self.left - self.color_tab_width) / 8
            spacing = self.resource_sprite_width * 1.5

            x = self.left + self.resource_sprite_width
            y = self.top - self.resource_sprite_width
            for res, n in self.resources.items():
                self.resource_sprites[res].center_x = x
                self.resource_sprites[res].center_y = y
                self.resource_sprites[res].width = self.resource_sprite_width
                self.resource_sprites[res].height = self.resource_sprite_width
                x += spacing

            button_height = (self.top - self.bottom) // 8
            button_width = button_height * 4
            x = (self.right - self.left - self.color_tab_width) // 2
            y = self.bottom + (button_height * 0.8)
            self.finish_turn_button.set_pos(x, y, button_width, button_height)

    def on_draw(self):
        # draw player representation
        arcade.draw_lrbt_rectangle_filled(self.left, self.right, self.bottom, self.top,
                                          (75, 110, 150))
        arcade.draw_lrbt_rectangle_outline(self.left, self.right, self.bottom, self.top,
                                           (40, 80, 140), 6)
        arcade.draw_lrbt_rectangle_filled(self.right - self.color_tab_width, self.right + 3,
                                          self.bottom + 3, self.top - 3, self.color)

        if self.active_player:
            # draw resources
            for res, n in self.resources.items():
                arcade.draw_text(f"x{n}", self.resource_sprites[res].center_x,
                                 self.resource_sprites[res].center_y - self.resource_sprite_width,
                                 arcade.color.BLACK, font_size=(self.resource_sprite_width / 3),
                                 anchor_x="center")

            self.sprites.draw()

            self.finish_turn_button.on_draw()
        else:
            pass

    def on_mouse_press(self, mouse_sprite):
        self.finish_turn_button.on_mouse_press(mouse_sprite)

    def on_mouse_motion(self, mouse_sprite):
        self.finish_turn_button.on_mouse_motion(mouse_sprite)