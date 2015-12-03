class Board():
    def __init__(self, size):
        self.data = [[0 for i in range(size[1])] for i in range(size[0])]

    def draw(self):
        print(self.data)

    def put(player, position):
        pass


class Game():
    def __init__(self, size):
        self.board = Board(size)

    def run(self):
        print('dlrow olleH')
        self.board.draw()


def main():
    size = (15, 19)
    game = Game(size)
    game.run()

if __name__ == '__main__':
    main()
