from enum import Enum
import random
from dataclasses import *

class GameState(Enum):
    SETUP = 0
    ROLL = 1
    TRADE = 2
    BUILD = 3

# haven't used this yet but whatever
class Resource(Enum):
    BRICK = 0
    SHEEP = 1
    STONE = 2
    WHEAT = 3
    WOOD = 4


# All dev card types, basically structs.  Subclasses of DevCard.  Each has the number of them(amt), name, and description.
# functions like "show type" and "print description" can be added to the parent DevCard function.  May be best to remove
# @dataclass decorator if we decide to do this
@dataclass(frozen=True)
class DevCard:
    amt: int
    name: str
    description: str
    pass

@dataclass(frozen=True)
class Knight():
    amt = 14
    name = "Knight"
    description = "Move the robber. Steal one resource from the owner of a settlement or city adjacent to the robber’s new hex."

@dataclass(frozen=True)
class RoadBuilding():
    amt = 2
    name = "Road Building"
    description = "Place two new roads as if you had just built them."

@dataclass(frozen=True)
class YearOfPlenty():
    amt = 2
    name = "Year of Plenty"
    description = "Take any two resources from the bank. Add them to your hand. They can be two of the same resource or two different resources."

@dataclass(frozen=True)
class Monopoly():
    amt = 2
    name = "Monopoly"
    description = "When you play this card, announce one type of resource. All other players must give you all of their resources of that type."

@dataclass(frozen=True)
class University():
    amt = 1
    name = "University"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."

@dataclass(frozen=True)
class Market():
    amt = 1
    name = "Market"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."

@dataclass(frozen=True)
class GreatHall():
    amt = 1
    name = "Great Hall"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."

@dataclass(frozen=True)
class Chapel():
    amt = 1
    name = "Chapel"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."

@dataclass(frozen=True)
class Library():
    amt = 1
    name = "Library"
    description = "One victory point. Reveal this card on your turn if, with it, you reach the number of points required for victory."

# Resource bank, mostly necessary because resources can and do run out during the game
class Bank():
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
class DevCardStack():
    # when initialized, dev card instances are added to stack list and then shuffled.  the description and name can be
    # accessed using <Class Instance>.<data field>
    def __init__(self):
        self.stack = []
        # this iterates over subclasses of DevCard
        for card in DevCard.__subclasses__():
            self.stack += [card()] * card.amt
        random.shuffle(self.stack)

    # draw card pops from stack and returns an instance of a dev card.  For example each player class instance can use
    # "draw_new_dev_card = DevCardStack.DrawCard()" to give the player a new dev card while also updating what's left in
    # the deck
    def DrawCard(self) -> DevCard:
        return self.stack.pop()



