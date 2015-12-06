import os
import re
import sys
from enum import Enum
import string
import itertools


class Error(Exception):
    pass


class IllegalMoveError(Error):
    pass


class Move():
    class Type(Enum):
        place = 'place'
        shift = 'shift'

    def __init__(self, type, player):
        if type not in Move.Type:
            raise Error("Wrong move type: {}".format(type))
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

    def __init__(self, player, direction, side, line, displace):
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
    empty_symbol = ' '
    coord_alphabet = (list(string.ascii_uppercase) +
                      [''.join(c) for c in itertools.product(
                       string.ascii_uppercase, repeat=2)] +
                      [''.join(c) for c in itertools.product(
                       string.ascii_uppercase, repeat=3)])

    def __init__(self, size):
        self.table = [[Board.empty_symbol for i in range(size[1])]
                      for i in range(size[0])]

    def draw(self):
        offset = 3
        for i, row in enumerate(self.table):
            if i == 0:
                # column line coordinates
                print(' ' * (offset * 2 + 3) + ' '.join(
                    ['{:^3}'.format(j) for j in
                        Board.coord_alphabet[:len(row)-1]]))

                # column piece coordinates
                print(' ' * (offset * 2 + 1) + '│'.join(
                    ['{:^3d}'.format(j) for j in range(len(row))]))

                # top line for the first row
                print(' ' * offset * 2 +
                      '┌' + '───┬' * (len(row) - 1) + '───┐')

            # print the pieces
            print(' ' * offset + '{:^3d}'.format(i) +
                  '│ ' + ' │ '.join(row) + ' │')

            if i == len(self.table) - 1:
                # bottom line for the last row
                print(' ' * offset * 2 +
                      '└' + '───┴' * (len(row) - 1) + '───┘')
            else:
                # bottom line for the middle rows
                print('{:^3}'.format(Board.coord_alphabet[i]) + '───' +
                      '├' + '───┼' * (len(row) - 1) + '───┤')

    def move(self, move):
        if move.type is Move.Type.place:
            self.verify_place(move)
            self.place(move)
        elif move.type is Move.Type.shift:
            self.verify_shift(move)
            self.shift(move)

    def on_board(self, position):
        if (any(p < 0 for p in position) or
                position[0] >= len(self.table) or
                position[1] >= len(self.table[0])):
            return False
        return True

    def verify_place(self, move):
        for pos in move.position:
            if not self.on_board(pos):
                raise IllegalMoveError("Place out of board: ", pos)
            if self.table[pos[0]][pos[1]] != Board.empty_symbol:
                raise IllegalMoveError("Place has been occupied: ", pos)

    def place(self, move):
        for pos in move.position:
            self.table[pos[0]][pos[1]] = move.player.symbol

    def shift(self, move):
        # TODO
        # player = move.player
        # direction = move.direction
        # line = move.line
        # side = move.side
        # displace = move.displace
        raise Error("Shift has not been implemented, yet")

    def verify_shift(self, move):
        pass


class Game():
    def __init__(self, size):
        self.board = Board(size)
        self.gameover = False
        self.players = [Player('One', '@'), Player('Two', 'O')]
        self.current_player_id = 0

    def clear_screen(self):
        # clear the screen
        # http://stackoverflow.com/questions/2084508/clear-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_interface(self):
        current_player = self.players[self.current_player_id]
        self.clear_screen()
        print('dlrow olleH\n')
        self.board.draw()
        # ask for move
        print("\nPlayer {}'s turn (symbol {})".format(
            current_player.name, current_player.symbol))

    def run(self):
        while not self.gameover:
            current_player = self.players[self.current_player_id]
            self.draw_interface()

            while True:
                try:
                    line = input("Please input your move: ")
                except EOFError:
                    continue

                # check for special commands
                if re.fullmatch('quit', line):
                    sys.exit()
                elif re.fullmatch('c(lear)?', line):
                    self.draw_interface()

                # initialize move
                move = None

                # replace all commas with spaces
                line = re.sub(',', ' ', line)

                # check if input is a list of numbers
                match = re.fullmatch(
                        '^\s*([0-9]+|([0-9]+\s+)+([0-9]+)?)\s*', line)
                if match:
                    position = [int(p) for p in line.split()]
                    num_pos = len(position)
                    if num_pos == 4:
                        position = [(position[i], position[i+1])
                                    for i in range(0, num_pos, 2)]
                        move = Place(current_player, position)

                # check if input is a Shift
                # [direction][side][line]\s*[displace]
                match = re.fullmatch(
                        '^\s*([\^v<>])([+-])([A-Z]+)\s*([+-]?[1-9][0-9]*)',
                        line)
                if match:
                    move = Shift(current_player, *match.groups())

                if move is not None:
                    try:
                        self.board.move(move)
                    except Error as e:
                        print(*e.args)
                        continue
                    else:
                        break

            # change to next player
            self.current_player_id += 1
            if self.current_player_id >= len(self.players):
                self.current_player_id = 0

        print("The winner is ...")


def main():
    size = (11, 11)
    game = Game(size)
    game.run()

if __name__ == '__main__':
    main()
