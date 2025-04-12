from enum import Enum
from gameobjects import ROAD_COST, SETTLEMENT_COST, CITY_COST, DEV_CARD_COST
# this plan will make the com player seek to expand and take control of as many possible resources focusing on settlement count and longest road
class Moves(Enum):
    BUILD_SETTLEMENT = 1
    BUILD_ROAD = 2
    BUILD_CITY = 3
    BUY_DEV_CARD = 4
    TRADE = 5
    PLAY_DEV_CARD = 6
    WAIT = 7

class AggressivePlan():
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.node_evaluations = []
        self.settlements = []# list of nodes that have settlements
        self.weights = []# list of values that control what the com does
        self.resource_types_weights = [0,0,0,0,0]# number of each resource tile you have

    def play_turn(self, action):
        pass

    def plan_move(self):
        # calculates how far from from the price of each item the player is or isnt 
        distances = {
            ROAD_COST: self.distance_from_price(ROAD_COST),
            SETTLEMENT_COST: self.distance_from_price(SETTLEMENT_COST),
            CITY_COST: self.distance_from_price(CITY_COST),
            DEV_CARD_COST: self.distance_from_price(DEV_CARD_COST)
        }
        

    
    # finds and evaluates all nodes that are one road segment from accessable nodes
    def evaluate_boardering_nodes(self):
        boardering_nodes = [[],[]]
        for node in self.player.get_roads():
            for neighbor in node.get_connections():
                if neighbor != node:
                    boardering_nodes.append(neighbor)
        return boardering_nodes
    
    # finds and evaluates nodes that do not have three roads going into them
    def evaluate_incomplete_edges(self):
        incomplete_edges = [[],[]]
        for node in self.player.get_roads():
            count = []
            for n in node.get_connections():
                if self.board.get_edge(node, n).get_road() == None:
                    count.append(n)
            if len(count) < 3:
                for n in count:
                    incomplete_edges[0].append([node, n])

        return incomplete_edges

    # finds and evaluates the nodes that are connected to roads and valid to build on
    def evaluate_buildable_nodes(self):
        buildable_nodes = [[],[]]# index 0 is the nodes and index 1 is the evaluation of the node in index 0 
        for node in self.player.get_roads():
            if node.get_building() == None and node.has_space():
                buildable_nodes[0].append(node)
        for node in buildable_nodes[0]:
            pass
    
    # TODO: deal with it later
    def trade(self):
        pass

    # checks if the node is valid to build on and if it is worth it to build on
    def evaluate_node(self, node, is_setup=False):
        # useless if someone has already built there 
        if node.get_building() and (node not in self.settlements or node not in self.cities):
            return -2 
        else:
            # almost useless if someone has built next to there
            settlements_next_door = [n for n in node.get_connections() if n.get_building() and (n not in self.settlements or n not in self.cities)]
            if settlements_next_door:
                return -1
            else:
                value_sum = 0
                resource_multiplier = 1
                opposition_score = 1
                for tile in node.get_adjacentTiles():
                    # adds the number of dice configurations 
                    # that can make the number to the value_sum
                    number = tile.get_number()
                    if number == 2 or number == 12:
                        value_sum += 2
                    elif number == 3 or number == 11:
                        value_sum += 3
                    elif number == 4 or number == 10:
                        value_sum += 4
                    elif number == 5 or number == 9:
                        value_sum += 5
                    else:
                        value_sum += 6

                    # adds to the resource_multiplier depending on the resource type and how many are possed
                    # higher weights for wood and brick so they can expand faster
                    multiplier = 0
                    resource = tile.get_resource()
                    if resource != 'desert':
                        if resource == 0 and self.resources[0] < 2:
                            multiplier += 0.5
                        elif resource == 1 and self.resources[1] < 2:
                            resource_multiplier += 0.325
                        elif resource == 2 and self.resources[2] < 2:
                            resource_multiplier += 0.25
                        elif resource == 3 and self.resources[3] < 2:
                            resource_multiplier += 0.325
                        elif resource == 4 and self.resources[4] < 2:
                            resource_multiplier += 0.5
                        # if there are no resources of this type, double the multiplier
                        if self.resource_types_weights[resource.value] == 0:
                            multiplier *= 2

                        resource_multiplier += multiplier

                        if tile.has_robber() and not self.player.has_knight():
                            resource_multiplier = resource_multiplier * 0.5

                for neighbor in node.get_connections():
                    # checks if there are any opposing player roads going to this node
                    if (self.board.get_edge(neighbor, node).get_road() != None and 
                    self.board.get_edge(neighbor, node).get_road() != self.player):
                        opposition_score += 2
                    for n in neighbor.get_connections():
                        # checks if any of the nodes two roads away have an opposing settlement or city
                        if n != node and (n.get_building() and n.get_building() != self.player) :
                            opposition_score += 2
                        # checks if there are any opposing player roads going into nodes one road away from this node
                        if (self.board.get_edge(neighbor, n).get_road() != None and
                        self.board.get_edge(neighbor, n).get_road() != self.player):
                            opposition_score += 2
                print("-----------------------------")
                print([value_sum, resource_multiplier, opposition_score])
                print(value_sum / opposition_score * resource_multiplier)


    # finds the nodes with the highest evaluation and builds there
    def opening_move(self):
        pass
    
    # calculates a distance from the price of some item. 
    # The distance based on how many of each resource is needed and the resource_type_weights
    # returns negative is the purchase is possible 
    def distance_from_price(self, purchase):
        distance = 0
        inventory = self.player.return_inventory()
        overkill_count = 0# the number of resources where the player has double the price
        for key, value in purchase.items():
            # if the value is less than the price it will add distance to the price
            # this distance is 
            if value > inventory[key]:
                this_distance = purchase[key] - value
                if self.resource_types_weights[key.value] >= 3:
                    this_distance *= 0.5
                elif self.resource_types_weights[key.value] < 1 and self.resource_types_weights[key.value] != 0:
                    this_distance *= 1.5
                distance += this_distance
            if value * 2 <= inventory[key]:
                overkill_count += 1
        if overkill_count == len(purchase):
            return -1
                
        return distance


    def play_dev_card(self):
        pass

    def build_road(self, edge):
        self.player.build_road(edge)

    def build_settlement(self, node):
        tiles = node.get_adjacentTiles()
        for tile in tiles:
            if tile.get_resource():
                if tile.get_number() < 4 or tile.get_number() > 10:
                    self.resource_types_weights[tile.get_resource().value] += 0.5
                elif tile.get_number() == 8 or tile.get_number() == 6:
                    self.resource_types_weights[tile.get_resource().value] += 1.5
                else:
                    self.resource_types_weights[tile.get_resource().value] += 1
            self.settlements.append(node)
        self.player.build_settlement(node)

    def build_city(self, node):
        if node not in self.settlements:
            return 
        for tile in node.get_adjacentTiles():
            if tile.get_resource():
                if tile.get_number() < 4 or tile.get_number() > 10:
                    self.resource_types_weights[tile.get_resource().value] += 0.5
                elif tile.get_number() == 8 or tile.get_number() == 6:
                    self.resource_types_weights[tile.get_resource().value] += 1.5
                else:
                    self.resource_types_weights[tile.get_resource().value] += 1

        self.player.build_city(node)
        

    def buy_dev_card(self):
        pass
