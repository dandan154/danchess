import logging


class Board:
    def __init__(self):
        self._board_size = 8
        self._cur_player_is_white = True
        self._taken_pieces = []
        self._board = None

        self._initialize_board()

    def _initialize_board(self):
        # Fill board with Squares
        self._board = [[Square((x, y)) for y in range(self._board_size)] for x in range(self._board_size)]

        # 2nd Rank should be white pawns, 7th Rank should be black pawns
        for x in range(self._board_size):
            self._board[1][x] = Pawn((x, 1), True)
            self._board[6][x] = Pawn((x, 6), False)

        # Corners should be Rooks
        self._board[0][0] = Rook((0, 0), True)
        self._board[0][7] = Rook((7, 0), True)

        self._board[7][0] = Rook((0, 7), False)
        self._board[7][7] = Rook((7, 7), False)

        # Squares adjacent to Rooks should be Knights
        self._board[0][1] = Knight((1, 0), True)
        self._board[0][6] = Knight((6, 0), True)

        self._board[7][1] = Knight((1, 7), False)
        self._board[7][6] = Knight((6, 7), False)

        # Squares adjacent to Knights should be Bishops
        self._board[0][2] = Bishop((2, 0), True)
        self._board[0][5] = Bishop((5, 0), True)

        self._board[7][2] = Bishop((2, 7), False)
        self._board[7][5] = Bishop((5, 7), False)

        #Queens are on D file
        self._board[0][3] = Queen((3, 0), True)
        self._board[7][3] = Queen((3, 7), False)

        # Kings are on E file
        self._board[0][4] = King((4, 0), True)
        self._board[7][4] = King((4, 7), False)


    def get_square(self, square):
        return self._board[square[1]][square[0]]

    def set_square(self, square, piece):
        self._board[square[1]][square[0]] = piece

    def get_board_size(self):
        return self._board_size

    def get_taken_pieces(self):
        return self._taken_pieces

    def get_board(self):
        return self._board

    def change_player(self):
        self._cur_player_is_white = not self._cur_player_is_white

    def print_board(self):
        for x in range(self._board_size):
            row = []
            for y in range(self._board_size):
                row.append(str(self._board[x][y]))
            print(row)

    def check_if_selection_valid(self, piece_square):
        sq = self.get_square(piece_square)

        if not sq.is_piece():
            logging.info("Selected square {} doesn't contain a piece".format(piece_square))
            return False, "Selected square {} doesn't contain a piece".format(piece_square)

        if sq.is_white() is not self._cur_player_is_white:
            return False, "Selected {} on {} is not your piece!".format(sq.long_name(), piece_square)

        return True, ""

    def check_if_move_valid(self, piece_square, new_square):
        piece_sq = self.get_square(piece_square)

        is_valid, err_msg = piece_sq.is_valid_move(new_square, self)

        return is_valid, err_msg

    def move_piece(self, piece_square, new_square):
        piece_sq = self.get_square(piece_square)
        new_sq = self.get_square(new_square)

        piece_sq.move(new_square)

        # Record that piece has been taken.
        if new_sq.is_piece():
            self._taken_pieces.append(new_sq)

        self.set_square(new_square, piece_sq)
        self.set_square(piece_square, Square(piece_square))


class Square:
    def __init__(self, cur_square, **kwargs):
        super().__init__(**kwargs)
        self._cur_square = cur_square
        logging.info("Square initialised - coords: {}".format(cur_square))

    @staticmethod
    def is_piece():
        return False

    @staticmethod
    def char_rep():
        return '0'

    @staticmethod
    def long_name():
        return "Square"

    def get_cur_square(self):
        return self._cur_square

    def set_cur_square(self, cur_square):
        self._cur_square = cur_square

    def __str__(self):
        return self.char_rep()


class Piece(Square):

    def __init__(self, is_white, **kwargs):
        super().__init__(**kwargs)
        self._is_white = is_white

    @staticmethod
    def is_piece():
        return True

    def is_white(self):
        return self._is_white

    def is_valid_move(self, new_square, board):
        logging.warning("No move rules are defined for this - coords: {}".format(self._cur_square))
        return False, "No move rules are defined for this - coords: {}".format(self._cur_square)

    def __str__(self):
        if self._is_white:
            return self.char_rep() + "(W)"
        else:
            return self.char_rep() + "(B)"


class HasMovedMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._has_moved = False

    def get_has_moved(self):
        return self._has_moved

    def set_has_moved(self, has_moved):
        self._has_moved = has_moved


