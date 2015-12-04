import os
import re
import sys
from enum import Enum

class Move():
    class Type(Enum):
        place = 'place'
        shift = 'shift'

    def __init__(self, type, player):
        self.type = type
        self.player = player


class Place(Move):
    def __init__(self, player, position):
        super().__init__(Move.Type.place, player)
        self.position = position


class Shift(Move):
    class Direction(Enum):
        up = '^'
        down = 'v'
        left = '<'
        right = '>'

    class Side(Enum):
        positive = '+'
        negative = '-'

    def __init__(self, player, direction, line, side, displace):
        super().__init__(Move.Type.shift, player)
        self.direction = direction
        self.line = line
        self.side = side
        self.displace = displace


class Player():
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class Board():
    def __init__(self, size):
        self.size = size
        self.table = [[' ' for i in range(size[1])] for i in range(size[0])]

    def draw(self):
        for i, row in enumerate(self.table):
            if i == 0:
                print(*(['┌'] + ['───┬' for i in self.table[0][:-1]] + ['───┐']), sep='')
            print('│ ' + ' │ '.join(row) + ' │')
            if i == len(self.table) - 1:
                print(*(['└'] + ['───┴' for i in self.table[0][:-1]] + ['───┘']), sep='')
            else:
                print('├─' + '─┼─'.join(['─' for j in row]) + '─┤')


    def move(self, move):
        player = move.player
        if move.type is Move.Type.place:
            self.place(move)
        elif move.type is Move.Type.shift:
            self.shift(move)

    def place(self, move):
        player = move.player
        pos = move.position
        self.table[pos[0]][pos[1]] = player.symbol

    def shift(self, move):
        player = move.player
        direction = move.direction
        line = move.line
        side = move.side
        displace = move.displace


class Game():
    def __init__(self, size):
        self.board = Board(size)
        self.gameover = False
        self.players = [Player('One', '@'), Player('Two', 'O')]
        self.current_player_id = 0

    def run(self):
        while not self.gameover:
            current_player = self.players[self.current_player_id]
            # clear the screen
            # http://stackoverflow.com/questions/2084508/clear-terminal-in-python
            os.system('cls' if os.name == 'nt' else 'clear')

            # draw the board
            print('dlrow olleH\n')
            self.board.draw()

            # ask for move
            print("\nPlayer {}'s turn (symbol {})".format(
                current_player.name, current_player.symbol))
            valid_input = False
            while not valid_input:
                line = input("Please input two numbers (row column): ")

                # http://stackoverflow.com/questions/4998629/python-split-string-with-multiple-delimiters
                pos = re.split(' |,', line)

                try:
                    # remove empty strings in the list, take only the first two
                    # and make them become integers
                    pos = [int(p) for p in pos if p is not ''][:2]
                except ValueError:
                    if pos[0] == 'q':
                        sys.exit()
                    else:
                        print("Invalid input!")
                else:
                    if len(pos) == 2 and all(
                            p >= 0 and p < self.board.size[i]
                            for i, p in enumerate(pos)):
                        valid_input = True
                    else:
                        print("Invalid input!")

            self.board.move(Place(current_player, pos))

            # change to next player
            self.current_player_id += 1
            if self.current_player_id >= len(self.players):
                self.current_player_id = 0

        print("The winner is ...")


def main():
    size = (5, 5)
    game = Game(size)
    game.run()

if __name__ == '__main__':
    main()
