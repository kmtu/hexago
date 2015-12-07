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

    def __init__(self, table):
        self.table = table
        self.size = (len(self.table), len(self.table[0]))

    @classmethod
    def empty(cls, size):
        table = [[Board.empty_symbol for i in range(size[1])]
                 for i in range(size[0])]
        return cls(table)

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

    def do(self, move):
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
        if len(move.position) != len(set(move.position)):
            raise IllegalMoveError(
                    "Placing two pieces at the same spot is not allowed")

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

    def has_n_in_row(self, n, player):
        for line_dir in Pattern.LineDirection:
            if len(self.scan(Pattern.n_in_row(n, line_dir), player)) > 0:
                return True
        return False

    def scan(self, pattern, player):
        """Scan if pattern exists within board with player as owner
        """
        # TODO
        match = []
        if all([b >= p for b in self.size for p in pattern.size]):
            for r in range(self.size[0] - pattern.size[0] + 1):
                for c in range(self.size[1] - pattern.size[1] + 1):
                    if self.sub_board((r, c), pattern.size).match(
                            pattern, player):
                        match.append((r, c))
        return match

    def sub_board(self, position, size):
        """Create sub board at position with size
        """
        table = [self.table[r+position[0]][position[1]:position[1]+size[1]]
                 for r in range(size[0])]
        return Board(table)

    def match(self, pattern, player):
        """Test if board and pattern match exactly
        """
        if self.size != pattern.size:
            return False
        else:
            for r in range(self.size[0]):
                for c in range(self.size[1]):
                    if pattern.table[r][c] is Pattern.Symbol.any:
                        continue
                    else:
                        if (pattern.table[r][c] is Pattern.Symbol.empty and
                                self.table[r][c] != Board.empty_symbol):
                            return False
                        elif (pattern.table[r][c] is Pattern.Symbol.own and
                                self.table[r][c] != player.symbol):
                            return False
                        elif (pattern.table[r][c] is Pattern.Symbol.others and
                                (self.table[r][c] == Board.empty_symbol or
                                 self.table[r][c] == player.symbol)):
                            return False

            return True


class Pattern():
    class Symbol(Enum):
        any = '*'
        empty = '_'
        own = 0
        others = '@'

    class LineDirection(Enum):
        horizontal = '-'
        vertical = '|'
        slash = '/'
        backslash = '\\'

    def __init__(self, table):
        self.table = table
        self.size = (len(self.table), len(self.table[0]))

    @classmethod
    def n_in_row(cls, n, line_dir):
        if line_dir is cls.LineDirection.horizontal:
            pattern = [[cls.Symbol.own for i in range(n)]]
        elif line_dir is cls.LineDirection.vertical:
            pattern = [[cls.Symbol.own] for i in range(n)]
        elif line_dir is cls.LineDirection.slash:
            pattern = [[cls.Symbol.any for i in range(n)]
                       for i in range(n)]
            for i in range(n):
                pattern[i][n-i-1] = cls.Symbol.own
        elif line_dir is cls.LineDirection.backslash:
            pattern = [[cls.Symbol.any for i in range(n)]
                       for i in range(n)]
            for i in range(n):
                pattern[i][i] = cls.Symbol.own

        return cls(pattern)


class Game():
    def __init__(self, size):
        self.board = Board.empty(size)
        self.players = [Player('One', '@'), Player('Two', 'O')]
        self.current_player_id = 0
        self.gameover = False
        self.winner = []

    def reset(self):
        self.board = Board.empty(self.board.size)
        self.players = [Player('One', '@'), Player('Two', 'O')]
        self.current_player_id = 0
        self.gameover = False
        self.winner = []

    def clear_screen(self):
        # clear the screen
        # http://stackoverflow.com/questions/2084508/clear-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_interface(self):
        current_player = self.players[self.current_player_id]
        self.clear_screen()
        print('dlrow olleH\n')
        self.board.draw()
        if self.gameover:
            print("\nThe winner is ... {}!".format(
                ' and '.join([w.name for w in self.winner])))
        else:
            # ask for move
            print("\nPlayer {}'s turn (symbol {})".format(
                current_player.name, current_player.symbol))

    def run(self):
        # main game loop
        while True:
            # check if game is over
            for p in self.players:
                if self.board.has_n_in_row(6, p):
                    self.winner.append(p)
            if len(self.winner) > 0:
                self.gameover = True

            current_player = self.players[self.current_player_id]
            self.draw_interface()

            # input processing
            if self.gameover:
                while True:
                    try:
                        line = input("Play again? ")
                    except EOFError:
                        continue

                    # check for commands
                    if re.fullmatch('n(o)?', line):
                        sys.exit()
                    elif re.fullmatch('y(es)?', line):
                        self.reset()

            else:
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
                    dirs = ''.join(d.value for d in Shift.Direction)
                    sides = ''.join(s.value for s in Shift.Side)
                    match = re.fullmatch(
                            '^\s*([\\{}])([{}])([a-zA-Z]+)\s*'
                            '([+-]?[1-9][0-9]*)'.format(dirs, sides),
                            line)
                    if match:
                        move = Shift(current_player, *match.groups())

                    if move is not None:
                        try:
                            self.board.do(move)
                        except Error as e:
                            print(*e.args)
                            continue
                        else:
                            break

                # change to next player
                self.current_player_id += 1
                if self.current_player_id >= len(self.players):
                    self.current_player_id = 0


def main():
    size = (11, 11)
    game = Game(size)
    game.run()

if __name__ == '__main__':
    main()
