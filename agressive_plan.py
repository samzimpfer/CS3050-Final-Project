# this plan will make the com player seek to expand and take control of as many possible resources focusing on settlement count and longest road
class AggressivePlan():
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.node_evaluations = []
        self.settlements = []# list of nodes that have settlements
        self.cities = []# list of nodes that have cities
        self.weights = []# list of values that control what the com does
        self.resource_tiles = [0,0,0,0,0]# number of each resource tile you have

    def play_turn(self):
        pass

    def next_move(self):
        if self.player.can_build_road():
            pass

    def trade(self):
        pass

    # checks if the node is valid to build on and if it is worth it to build on
    def evaluate_nodes(self, is_setup=False):
        for row in self.board.get_nodes():
            row_evaluations = []
            for node in row:
                # useless if someone has already built there 
                if node.get_building() and (node not in self.settlements or node not in self.cities):
                    row_evaluations.append(-2)
                    continue 
                else:
                    # almost useless if someone has built next to there
                    settlements_next_door = [n for n in node.get_connections() if n.get_building() and (n not in self.settlements or n not in self.cities)]
                    if settlements_next_door:
                        row_evaluations.append(-1)
                        continue
                    else:
                        value_sum = 0
                        resource_multiplier = 1
                        opposition_score = 0
                        for tile in node.get_adjacentTiles():
                            # adds the number of dice configurations 
                            # that can make the number to the value_sum
                            number += tile.get_number()
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
                            if self.resource_tiles[resource] == 0:
                                multiplier *= 2

                            resource_multiplier += multiplier

                            if tile.get_robber() and not self.player.has_knight():
                                resource_multiplier = resource_multiplier * 0.5
                        for neighbor in node.get_connections():
                            # checks if there are any opposing player roads going to this node
                            if (self.board.get_edge(neighbor, node).get_road() != None or 
                            self.board.get_edge(neighbor, node).get_road() != self.player):
                                opposition_score += 2
                            for n in neighbor.get_connections():
                                # checks if any of the nodes two roads away have an opposing settlement or city
                                if n != node and (n.get_building() != None or n.get_building() != self.player):
                                    opposition_score += 2
                                # checks if there are any opposing player roads going into nodes one road away from this node
                                if (self.board.get_edge(neighbor, n).get_road() != None or
                                self.board.get_edge(neighbor, n).get_road() != self.player):
                                    opposition_score += 2
                                
                        evaluation = value_sum / opposition_score * resource_multiplier
                        row_evaluations.append(evaluation)
            self.node_evaluations.append(row_evaluations)

    def evaluate_edges(self):
        pass
                    


    # finds the nodes with the highest evaluation and builds there
    def opening_move(self):
        for i in range(2):
            self.evaluate_nodes(True)
            best_move = [0,0,0]
            for row in range(len(self.board.get_nodes())):
                for node in range(len(row)):
                    if self.node_evaluations[row][node] > best_move[2]:
                        best_move[0] = row
                        best_move[1] = node
                        best_move[2] = self.node_evaluations[row][node]
            # build a settlement on the best node
        
                

    def play_dev_card(self):
        pass

    def build_road(self):
        pass

    def build_settlement(self, node):
        tiles = node.get_adjacentTiles()
        for tile in tiles:
            if tile.get_resource():
                if tile.get_number() < 4 or tile.get_number() > 10:
                    self.resource_tiles[tile.get_resource()] += 0.5
                elif tile.get_number() == 8 or tile.get_number() == 6:
                    self.resource_tiles[tile.get_resource()] += 1.5
                else:
                    self.resource_tiles[tile.get_resource()] += 1
            self.tile.get_resource()
            if tile.get_robber and self.player.has_knight():
                self.player.next_move()
            

    def buy_dev_card(self):
        pass

    