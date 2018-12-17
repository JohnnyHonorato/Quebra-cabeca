################################################################################
#
# Este é o exercício da 1a avaliação da disciplina de IA.
#
# O código traz um esqueleto para a implementação da busca A* para
# resolver o problema do quebra-cabeça de 8 números.
#
# O Objetivo do exercício é implementar o que falta da busca no código abaixo.
# Os métodos que precisam ser implementados estão com a marcação "TODO" seguida
# de uma descrição do que precisa ser feito.
#
# Leia atentamente todo os comentários no código.
#
# Se o programa estiver executando corretamente, ele deve exibir todas as
# configurações do tabuleiro do quebra cabeça dos 8 números para sair do estado
# final até chegar ao objetivo.
#
################################################################################

import random

class Board(object):

    def __init__(self, tiles):
        self.goal = [1,2,3,4,5,6,7,8,"x"]
        self.tiles = tiles

    def is_goal(self):
        return self.tiles == self.goal
        pass

    def heuristic(self):
        cont = 0;
        num = 0;
        while(cont < 9):
            if self.tiles[cont] != self.goal[cont]:
                num += 1
            cont += 1
        return num
        pass

    def acha_X(self):
        cont = 0
        while(cont < 9):
            if self.tiles[cont] == 'x':
                return cont
            cont += 1
        return None

    def get_neighbors(self):
        neighbors = []
        aff = self.acha_X()

        if(aff == 0 or aff == 1 or aff == 3 or aff == 4 or aff == 6 or aff == 7):
            new_board = self.tiles.copy()
            new_board[aff] = new_board[aff+1] 
            new_board[aff+1] = 'x'
            neighbors.append(Board(new_board))
        if(aff == 0 or aff == 1 or aff == 2 or aff == 3 or aff == 4 or aff == 5):
            new_board = self.tiles.copy()
            new_board[aff] = new_board[aff+3] 
            new_board[aff+3] = 'x'
            neighbors.append(Board(new_board))
        if(aff == 1 or aff == 2 or aff == 4 or aff == 5 or aff == 7 or aff == 8):
            new_board = self.tiles.copy()
            new_board[aff] = new_board[aff-1] 
            new_board[aff-1] = 'x'
            neighbors.append(Board(new_board))
        if(aff == 3 or aff == 4 or aff == 5 or aff == 6 or aff == 7 or aff == 8):
            new_board = self.tiles.copy()
            new_board[aff] = new_board[aff-3] 
            new_board[aff-3] = 'x'
            neighbors.append(Board(new_board))
            
        return neighbors
             
    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(tuple(self.tiles))

    def __str__(self):
        return str(self.tiles)

    def __repr__(self):
        return str(self.tiles)

    def print_board(self):
        print(self.tiles[:3])
        print(self.tiles[3:6])
        print(self.tiles[6:])


class Node(object):

    def __init__(self, state, cost):
        self.state = state
        self.cost = cost
        self.parent = None

    def __str__(self):
        return str(self.state.tiles) + " - " + str(self.cost)

    def __repr__(self):
        return str(self.state.tiles) + " - " + str(self.cost)


class AStar(object):

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.frontier = [Node(self.initial_state, 0 + self.initial_state.heuristic())]
        self.explored = set()
        self.current_node = None

    def choose_from_frontier(self):
        menor = self.frontier[0]
        for no in self.frontier:
            if no.cost < menor.cost:
                menor = no
        self.frontier.remove(menor)
        return menor

    def update_frontier(self):
        vizinho = self.current_node.state.get_neighbors()
        for oxi in vizinho:
            no = Node(oxi, oxi.heuristic())
            if not(self.is_neighbor_in_frontier(no.state)):
                if not(no.state in self.explored):
                    no.parent = self.current_node
                    self.frontier.append(no)

    def is_neighbor_in_frontier(self, neighbor):
        for node in self.frontier:
            if node.state == neighbor:
                return True
        
        return False

    def get_path(self, node):
        lista = [node.state]
        for i in self.initial_state.tiles:
            lista.append(node.parent.state)
            node = node.parent

        return lista

    def search(self):
        while True:
            if len(self.frontier) == 0:
                return False

            self.current_node = self.choose_from_frontier()

            self.explored.add(self.current_node.state)

            if self.current_node.state.is_goal():
                return self.current_node

            self.update_frontier()
            

if __name__ == "__main__":
    tiles = [3, 2, 8, 1, 5, 4, 7, 6, "x"]
    initial_state = Board(tiles)

    astar = AStar(initial_state)
    final_node = astar.search()
    path = astar.get_path(final_node).__reversed__()
    
    for state in path:
        state.print_board()
        print("---")
