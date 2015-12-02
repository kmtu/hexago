class Board():
    def __init__(self, size):
        self.data = [[0 for i in range(size[0])] for i in range(size[1])]

    def draw(self):
        pass

    def put(player, position):
        pass


class Game():
    def __init__(self, size):
        self.board = Board(size)

    def run(self):
        pass


def main():
    size = (19, 19)
    game = Game(size)
    game.run()

if __name__ == '__main__':
    main()
