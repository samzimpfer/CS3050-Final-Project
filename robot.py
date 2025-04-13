from enum import Enum
import random
from gameobjects import *
from inventory import Inventory


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
        self.settlements = []# list of nodes that have settlements
        self.resource_types_weights = [0,0,0,0,0]# number of each resource tile you have
        self.actions = []# the action that is queued up 
        self.road_plans = []
        self.planned_settlement = None
        self.planned_city = None

    def play_first_turn(self):
        node, edge = self.plan_first_turns()
        self.build_settlement(node, True)
        self.build_road(self.board.get_edge(edge[0], edge[1]), True)
        
    def play_turn(self):
        self.plan_move()
        for action in self.actions:
            match action[0]:
                case Moves.BUILD_SETTLEMENT:
                    self.build_settlement(action[1])
                case Moves.BUILD_ROAD:
                    self.build_road(action[1])
                case Moves.BUILD_CITY:
                    self.build_city(action[1])
                case Moves.TRADE:
                    self.trade(action[1])
                case Moves.WAIT:
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
        self.road_plans = []
        self.actions = []
        # checks if the player can be robbed if they have more than 7 cards
        can_be_robbed = False
        number_of_resource_cards = 0
        for _, value in inventory.items():
            number_of_resource_cards += value
        if number_of_resource_cards > 7:
            can_be_robbed = True
        
        # calculates how far from from the price of each item the player is or isnt 
        settlement_distance_weights = self.distance_from_price_relative(SETTLEMENT_COST)
        city_distance_weights = self.distance_from_price_relative(CITY_COST)
        dev_card_weights = self.distance_from_price_relative(DEV_CARD_COST)

        settlement_distance = 0
        for value in settlement_distance_weights:
            if value < 0:
                settlement_distance += value

        city_distance = 0
        for value in city_distance_weights:
            if value < 0:
                city_distance += value

        
        #find destination
        city_location = self.evaluate_city_locations()
        destination = self.find_road_destination()
        path = None

        if self.planned_settlement and settlement_distance > -2:
            self.actions.append([Moves.BUILD_SETTLEMENT, self.planned_settlement])

        elif self.player.can_build_road():
            if self.resource_types_weights[0] == 0:
                path = self.find_path_to_resource(Resource.BRICK)
            elif self.resource_types_weights[4] == 0:
                path = self.find_path_to_resource(Resource.WOOD)
            else:
                path = self.find_path_to_destination(destination)

            if path:
                for i in range(len(path) - 1):
                    self.road_plans.append(self.board.get_edge(path[i], path[i+1]))
            
            for i in range(len(self.road_plans)):
                self.actions.append([Moves.BUILD_ROAD, self.road_plans[i]])

        if city_distance > -2 and city_location:
            self.actions.append([Moves.BUILD_CITY, city_location])

        if len(self.actions):
            if self.actions[0][0] == Moves.BUILD_CITY:
                self.actions.append([Moves.TRADE, CITY_COST])
            elif self.actions[0][0] == Moves.BUILD_SETTLEMENT:
                self.actions.append([Moves.TRADE, SETTLEMENT_COST])
            elif self.actions[0][0] == Moves.BUILD_ROAD:
                self.actions.append([Moves.TRADE, ROAD_COST])
        self.actions.append([Moves.WAIT, None])


    def evaluate_city_locations(self):
        best_eval = 0
        best_location = None
        for node in self.settlements:
            this_eval = self.evaluate_node(node, opposition=False)
            if this_eval > best_eval:
                best_location = node
                best_eval = this_eval

        return best_location
    
    def evaluate_settlement_locations(self):
        for node in self.player.get_roads():
            if node.has_space():
                pass

    
    def find_path_to_destination(self, destination):
        end_points = self.board.find_endpoints(self.player)
        for node in end_points:
            for neighbor in node.get_connections():
                for degree_2_neighbor in neighbor.get_connections():
                    if degree_2_neighbor.get_building():
                        continue
                    elif degree_2_neighbor == destination:
                        return [node, neighbor, degree_2_neighbor]
                    for degree_3_neighbor in degree_2_neighbor.get_connections():
                        if degree_3_neighbor.get_building():
                            continue
                        elif degree_3_neighbor == destination:
                            return [node, neighbor, degree_2_neighbor, degree_3_neighbor]
        return
                        
    def find_path_to_resource(self, resource):
        best_node = None
        best_score = 0
        degree_2_path = []
        degree_3_path = []
        best_degree_2_score = 0
        best_degree_3_score = 0
        for node in self.board.find_endpoints(self.player):
            for neighbor in node.get_connections():
                for degree_2_neighbor in neighbor.get_connections():
                    if not degree_2_neighbor.has_space() or degree_2_neighbor == node:
                        continue
                    else:
                        for tile in degree_2_neighbor.get_adjacent_tiles():
                            if tile.get_resource() == resource:
                                this_degree_2_score = tile.get_number()
                                if this_degree_2_score > best_degree_2_score:
                                    best_degree_2_score = this_degree_2_score
                                    degree_2_path = [node, neighbor, degree_2_neighbor]
                    for degree_3_neighbor in degree_2_neighbor.get_connections():
                        if not degree_3_neighbor.has_space() or degree_3_neighbor == neighbor:
                            continue
                        else:
                            for tile in degree_3_neighbor.get_adjacent_nodes():
                                if tile.get_resource() == resource:
                                    this_degree_3_score = tile.get_resource()
                                    if this_degree_3_score > best_degree_3_score:
                                        this_degree_3_score = tile.get_number()
                                        degree_3_path = [node, neighbor, degree_2_neighbor, degree_3_neighbor]
        
        if best_degree_3_score > best_degree_2_score * 1.25:
            return degree_3_path
        else:
            return degree_2_path

                        
    def get_value_score(self, n):
        return 7 - abs(7 - n)



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
                    if this_degree_2_eval > best_degree_2_eval and degree_2_neigbor != node and not degree_2_neigbor.has_space():
                        best_degree_2_eval = this_degree_2_eval
                        best_degree_2_node = degree_2_neigbor
                    for degree_3_neighbor in degree_2_neigbor.get_connections():
                        # scans three edges away
                        this_degree_3_eval = self.evaluate_node(degree_3_neighbor)
                        if  this_degree_3_eval > best_degree_3_eval and degree_3_neighbor != neighbor and not degree_3_neighbor.has_space():
                            best_degree_3_eval = this_degree_3_eval
                            best_degree_3_node = degree_3_neighbor
        if best_degree_3_eval > best_degree_2_eval * 1.25:
            return best_degree_3_node
        else:
            return best_degree_2_node

    # TODO: could add additional price arguments for future turns in this
    def trade(self, price):
        get = self.player.get_inventory
        give = self.player.give_inventory

        # TODO: test distance_from_price_absolute to make sure it works right
        needed = self.distance_from_price_absolute(price)
        self.player.open_trade()
        get.set_amounts(needed) # this function automatically ignores negatives

        # loop to set give inventory to same cardinality of unneeded resources
        while give.get_total_amount() < get.get_total_amount():
            change = Inventory.ALL_ZERO.copy()
            min_key = Resource.BRICK
            min_val = needed[Resource.BRICK]
            # add the most abundant resource at each pass to the give inventory
            for t, r in needed.items():
                if r < min_val:
                    min_key = t
                    min_val = r
            change[min_key] = 1
            give.change_amounts(change)

        # this should open a trade to any players who can trade



    # checks if the node is valid to build on and if it is worth it to build on
    def evaluate_node(self, node, opposition=True):
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
                    if tile.get_number():
                        value_sum += self.get_value_score(tile.get_number())

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
                # dont need to care about the opposition when building a city
                if opposition:
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
    def distance_from_price_relative(self, purchase):
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
        
                


    def distance_from_price_absolute(self, purchase):
        distance_dict = {}
        inventory = self.player.return_inventory()
        for key, value in purchase.items():
            distance_dict[key] = value - inventory[key]
        return distance_dict


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
