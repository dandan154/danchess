import logging
import pprint

BOARD_SIZE = 8


class Board:
    def __init__(self):
        # Fill board with Squares
        self.board = [[Square((x, y)) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

        print("starting pawns")
        # 2nd Rank should be white pawns, 7th Rank should be black pawns
        for x in range(BOARD_SIZE):
            self.board[1][x] = Pawn((x,1), True)
            self.board[6][x] = Pawn((x,6), False)

    def get_square(self, square):
        return self.board[square[1]][square[0]]

    def pprint_board(self):
        board_char = [[self.board[x][y].char_rep() for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
        pprint.pprint(board_char)


class Square:
    def __init__(self, cur_square):
        self.cur_square = cur_square
        print(cur_square)

    @staticmethod
    def is_piece():
        return False

    @staticmethod
    def char_rep():
        return '0'


class Pawn(Square):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square)
        self.is_white = is_white
        self.has_moved = False

    @staticmethod
    def is_piece():
        return True

    @staticmethod
    def char_rep():
        return 'P'

    def is_valid_move(self, new_square, board):
        x_diff = self.cur_square[0] - new_square[0]
        y_diff = self.cur_square[1] - new_square[1]

        # White and Black pawns move in opposite directions
        if self.is_white:
            y_diff = -y_diff

        # Pawns cannot move backwards.
        if y_diff < 1:
            return False

        # Pawns cannot move more that 1 square (or 2 square on first move)
        if y_diff > 2 or y_diff > 1 and self.has_moved:
            return False

        # Pawns cannot move more than 1 square on x-axis (and only occurs during capture)
        if abs(x_diff) > 1:
            return False

        # Check if move is an attack
        if x_diff == 0:
            # move is not a capture, check if squares between cur square and square to move to are empty
            if self.is_white:
                for y in range(self.cur_square[1]+1, new_square[1]+1):
                    square = board.get_square((new_square[0], y))
                    print(square.char_rep(), square.cur_square, square.is_piece())
                    if square.is_piece():
                        return False

            else:
                for y in range(new_square[1], self.cur_square[1]):
                    square = board.get_square((new_square[0], y))
                    print(square.char_rep(), square.cur_square)
                    if square.is_piece():
                        return False


        else:
            # Pawns capture 1 square diagonally.
            if y_diff != 1:
                return False


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',
                        level=logging.ERROR)

    board = Board()
    board.pprint_board()
    pawn = board.get_square((2, 1))
    print(pawn.is_valid_move((2, 3), board))

    black_pawn = board.get_square((2, 6))
    print(black_pawn.is_valid_move((2, 4), board))


