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
from pygame.examples.music_drop_fade import play_file
from gameobjects import *


class Player:

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15


    #testing this out, not even sure if it works
    global Bank
    global GameDevCards

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
        self.roads = []# used for calculating longest road is a list of nodes
        self.color = color
        self.sheepCount = 0
        self.woodCount = 0
        self.brickCount = 0
        self.oreCount = 0
        self.wheatCount = 0

        self.resources = {
            Resource.BRICK:0,
            Resource.SHEEP:0,
            Resource.STONE:0,
            Resource.WHEAT:0,
            Resource.WOOD:0,
        }

        self.knightCardCount = 0
        # add other dev card fields here

        self.playerDevCards = []


        self.settlementCount = 0
        self.cityCount = 0
        self.roadCount = 0

        self.hasLongestRoad = False
        self.hasLargestArmy = False

        self.victoryPoints = 0

        #adding these so player class can consult bank and dev cards
        #TODO: right now these are separate instances for each player.  We will need to create bank instance in main
        # and pass the same instance to each player, or create a global bank instance.
        # easily done in main gameBank = Bank(), then in player global gameBank
        #self.bank = Bank()
        #self.devCardStack = DevCardStack()


    def add_road(self,edge):
        start_node = edge.get_start_node()
        end_node = edge.get_end_node()
        if start_node not in self.roads:
            self.roads.append(start_node)
        if end_node not in self.roads:
            self.roads.append(end_node)

    def get_roads(self):
        return self.roads

    # increment resource functions
    def addSheep(self, amt):
        self.sheepCount += amt

    def addWood(self, amt):
        self.woodCount += amt

    def addBrick(self, amt):
        self.brickCount += amt

    def addOre(self, amt):
        self.oreCount += amt

    def addWheat(self, amt):
        self.wheatCount += amt

    def AddResources(self, amts: dict):
        taken_from_bank = self.Bank.TakeResources(amts)
        for r, val in taken_from_bank.items():
            self.resources[r] += val

    # decrement resource functions
    def useSheep(self, amt):
        self.sheepCount -= amt

    def useWood(self, amt):
        self.woodCount -= amt

    def useBrick(self, amt):
        self.brickCount -= amt

    def useOre(self, amt):
        self.oreCount -= amt

    def useWheat(self, amt):
        self.wheatCount -= amt

    #decrements resources if possible and returns true, else returns false
    def UseResources(self, amts: dict):
        for r, val in amts.items():
            if self.resources[r] - val < 0:
                return False
        for r, val in amts.items():
            self.resources[r] -= val
        self.Bank.ReturnResources(amts)
        return True


    def get_color(self):
        return self.color


    # can build functions
    # return True is the player hasn't exceeded the limit per building and has the resources to build, and False otherwise
    # TODO: override limitations by resource if dev card owned
    def canBuildRoad(self):
        return self.roadCount < Player.MAX_ROADS and self.brickCount >= 1 and self.woodCount >= 1

    def canBuildSettlement(self):
        return self.settlementCount < Player.MAX_SETTLEMENTS and self.brickCount >= 1 and self.woodCount >= 1 and self.sheepCount >= 1 and self.wheatCount >= 1

    def canBuildCity(self):
        return self.cityCount < Player.MAX_CITIES and  self.oreCount >= 3 and self.wheatCount >= 2

    def canBuyDevCard(self):
        return self.sheepCount >= 1 and self.oreCount >= 1 and self.wheatCount >= 1


    # build functions
    # update the player's resources in the event that they build
    # return True if build is successful, and False otherwise
    def buildRoad(self, start_node, end_node):
        if self.canBuildRoad():
            self.brickCount -= 1
            self.woodCount -= 1

            self.roadCount += 1
            return True
        return False

    # TODO: connect board logic for valid build move
    def BuildRoad2(self, start_node, end_node):
        if self.UseResources(self.ROAD_COST):
            #build the road
            print("Road built")
        else:
            print("Not enough resources")



    def buildSettlement(self):
        if self.canBuildSettlement():
            self.brickCount -= 1
            self.woodCount -= 1
            self.sheepCount -= 1
            self.wheatCount -= 1

            self.settlementCount += 1
            return True
        return False

    def BuildSettlement2(self):
        if self.UseResources(self.SETTLEMENT_COST):
            #build the settlement
            print("Settlement built")
        else:
            print("Not enough resources")

    def buildCity(self):
        if self.canBuildCity():
            self.oreCount -= 3
            self.wheatCount -= 2

            self.cityCount += 1
            self.settlementCount -= 1
            return True
        return False

    def BuildCity2(self):
        if self.UseResources(self.CITY_COST):
            print("City built")
        else:
            print("Not enough resources")

    def buyDevCard(self):
        if self.canBuyDevCard():
            self.sheepCount -= 1
            self.oreCount -= 1
            self.wheatCount -= 1
            return True
        return False

    def BuyDevCard(self):
        if self.UseResources(self.DEV_CARD_COST):
            drawn_dev_card = GameDevCards.DrawCard()
            print(f"{drawn_dev_card.name}: {drawn_dev_card.description}")
            match drawn_dev_card:
                case Knight():
                    #TODO: add move robber
                    self.knightCardCount += 1
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
            self.playerDevCards.append(GameDevCards.DrawCard())


    # sets the value of hasLongestRoad for this player
    def setLongestRoad(self, value):
        self.hasLongestRoad = value


    # returns the number of points the player has based on settlements, cities, and longest road
    def getPoints(self):
        total = 0
        total += self.settlementCount
        total += (self.cityCount * 2)
        if self.hasLongestRoad:
            total += 2
        if self.hasLargestArmy:
            total += 2
        # add in victory card points

        return total