class Pawn(Piece, HasMovedMixin):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)

        logging.info("Pawn initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'P'

    @staticmethod
    def long_name():
        return "Pawn"

    def is_valid_move(self, new_square, board):
        logging.info("Checking validity of Pawn move from {} to {}".format(self._cur_square, new_square))
        x_diff = self._cur_square[0] - new_square[0]
        y_diff = self._cur_square[1] - new_square[1]

        # White and Black pawns move in opposite directions
        if self._is_white:
            y_diff = -y_diff

        # Pawns cannot move backwards and Pawns must move.
        if y_diff < 1:
            return False, "Pawns must at least 1 square forward."

        # Pawns cannot move more that 1 square (or 2 square on first move)
        if y_diff > 2 or y_diff > 1 and self.get_has_moved():
            return False, "Pawns cannot move forward more that 1 square (or 2 square on first move)"

        # Pawns cannot move more than 1 square on x-axis (and only occurs during capture)
        if abs(x_diff) > 1:
            return False, "Pawns cannot move more than 1 square on x-axis (only during captures)"

        # Check if move is an attack
        if x_diff == 0:
            # move is not a capture, check if squares between cur square and square to move to are empty
            if self._is_white:
                for y in range(self._cur_square[1] + 1, new_square[1] + 1):
                    square_to_check = board.get_square((new_square[0], y))
                    if square_to_check.is_piece():
                        return False, "Pawn is blocked by {} on {}".format(
                            square_to_check.long_name(),
                            (new_square[0], y)
                        )

            else:
                for y in range(new_square[1], self._cur_square[1]):
                    square_to_check = board.get_square((new_square[0], y))
                    if square_to_check.is_piece():
                        return False, "Pawn is blocked by {} on {}".format(
                            square_to_check.long_name(),
                            (new_square[0], y)
                        )

            # DOES THIS MOVE RESULT IN A CHECK? - FUTURE FUNCTIONALITY

            return True, ""

        else:
            # Pawns capture 1 square diagonally.
            if y_diff != 1:
                return False, "Pawns only capture 1 square diagonally."

            square_to_check = board.get_square(new_square)
            if not square_to_check.is_piece():
                return False, "Cannot move diagonally unless it's a capture."

            # Cannot capture own piece
            if square_to_check.is_white() == self._is_white:
                return False, "Cannot capture own piece!"

            return True, ""

    def move(self, new_square):
        logging.info("Updating Pawn variables after move")
        self._cur_square = new_square
        if not self.get_has_moved():
            self.set_has_moved(True)


class Rook(Piece, HasMovedMixin):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)

        logging.info("Rook initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'R'

    @staticmethod
    def long_name():
        return "Rook"

    def is_valid_move(self, new_square, board):
        logging.info("Checking validity of Rook move from {} to {}".format(self._cur_square, new_square))
        x_diff = self._cur_square[0] - new_square[0]
        y_diff = self._cur_square[1] - new_square[1]

        # Rooks can only move along one axis at a time.
        if abs(x_diff) > 0 and abs(y_diff) > 0:
            return False, "Rooks can only move along one axis at a time."

        # Rook must move
        if x_diff == 0 and y_diff == 0:
            return False, "Piece cannot remain in same square!"

        loop_inc = -1
        if x_diff < 0 or y_diff < 0:
            loop_inc = 1

        # Check for pieces between cur square and new square.
        if abs(y_diff) > 0:
            # Check all squares leading up to landing square for pieces.
            for y in range(self._cur_square[1] + loop_inc, new_square[1], loop_inc):
                tmp_coord = (self._cur_square[0], y)
                print("checking square", tmp_coord)
                logging.debug("Checking square {}".format(tmp_coord))
                square_to_check = board.get_square(tmp_coord)
                if square_to_check.is_piece():
                    return False, "Rook is blocked by {} on {}".format(square_to_check.long_name(), tmp_coord)
        else:
            # Check all squares leading up to landing square for pieces.
            for x in range(self._cur_square[0] + loop_inc, new_square[0], loop_inc):
                tmp_coord = (x, self._cur_square[1])
                logging.debug("Checking square {}".format(tmp_coord))
                square_to_check = board.get_square(tmp_coord)
                if square_to_check.is_piece():
                    return False, "Rook is blocked by {} on {}".format(square_to_check.long_name(), tmp_coord)

        landing_square = board.get_square(new_square)

        # Can't capture own piece.
        if landing_square.is_piece() and landing_square.is_white() == self.is_white():
            return False, "The {} on {} belongs to you!".format(landing_square.long_name(), new_square)

        return True, ""

    def move(self, new_square):
        logging.info("Updating Rook variables after move")
        self._cur_square = new_square
        if not self.get_has_moved():
            self.set_has_moved(True)


class Bishop(Piece):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)
        logging.info("Bishop initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'B'

    @staticmethod
    def long_name():
        return "Bishop"


class Knight(Piece):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)
        logging.info("Knight initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'N'

    @staticmethod
    def long_name():
        return "Knight"


class Queen(Piece):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)
        logging.info("Queen initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'Q'

    @staticmethod
    def long_name():
        return "Queen"


class King(Piece):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)
        logging.info("King initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'K'

    @staticmethod
    def long_name():
        return "King"



