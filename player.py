from node import Node
from gameobjects import *

class Player:
    def __init__(self, id, points, resources, VictoryCards, nodes, edges):
        self.id = id
        self.points = 0
        self.resources = {
            BRICK:0,
            SHEEP:0,
            STONE:0,
            WHEAT:0,
            WOOD:0
        }
        self.VictoryCards = []
        self.nodes = []
        self.edges = []

    def SetID(self, n):
        self.id = n
        
    def UpdateHand(self, IncDict, DecDict):
        for resource, value in IncDict.items():
            self.resources[resource] += value
        for resource, value in DecDict.items():
            self.resources[resource] -= value
            
    def UpdateVictoryPoints(self, n):
        # for cards in vcards, calc points
        # also calc other stuff like settlements, cities, etc

    def AddVictoryCard(self, VictoryCard):
        self.VictoryCards.append(VictoryCard)

    def RemoveVictoryCard(self, VictoryCard):
        self.VictoryCards.remove(VictoryCard)

    #TODO: not sure how to implement building node.  I think the best way would be to have the node as part of the board,
    # then players have ownership of node.  this way it's more straightforward for each player to check for a valid move
    def BuildNode(self, loc_x, loc_y):
        self.nodes.append(Node(loc_x, loc_y)) #placeholder
    #same deal
    def BuildEdge(self, loc_x, loc_y):
        self.edges.append(Edge(loc_x, loc_y))
        
    def CollectResources(self, roll):
        #for loop checks nodes, collects based on what node has. again based on how we want to structure player node interaction