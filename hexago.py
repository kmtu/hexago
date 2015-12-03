import os
import re


class Board():
    def __init__(self, size):
        self.table = [[0 for i in range(size[1])] for i in range(size[0])]

    def draw(self):
        for row in self.table:
            print(row)

    def put(self, player, position):
        self.table[position[0]][position[1]] = player


class Game():
    def __init__(self, size):
        self.board = Board(size)
        self.gameover = False
        self.winner = None
        self.current_player = 2

    def run(self):
        while not self.gameover:
            # swap the player 1 -> 2, 2 -> 1
            self.current_player += 1
            if self.current_player > 2:
                self.current_player = 1

            # clear the screen
            # http://stackoverflow.com/questions/2084508/clear-terminal-in-python
            os.system('cls' if os.name == 'nt' else 'clear')

            # draw the board
            print('dlrow olleH')
            self.board.draw()

            # ask for move
            print("\nPlayer {}'s turn".format(self.current_player))
            valid_input = False
            while not valid_input:
                line = input("Please input two numbers (row column): ")

                # http://stackoverflow.com/questions/4998629/python-split-string-with-multiple-delimiters
                pos = re.split(' |,', line)

                # remove empty strings in the list and take only the first two
                # and make them become integers
                try:
                    pos = [int(p) for p in pos if p is not ''][:2]
                except ValueError:
                    valid_input = False
                else:
                    valid_input = True

            self.board.put(self.current_player, pos)

        print("The winner is: Player {}".format(self.winner))


def main():
    size = (15, 19)
    game = Game(size)
    game.run()

if __name__ == '__main__':
    main()
