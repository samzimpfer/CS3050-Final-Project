from enum import Enum
import random
from dataclasses import *

import arcade

# enums
class GameState(Enum):
    PLAYER_SELECT = 0
    BOT_SELECT = 1
    START_TURN = 2
    ROLL = 3
    TRADE = 4
    BUILD = 5
    ROBBER = 6
    WINNER = 7

INSTRUCTIONS = {
    GameState.START_TURN: "Place a settlement and then a road",
    GameState.ROLL: "Click the dice to roll",
    GameState.TRADE: "You may trade with other players or click on the board to build",
    GameState.ROBBER: "You've activated the robber by rolling a 7! Click any tile next to another "
                      "player's settlement and take a random resource from them",
}

class Resource(Enum):
    BRICK = 0
    SHEEP = 1
    STONE = 2
    WHEAT = 3
    WOOD = 4

# game constants
UI_COLOR = (75, 110, 150)
UI_OUTLINE_COLOR = (40, 80, 140)
BUTTON_COLOR = (40, 80, 140)
TEXT_COLOR = (255, 200, 10)

PLAYER_COLORS = [arcade.color.BLUE, arcade.color.GREEN, arcade.color.RED, arcade.color.YELLOW]
PLAYER_COLOR_NAMES = ["Blue", "Green", "Red", "Yellow"]

ROAD_COST = {
    Resource.BRICK:1,
    Resource.SHEEP:0,
    Resource.STONE:0,
    Resource.WHEAT:0,
    Resource.WOOD:1
}

SETTLEMENT_COST = {
    Resource.BRICK:1,
    Resource.SHEEP:1,
    Resource.STONE:0,
    Resource.WHEAT:1,
    Resource.WOOD:1
}

CITY_COST = {
    Resource.BRICK:0,
    Resource.SHEEP:0,
    Resource.STONE:3,
    Resource.WHEAT:2,
    Resource.WOOD:0
}

DEV_CARD_COST = {
    Resource.BRICK:0,
    Resource.SHEEP:1,
    Resource.STONE:1,
    Resource.WHEAT:1,
    Resource.WOOD:0
}


# All dev card types, basically structs.  Subclasses of DevCard.  Each has the number of them(amt), name, and description.
# functions like "show type" and "print description" can be added to the parent DevCard function.  May be best to remove
# @dataclass decorator if we decide to do this
@dataclass(frozen=True)
class DevCard:
    amt: int
    name: str
    description: str
    pathname: str
    pass

@dataclass(frozen=True)
class Knight(DevCard):
    amt = 14
    name = "Knight"
    description = "Move the robber. Steal one resource from the owner of a settlement or city adjacent to the robber’s new hex."
    pathname = "sprites/catan_knight_card.png"
    def __init__(self):
        super().__init__(Knight.amt, Knight.name, Knight.description, Knight.pathname)


@dataclass(frozen=True)
class RoadBuilding(DevCard):
    amt = 2
    name = "Road Building"
    description = "Place two new roads as if you had just built them."
    pathname = "sprites/road_building_card.png"
    def __init__(self):
        super().__init__(RoadBuilding.amt, RoadBuilding.name, RoadBuilding.description, RoadBuilding.pathname)


@dataclass(frozen=True)
class YearOfPlenty(DevCard):
    amt = 2
    name = "Year of Plenty"
    description = "Take any two resources from the bank. Add them to your hand. They can be two of the same resource or two different resources."
    pathname = "sprites/yearofplenty_card.jpeg"
    def __init__(self):
        super().__init__(YearOfPlenty.amt, YearOfPlenty.name, YearOfPlenty.description, YearOfPlenty.pathname)




@dataclass(frozen=True)
class Monopoly(DevCard):
    amt = 2
    name = "Monopoly"
    description = "When you play this card, announce one type of resource. All other players must give you all of their resources of that type."
    pathname = "sprites/monopoly_card.png"
    def __init__(self):
        super().__init__(Monopoly.amt, Monopoly.name, Monopoly.description, Monopoly.pathname)



@dataclass(frozen=True)
class University(DevCard):
    amt = 1
    name = "University"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."
    pathname = "sprites/university_card.png"
    def __init__(self):
        super().__init__(University.amt, University.name, University.description, University.pathname)



@dataclass(frozen=True)
class Market(DevCard):
    amt = 1
    name = "Market"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."
    pathname = "sprites/market_card.png"
    def __init__(self):
        super().__init__(Market.amt, Market.name, Market.description, Market.pathname)



@dataclass(frozen=True)
class GreatHall(DevCard):
    amt = 1
    name = "Great Hall"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."
    pathname = "sprites/greathall_card.jpeg"
    def __init__(self):
        super().__init__(GreatHall.amt, GreatHall.name, GreatHall.description, GreatHall.pathname)


@dataclass(frozen=True)
class Chapel(DevCard):
    amt = 1
    name = "Chapel"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."
    pathname = "sprites/chapel_card.jpg"
    def __init__(self):
        super().__init__(Chapel.amt, Chapel.name, Chapel.description, Chapel.pathname)



@dataclass(frozen=True)
class Library(DevCard):
    amt = 1
    name = "Library"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."
    pathname = "sprites/library_card.png"
    def __init__(self):
        super().__init__(Library.amt, Library.name, Library.description, Library.pathname)

# Resource bank, mostly necessary because resources can and do run out during the game
class Bank:
    # when initialized, there are 19 of each resource (95 cards total)
    def __init__(self):
        self.resourceDict = {
            Resource.BRICK:19,
            Resource.SHEEP:19,
            Resource.STONE:19,
            Resource.WHEAT:19,
            Resource.WOOD:19,
        }
        # self.Brick = 19
        # self.Sheep = 19
        # self.Stone = 19
        # self.Wheat = 19
        # self.Wood = 19
    
    # both Take and Return resources take amounts passed in as dictionary form.  This is also the return type for
    # TakeResources().  Take could be simplified but for now his is just a very true representation of what the process
    # would look like in game
    def TakeResources(self, amounts: dict) -> dict:
        #amounts passed in as dict with +/- values
        taken = {}
        for r, amount in amounts.items():
            #if a player tries to take more than what's available, the player only receives what's actually there and
            # the amount is set to 0
            if self.resourceDict[r] >= amount:
                amt = amount
                self.resourceDict[r] -= amount
                taken[r] = amt
            else:
                amt = self.resourceDict[r]
                self.resourceDict[r] = 0
                taken[r] = amt
        return taken

    def ReturnResources(self, amounts: dict):
        for r, amount in amounts.items():
            self.resourceDict[r] += amount



# Actual stack of Dev Cards
class DevCardStack:
    # when initialized, dev card instances are added to stack list and then shuffled.  the description and name can be
    # accessed using <Class Instance>.<data field>
    def __init__(self):
        self.stack = []
        # this iterates over subclasses of DevCard
        for card in DevCard.__subclasses__():
            self.stack += [card()] * card.amt
        random.shuffle(self.stack)
        self.stack.append(Monopoly())
        self.stack.append(YearOfPlenty())
        self.stack.append(Knight())

    # draw card pops from stack and returns an instance of a dev card.  For example each player class instance can use
    # "draw_new_dev_card = DevCardStack.DrawCard()" to give the player a new dev card while also updating what's left in
    # the deck
    def DrawCard(self) -> DevCard:
        return self.stack.pop()



