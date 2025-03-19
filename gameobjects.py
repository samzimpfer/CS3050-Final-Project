from enum import Enum

class Resource(Enum):
    BRICK = 0
    SHEEP = 1
    STONE = 2
    WHEAT = 3
    WOOD = 4


@dataclass(frozen=True)
class Knight():
    amt = 14
    description = ""

@dataclass(frozen=True)
class 

class Bank():
    def __init__(self):
        self.Brick = 19
        self.Sheep = 19
        self.Stone = 19
        self.Wheat = 19
        self.Wood = 19

    def TakeResources(self, amounts):
        #amounts passed in as dict with +/- values
        for r, amount in amounts.items():
            #if a player tries to take more than what's available, the player only receives what's actually there and
            # the amount is set to 0
            if self.r >= amount:
                amt = amount
                self.r -= amount
                return amt
            else:
                amt = self.r
                self.r = 0
                return amt

    def ReturnResources(self, amounts):
        for r, amount in amounts.items():
            for r, amount in amounts.items():
                self.r += amount

class DevCards():
    def __init__(self):


