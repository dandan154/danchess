import logging
import pprint

class Board:
    def __init__(self):
        self._board_size = 8
        self._cur_player_is_white = True
        self._taken_pieces = []
        self.initialize_board()

    def initialize_board(self):
        # Fill board with Squares
        self._board = [[Square((x, y)) for x in range(self._board_size)] for y in range(self._board_size)]

        # 2nd Rank should be white pawns, 7th Rank should be black pawns
        for x in range(self._board_size):
            self._board[1][x] = Pawn((x, 1), True)
            self._board[6][x] = Pawn((x, 6), False)

        # Corners should be Rooks
        self._board[0][0] = Rook((0, 0), True)
        self._board[0][7] = Rook((0, 7), True)

        self._board[7][0] = Rook((0, 0), False)
        self._board[7][7] = Rook((7, 7), False)

    def get_square(self, square):
        return self._board[square[1]][square[0]]

    def set_square(self, square, piece):
        self._board[square[1]][square[0]] = piece

    def pprint_board(self):
        board_char = [[self._board[x][y].char_rep() for y in range(self._board_size)] for x in range(self._board_size)]
        pprint.pprint(board_char)

    def check_if_selection_valid(self, piece_square):
        sq = self.get_square(piece_square)

        if not sq.is_piece():
            logging.info("Selected square {} doesn't contain a piece".format(piece_square))
            return False, "Selected square {} doesn't contain a piece".format(piece_square)

        if sq.is_white() != self._cur_player_is_white:
            return False, "Selected {} on {} is not your piece!".format(sq.long_name(), piece_square)

    def move_piece(self, piece_square, new_square):
        piece_sq = self.get_square(piece_square)
        new_sq = self.get_square(new_square)

        is_valid, err_msg = piece_sq.is_valid_move(new_square, self._board)

        if not is_valid:
            piece_sq.move(new_square)

            # Record that piece has been taken.
            if new_sq.is_piece():
                self._taken_pieces.append(new_sq)

            self.set_square(new_square, piece_sq)
            self.set_square(piece_square, Square(piece_square))


        else:
            return False, err_msg



class Square:
    def __init__(self, cur_square):
        self.cur_square = cur_square
        logging.info("Square initialised - coords: {}".format(cur_square))

    @staticmethod
    def is_piece():
        return False

    @staticmethod
    def char_rep():
        return '0'

    @staticmethod
    def long_name():
        return "Empty Square"

    def is_valid_move(self, new_square, board):
        logging.warning("No move rules are defined for this - coords: {}".format(self.cur_square))
        return False


class Pawn(Square):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square)
        self.is_white = is_white
        self.has_moved = False

        logging.info("Pawn initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def is_piece():
        return True

    @staticmethod
    def char_rep():
        return 'P'

    @staticmethod
    def long_name():
        return "Pawn"

    def is_white(self):
        return self.is_white

    def is_valid_move(self, new_square, board):
        logging.info("Checking validity of Pawn move from {} to {}".format(self.cur_square, new_square))
        x_diff = self.cur_square[0] - new_square[0]
        y_diff = self.cur_square[1] - new_square[1]

        # White and Black pawns move in opposite directions
        if self.is_white:
            y_diff = -y_diff

        # Pawns cannot move backwards and Pawns must move.
        if y_diff < 1:
            return False

        # Pawns cannot move more that 1 square (or 2 square on first move)
        if y_diff > 2 or y_diff > 1 and self.has_moved:
            return False, "Pawns cannot move forward more that 1 square (or 2 square on first move)"

        # Pawns cannot move more than 1 square on x-axis (and only occurs during capture)
        if abs(x_diff) > 1:
            return False

        # Check if move is an attack
        if x_diff == 0:
            # move is not a capture, check if squares between cur square and square to move to are empty
            if self.is_white:
                for y in range(self.cur_square[1]+1, new_square[1]+1):
                    square_to_check = board.get_square((new_square[0], y))
                    if square_to_check.is_piece():
                        return False, "Pawn is blocked by {} on {}".format(square_to_check.long_name(), (new_square[0], y))

            else:
                for y in range(new_square[1], self.cur_square[1]):
                    square_to_check = board.get_square((new_square[0], y))
                    if square_to_check.is_piece():
                        return False, "Pawn is blocked by {} on {}".format(square_to_check.long_name(), (new_square[0], y))

            # DOES THIS MOVE RESULT IN A CHECK? - FUTURE FUNCTIONALITY

            return True

        else:
            # Pawns capture 1 square diagonally.
            if y_diff != 1:
                return False, "Pawns only capture 1 square diagonally."

            square_to_check = board.get_square(new_square)
            if not square_to_check.is_piece():
                return False, "Cannot move diagonally unless it's a capture."

            # Cannot capture own piece
            if square_to_check.is_white == self.is_white:
                return False, "Cannot capture own piece!"

            return True

    def move(self, new_square):
        logging.info("Updating Pawn variables after move")
        self.cur_square = new_square
        if not self.has_moved:
            self.has_moved = True


class Rook(Square):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square)
        self.is_white = is_white
        self.has_moved = False
        logging.info("Rook initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def is_piece():
        return True

    @staticmethod
    def char_rep():
        return 'R'

    @staticmethod
    def long_name():
        return "Rook"

    def is_white(self):
        return self.is_white


    def is_valid_move(self, new_square, board):
        logging.info("Checking validity of Rook move from {} to {}".format(self.cur_square, new_square))
        x_diff = self.cur_square[0] - new_square[0]
        y_diff = self.cur_square[1] - new_square[1]

        # Rooks can only move along one axis at a time.
        if abs(x_diff) > 0 and abs(y_diff) > 0:
            return False, "Rooks can only move along one axis at a time."

        # Rook must move
        if x_diff == 0 and y_diff == 0:
            return False, "Piece cannot remain in same square!"

        loop_incr = 1
        if x_diff < 0 or y_diff < 0:
            loop_incr = -1

        # Check for pieces between cur square and new square.
        if abs(y_diff) > 0:
            # Check all squares leading up to landing square for pieces.
            for y in range(self.cur_square[1] + loop_incr, new_square[1], loop_incr):
                tmp_coord = (self.cur_square[0], y)
                logging.debug("Checking square {}".format(tmp_coord))
                square_to_check = board.get_square(tmp_coord)
                if square_to_check.is_piece():
                    return False, "Rook is blocked by {} on {}".format(square_to_check.long_name(), tmp_coord)
        else:
            # Check all squares leading up to landing square for pieces.
            for x in range(self.cur_square[0]+loop_incr, new_square[0], loop_incr):
                tmp_coord = (x, self.cur_square[1])
                logging.debug("Checking square {}".format(tmp_coord))
                square_to_check = board.get_square(tmp_coord)
                if square_to_check.is_piece():
                    return False, "Rook is blocked by {} on {}".format(square_to_check.long_name(), tmp_coord)

        landing_square = board.get_square(new_square)

        # Can't capture own piece.
        if landing_square.is_piece() and landing_square.is_white:
            return False, "The {} on {} belongs to you!".format(landing_square.long_name(), new_square)

        return True

    def move(self, new_square):
        logging.info("Updating Rook variables after move")
        self.cur_square = new_square
        if not self.has_moved:
            self.has_moved = True
