from enum import Enum

class Resource(Enum):
    BRICK = 0
    SHEEP = 1
    STONE = 2
    WHEAT = 3
    WOOD = 4

# All dev card types
@dataclass(frozen=True)
class DevCard:
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

class Bank():
    def __init__(self):
        self.Brick = 19
        self.Sheep = 19
        self.Stone = 19
        self.Wheat = 19
        self.Wood = 19

    def TakeResources(self, amounts) -> dict:
        #amounts passed in as dict with +/- values
        taken = {}
        for r, amount in amounts.items():
            #if a player tries to take more than what's available, the player only receives what's actually there and
            # the amount is set to 0
            if self.r >= amount:
                amt = amount
                self.r -= amount
                taken[r] = amt
            else:
                amt = self.r
                self.r = 0
                taken[r] = amt
        return taken

    def ReturnResources(self, amounts):
        for r, amount in amounts.items():
            for r, amount in amounts.items():
                self.r += amount



class DevCardStack():
    def __init__(self):
        self.stack = []
        for card in DevCard.__subclasses__():
            self.stack += [card()] * card.amt
        self.stack = shuffle(self.stack)


    def DrawCard(self) -> DevCard:
        return self.stack.pop()



