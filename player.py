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


class Player:

    MAX_SETTLEMENTS = 5
    MAX_CITIES = 4
    MAX_ROADS = 15

    def __init__(self):
        # inventory
        self.sheepCount = 0
        self.woodCount = 0
        self.brickCount = 0
        self.oreCount = 0
        self.wheatCount = 0

        self.knightCardCount = 0
        # add other dev card fields here

        self.settlementCount = 0
        self.cityCount = 0
        self.roadCount = 0

        self.hasLongestRoad = False
        self.hasLargestArmy = False


    # increment resource functions
    def addSheep(self, amt):
        self.sheepCount += amt

    def addWood(self, amt):
        self.woodCount += amt

    def addBrick(self, amt):
        self.brickCount += amt

    def addOre(self, amt):
        self.oreCount += amt

    def useWheat(self, amt):
        self.wheatCount += amt


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
    def buildRoad(self):
        if self.canBuildRoad():
            self.brickCount -= 1
            self.woodCount -= 1

            self.roadCount += 1
            return True
        return False

    def buildSettlement(self):
        if self.canBuildSettlement():
            self.brickCount -= 1
            self.woodCount -= 1
            self.sheepCount -= 1
            self.wheatCount -= 1

            self.settlementCount += 1
            return True
        return False

    def buildCity(self):
        if self.canBuildCity():
            self.oreCount -= 3
            self.wheatCount -= 2

            self.cityCount += 1
            self.settlementCount -= 1
            return True
        return False

    def buyDevCard(self):
        if self.canBuyDevCard():
            self.sheepCount -= 1
            self.oreCount -= 1
            self.wheatCount -= 1
            return True
        return False


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
