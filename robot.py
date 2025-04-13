from enum import Enum
from gameobjects import ROAD_COST, SETTLEMENT_COST, CITY_COST, DEV_CARD_COST
import random
# this plan will make the com player seek to expand and take control of as many possible resources focusing on settlement count and longest road
class Moves(Enum):
    BUILD_SETTLEMENT = 1
    BUILD_ROAD = 2
    BUILD_CITY = 3
    BUY_DEV_CARD = 4
    TRADE = 5
    PLAY_DEV_CARD = 6
    WAIT = 7

class Robot():
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.node_evaluations = []
        self.settlements = []# list of nodes that have settlements
        self.weights = []# list of values that control what the com does
        self.resource_types_weights = [0,0,0,0,0]# number of each resource tile you have
        self.action = None# the action that is queued up 
        self.action_location = None# where the action will take place if needed

    def play_first_turn(self):
        node, edge = self.plan_first_turns()
        self.build_settlement(node, True)
        self.build_road(self.board.get_edge(edge[0], edge[1]), True)
        
    def play_turn(self):
        self.plan_move()
        if self.action == Moves.BUILD_SETTLEMENT:
            self.build_settlement(self.action_location)
        elif self.action == Moves.BUILD_ROAD:
            self.build_road(self.action_location)
        elif self.action == Moves.BUILD_CITY:
            self.build_city(self.action_location)
        elif self.action == Moves.BUY_DEV_CARD:
            self.buy_dev_card()
        elif self.action == Moves.PLAY_DEV_CARD:
            self.play_dev_card()
        elif self.action == Moves.TRADE:
            self.trade()
        else:
            pass
        return 

    def plan_first_turns(self):
        inventory = self.player.return_inventory()
        best_node = None
        best_edge = None
        best_eval = 0
        for row in self.board.get_nodes():
            for node in row:
                if self.evaluate_node(node) > best_eval and not node.get_building() and node.has_space():
                    best_eval = self.evaluate_node(node)
                    best_node = node

        # find the best edge to build on
        best_eval = 0
        best_edge_backup = None# theres an error that sometimes returns best_edge as None
        for neighbor in best_node.get_connections():
            this_eval = 0
            best_edge_backup = [best_node, neighbor]
            this_eval += self.evaluate_node(neighbor)
            for n in neighbor.get_connections():
                if n != best_node and not n.get_building():
                    best_eval += self.evaluate_node(n) * 0.33
            if this_eval > best_eval:
                best_eval = this_eval 
                best_edge = [best_node, neighbor]
            
        if best_edge == None:
            return best_node, best_edge_backup

        return best_node, best_edge
                


    def plan_move(self):
        inventory = self.player.return_inventory()

        # checks if the player can be robbed if they have more than 7 cards
        can_be_robbed = False
        number_of_resource_cards = 0
        for _, value in inventory.items():
            number_of_resource_cards += value
        if number_of_resource_cards > 7:
            can_be_robbed = True
        
        # calculates how far from from the price of each item the player is or isnt 
        road_weights = self.distance_from_price(ROAD_COST)
        settlement_weights = self.distance_from_price(SETTLEMENT_COST)
        city_weights = self.distance_from_price(CITY_COST)
        dev_card_weights = self.distance_from_price(DEV_CARD_COST)



        return 
    
    def find_distance_to_destination(self):
        end_points = self.board.find_endpoints(self.player)
        for node in end_points:
            pass

    
    def find_road_destination(self):
        best_degree_2_node = None
        best_degree_2_eval = 0
        best_degree_3_node = None
        best_degree_3_eval = 0
        for node in self.settlements:
            for neighbor in node.get_connections():
                for degree_2_neigbor in neighbor.get_connections():
                    # scans two edges away
                    this_degree_2_eval = self.evaluate_node(degree_2_neigbor)
                    if this_degree_2_eval > best_degree_2_eval and degree_2_neigbor != neighbor:
                        best_degree_2_eval = this_degree_2_eval
                        best_degree_2_node = degree_2_neigbor
                    for degree_3_neighbor in degree_2_neigbor.get_connections():
                        # scans three edges away
                        this_degree_3_eval = self.evaluate_node(degree_3_neighbor)
                        if  this_degree_3_eval > best_degree_3_eval and degree_3_neighbor != degree_2_neigbor:
                            best_degree_3_eval = this_degree_3_eval
                            best_degree_3_node = degree_3_neighbor
        if best_degree_3_eval > best_degree_2_eval * 1.25:
            return best_degree_3_node
        else:
            return best_degree_2_node
                        
    
    # TODO: deal with it later
    def trade(self):
        pass

    # checks if the node is valid to build on and if it is worth it to build on
    def evaluate_node(self, node):
        # useless if someone has already built there 
        if node.get_building() and (node not in self.settlements):
            return -2 
        else:
            # almost useless if someone has built next to there
            settlements_next_door = [n for n in node.get_connections() if n.get_building() and (n not in self.settlements)]
            if settlements_next_door:
                return -1
            else:
                node_resources = [0,0,0,0,0]
                value_sum = 0
                resource_multiplier = 1
                opposition_score = 1
                for tile in node.get_adjacent_tiles():
                    if tile.get_resource() != "desert":
                        node_resources[tile.get_resource().value] += 1
                for tile in node.get_adjacent_tiles():
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
                    multiplier = 1
                    resource = tile.get_resource()
                    if resource != 'desert':
                        if resource == 0 and self.resources[0] < 2:
                            multiplier += 0.75
                        elif resource == 1 and self.resources[1] < 2:
                            multiplier += 0.325
                        elif resource == 2 and self.resources[2] < 2:
                            multiplier += 0.25
                        elif resource == 3 and self.resources[3] < 2:
                            multiplier += 0.325
                        elif resource == 4 and self.resources[4] < 2:
                            resource_multiplier += 0.75
                        # if there are no resources of this type, double the multiplier
                        if self.resource_types_weights[resource.value] == 0:
                            multiplier *= 2

                        if max(node_resources) == 2:
                            multiplier *= 0.7
                        elif max(node_resources) == 3:
                            multiplier *= 0.5

                        resource_multiplier += multiplier

                    else:
                        resource_multiplier *= 0.8
                if len(node.get_adjacent_tiles()) < 3:
                    if len(node.get_adjacent_tiles()) == 2:
                        resource_multiplier *= 0.9
                    else:
                        resource_multiplier *= 0.7
                for neighbor in node.get_connections():
                    # checks if there are any opposing player roads going to this node
                    if (self.board.get_edge(neighbor, node).get_road() != None and 
                    self.board.get_edge(neighbor, node).get_road() != self.player):
                        opposition_score += 1
                    for n in neighbor.get_connections():
                        # checks if any of the nodes two roads away have an opposing settlement or city
                        if n != node and (n.get_building() and n.get_building() != self.player) :
                            opposition_score += 0.5
                        # checks if there are any opposing player roads going into nodes one road away from this node
                        if (self.board.get_edge(neighbor, n).get_road() != None and
                        self.board.get_edge(neighbor, n).get_road() != self.player):
                            opposition_score += 0.5
                print("------------------")
                print(value_sum, resource_multiplier, opposition_score)
                print(value_sum * resource_multiplier / opposition_score)
                return value_sum * resource_multiplier / opposition_score 
    
    # calculates the distance from the price per resource then returns a list of distances 
    # if the distance is negative it means the player is over the cost of that resource
    def distance_from_price(self, purchase):
        distance_list = [0,0,0,0,0]# each index is a resources type
        inventory = self.player.return_inventory()
        for key, value in purchase.items():
            # if the value is less than the price it will add distance to the price
            # this distance is 
            if value > inventory[key]:
                this_distance = value - inventory[key]
                if self.resource_types_weights[key.value] >= 3:
                    this_distance *= 0.5
                elif self.resource_types_weights[key.value] < 1 and self.resource_types_weights[key.value] != 0:
                    this_distance *= 1.5
                distance_list[key.value] = -1 * this_distance
            elif value < inventory[key]:
                distance_list[key.value] = inventory[key]/value
                if distance_list[key.value] >= 2 and purchase != ROAD_COST:
                    # if the player has over double the cost square the distance 
                    distance_list[key.value] *=  distance_list[key.value]
        return distance_list
    
    def place_robber(self):
        best_tile = None
        best_eval = 0
        best_victims = []
        for tile in self.board.get_tiles():
            this_eval = 0
            these_victims = []
            if tile.has_robber():
                continue
            for node in tile.get_nodes():
                if node.get_building == self.player:
                    this_eval = -1000
                elif node.get_building():
                    these_victims.append(node.get_building())
                    this_eval += self.evaluate_node(node)

            if this_eval > best_eval:
                best_victims = these_victims
                best_tile = tile
                best_eval = this_eval
        
        self.board.bot_place_robber(best_tile)
        # randomly chooses a player 
        if len(best_victims):
            random.shuffle(best_victims)
            return best_victims[0]
        else:
            return None
        
                


    def play_dev_card(self):
        pass

    def build_road(self, edge, start_turn=False):
        self.board.bot_build_road(edge, self.player, start_turn=start_turn)

    def build_settlement(self, node, start_turn=False):
        tiles = node.get_adjacent_tiles()
        for tile in tiles:
            if tile.get_resource() != "desert":
                if tile.get_number() < 4 or tile.get_number() > 10:
                    self.resource_types_weights[tile.get_resource().value] += 0.5
                elif tile.get_number() == 8 or tile.get_number() == 6:
                    self.resource_types_weights[tile.get_resource().value] += 1.5
                else:
                    self.resource_types_weights[tile.get_resource().value] += 1
            self.settlements.append(node)
        if len(self.settlements) == 0:
            self.board.bot_build_settlement(node, self.player, start_turn=start_turn, is_first=True)
        self.board.bot_build_settlement(node, self.player, start_turn=start_turn)
        

    def build_city(self, node):
        if node not in self.settlements:
            return 
        for tile in node.get_adjacent_tiles():
            if tile.get_resource() != "desert":
                if tile.get_number() < 4 or tile.get_number() > 10:
                    self.resource_types_weights[tile.get_resource().value] += 0.5
                elif tile.get_number() == 8 or tile.get_number() == 6:
                    self.resource_types_weights[tile.get_resource().value] += 1.5
                else:
                    self.resource_types_weights[tile.get_resource().value] += 1

        self.player.build_city(node)
        

    def buy_dev_card(self):
        pass
