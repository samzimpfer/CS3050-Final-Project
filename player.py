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

class Player:

    def __init__(self,color):
        # inventory
        self.roads = []# used for calculating longest road is a list of nodes
        self.color = color
        self.sheepCount = 0
        self.woodCount = 0
        self.brickCount = 0
        self.oreCount = 0
        self.wheatCount = 0

        self.knightCardCount = 0
        # add other dev card counters here

        self.settlementCount = 0
        self.cityCount = 0

        self.hasLongestRoad = False


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

    def get_color(self):
        return self.color


    # can build functions
    # return True is the player has the resources to build things, and False otherwise
    def canBuildRoad(self):
        return self.brickCount >= 1 and self.woodCount >= 1

    def canBuildSettlement(self):
        return self.brickCount >= 1 and self.woodCount >= 1 and self.sheepCount >= 1 and self.wheatCount >= 1

    def canBuildCity(self):
        return self.oreCount >= 3 and self.wheatCount >= 2

    def canBuyDevCard(self):
        return self.sheepCount >= 1 and self.oreCount >= 1 and self.wheatCount >= 1


    # build functions
    # update the player's resources in the event that they build
    # return True if build is successful, and False otherwise
    def buildRoad(self, start_node, end_node):
        if self.canBuildRoad():
            self.brickCount -= 1
            self.woodCount -= 1
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

        return total
