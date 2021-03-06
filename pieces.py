from copy import deepcopy
import logging


def is_landing_square_occupied(func):
    def wrapper(self, new_square, board, *args, **kwargs):
        val = func(self, new_square, board, *args, **kwargs)
        landing_square = board.get_square(new_square)
        # Can't capture own piece.
        if landing_square.is_piece() and landing_square.is_white() == self.is_white():
            val = False, "The {} on {} belongs to you!".format(landing_square.long_name(), new_square)
        return val
    return wrapper


class Board:

    def __init__(self):
        self._board_size = 8
        self._cur_player_is_white = True
        self._taken_pieces = []
        self._board = None

        self._white_king_coords = None
        self._black_king_coords = None

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

        # Queens are on D file
        self._board[0][3] = Queen((3, 0), True)
        self._board[7][3] = Queen((3, 7), False)

        # Kings are on E file
        self._white_king_coords = (4, 0)
        self._black_king_coords = (4, 7)

        self._board[self._white_king_coords[1]][self._white_king_coords[0]] = King(self._white_king_coords, True)
        self._board[self._black_king_coords[1]][self._black_king_coords[0]] = King(self._black_king_coords, False)

    def get_square(self, square):
        if square[0] > self._board_size-1 or square[0] < 0 or square[1] > self._board_size-1 or square[1] < 0:
            return None
        return self._board[square[1]][square[0]]

    def set_square(self, square, piece):
        self._board[square[1]][square[0]] = piece

    def get_board_size(self):
        return self._board_size

    def get_taken_pieces(self):
        return self._taken_pieces

    def get_board(self):
        return self._board

    def is_cur_player_white(self):
        return self._cur_player_is_white

    def change_player(self):
        self._cur_player_is_white = not self._cur_player_is_white
        return self._cur_player_is_white

    def get_cur_king_coords(self):
        if self._cur_player_is_white:
            return self._white_king_coords
        else:
            return self._black_king_coords

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

        if piece_square == new_square:
            return False, "Piece cannot remain in same square!"

        piece_sq = self.get_square(piece_square)

        # Check if move is valid
        is_valid, err_msg = piece_sq.is_valid_move(new_square, self)
        if not is_valid:
            return is_valid, err_msg

        # Check if current move would put current player into check
        tmp_board = deepcopy(self)
        tmp_board.move_piece(piece_square, new_square)
        is_check, err = tmp_board.is_cur_player_in_check()

        return not is_check, err

    def is_cur_player_in_check(self):

        if self._cur_player_is_white:
            cur_king = self.get_square(self._white_king_coords)
        else:
            cur_king = self.get_square(self._black_king_coords)

        res, err = cur_king.is_in_check(self)

        return res, err

    def move_piece(self, piece_square, new_square):

        piece_sq = self.get_square(piece_square)
        new_sq = self.get_square(new_square)

        # CASTLING
        if piece_square == self._black_king_coords or piece_square == self._white_king_coords:
            x_dir = piece_square[0] - new_square[0]
            if abs(x_dir) > 1:
                self._move_rook_when_castling(new_square, x_dir)

        # PAWN PROMOTION
        # TODO: Allow to choose how pawn is promoted
        if self.check_if_pawn_promotion(piece_square, new_square):
            piece_sq = Queen(piece_square, self._cur_player_is_white)

        # Update king position if king was moved
        if piece_square == self._black_king_coords:
            self._black_king_coords = new_square
        elif piece_square == self._white_king_coords:
            self._white_king_coords = new_square

        piece_sq.move(new_square)

        # Record that piece has been taken.
        if new_sq.is_piece():
            self._taken_pieces.append(new_sq)

        self.set_square(new_square, piece_sq)
        self.set_square(piece_square, Square(piece_square))

    def check_if_pawn_promotion(self, piece_square, new_square):
        sq = self.get_square(piece_square)
        if sq.char_rep() == Pawn.char_rep():
            if new_square[1] == 0 or new_square[1] == self._board_size-1:
                return True
        return False

    def _move_rook_when_castling(self, new_square, x_dir):
        # Rook should go next to king, towards the centre.
        if x_dir > 0:
            logging.info(f"Casting long: {new_square}")
            new_rook_x = new_square[0] + 1
            former_rook_x = 0
        else:
            logging.info(f"Casting short: {new_square}")
            new_rook_x = new_square[0] - 1
            former_rook_x = self._board_size-1

        new_rook_square = (new_rook_x, new_square[1])
        r = Rook(new_rook_square, self._cur_player_is_white)
        r.set_has_moved(True)

        self.set_square(new_rook_square, r)
        self.set_square((former_rook_x, new_square[1]), Square((former_rook_x, new_square[1])))

    @staticmethod
    def _create_pawn_promotion_piece(piece_square, piece_type, is_white):
        if piece_type == Rook.char_rep():
            return Rook(piece_square, is_white)
        elif piece_type == Knight.char_rep():
            return Knight(piece_square, is_white)
        elif piece_type == Bishop.char_rep():
            return Bishop(piece_square, is_white)
        else:
            return Queen(piece_square, is_white)

    def list_valid_moves_for_piece(self, piece_square):
        valid_moves = []
        for x in range(self._board_size):
            for y in range(self._board_size):
                res, _ = self.check_if_move_valid(piece_square, (x,y))
                if res:
                    valid_moves.append((x, y))
        return valid_moves

    def list_valid_moves_for_player(self):
        possible_moves = []
        for x in range(self._board_size):
            for y in range(self._board_size):
                sq = self.get_square((x, y))
                if sq.is_piece() and sq.is_white() == self._cur_player_is_white:
                    pieces_moves = self.list_valid_moves_for_piece((x, y))
                    for p_m in pieces_moves:
                        possible_moves.append(p_m)
        return possible_moves

    def is_stalemate_or_checkmate(self):
        x = self.list_valid_moves_for_player()
        if len(x) == 0:
            res, _ = self.is_cur_player_in_check()
            if res:
                return "CHECKMATE"
            else:
                return "STALEMATE"
        return None


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

    @is_landing_square_occupied
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

            return True, ""

        else:
            # Pawns capture 1 square diagonally.
            if y_diff != 1:
                return False, "Pawns only capture 1 square diagonally."

            square_to_check = board.get_square(new_square)
            if not square_to_check.is_piece():
                return False, "Cannot move diagonally unless it's a capture."

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

    @is_landing_square_occupied
    def is_valid_move(self, new_square, board):
        logging.info("Checking validity of Rook move from {} to {}".format(self._cur_square, new_square))
        x_diff = self._cur_square[0] - new_square[0]
        y_diff = self._cur_square[1] - new_square[1]

        # Rooks can only move along one axis at a time.
        if abs(x_diff) > 0 and abs(y_diff) > 0:
            return False, "Rooks can only move along one axis at a time."

        loop_inc = -1
        if x_diff < 0 or y_diff < 0:
            loop_inc = 1

        # Check for pieces between cur square and new square.
        if abs(y_diff) > 0:
            # Check all squares leading up to landing square for pieces.
            for y in range(self._cur_square[1] + loop_inc, new_square[1], loop_inc):
                tmp_coord = (self._cur_square[0], y)
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

    @is_landing_square_occupied
    def is_valid_move(self, new_square, board):
        cur_square = self.get_cur_square()
        x_diff = cur_square[0] - new_square[0]
        y_diff = cur_square[1] - new_square[1]

        if abs(x_diff) != abs(y_diff):
            return False, "Bishops only move diagonally!"

        x_inc = -1
        if x_diff < 0:
            x_inc = 1

        y_inc = -1
        if y_diff < 0:
            y_inc = 1

        for i in range(1, abs(x_diff)):
            tmp_coord = (cur_square[0] + (i * x_inc), cur_square[1] + (i * y_inc))
            sq_to_check = board.get_square(tmp_coord)
            if sq_to_check.is_piece():
                return False, "Bishop is blocked by {} on {}".format(sq_to_check.long_name(), tmp_coord)

        return True, ""

    def move(self, new_square):
        logging.info("Updating Bishop variables after move")
        self._cur_square = new_square


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

    @is_landing_square_occupied
    def is_valid_move(self, new_square, board):
        cur_square = self.get_cur_square()
        x_diff = cur_square[0] - new_square[0]
        y_diff = cur_square[1] - new_square[1]

        abs_x = abs(x_diff)
        abs_y = abs(y_diff)

        if not (abs_x == 2 and abs_y == 1 or abs_x == 1 and abs_y == 2):
            return False, "Knights move in L-shapes. (1 square on one axis and 2 along another.)"

        return True, ""

    def move(self, new_square):
        logging.info("Updating Knight variables after move")
        self._cur_square = new_square


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

    @is_landing_square_occupied
    def is_valid_move(self, new_square, board):
        cur_square = self.get_cur_square()
        x_diff = cur_square[0] - new_square[0]
        y_diff = cur_square[1] - new_square[1]

        abs_x = abs(x_diff)
        abs_y = abs(y_diff)

        # Check if moving vertically/horizontally
        if not (abs_x > 0 and abs_y > 0):
            # TODO: Refactor Rook move validation into reusable function, remove this repetition.

            loop_inc = -1
            if x_diff < 0 or y_diff < 0:
                loop_inc = 1

            if abs_y > 0:
                # Check all squares leading up to landing square for pieces.
                for y in range(self._cur_square[1] + loop_inc, new_square[1], loop_inc):
                    tmp_coord = (self._cur_square[0], y)
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

        # Check if moving diagonally
        elif abs_x == abs_y:

            # TODO: Refactor Bishop move validation into reusable function, remove this repetition.
            x_inc = -1
            if x_diff < 0:
                x_inc = 1

            y_inc = -1
            if y_diff < 0:
                y_inc = 1

            for i in range(1, abs(x_diff)):
                tmp_coord = (cur_square[0] + (i * x_inc), cur_square[1] + (i * y_inc))
                sq_to_check = board.get_square(tmp_coord)
                if sq_to_check.is_piece():
                    return False, "Bishop is blocked by {} on {}".format(sq_to_check.long_name(), tmp_coord)

        else:
            return False, "Queens move diagonally or in a straight line!"

        return True, ""

    def move(self, new_square):
        logging.info("Updating Queen variables after move")
        self._cur_square = new_square


class King(Piece, HasMovedMixin):
    def __init__(self, cur_square, is_white):
        super().__init__(cur_square=cur_square, is_white=is_white)
        logging.info("King initialised - coords: {}, is_white: {}".format(cur_square, is_white))

    @staticmethod
    def char_rep():
        return 'K'

    @staticmethod
    def long_name():
        return "King"

    def is_in_check(self, board):

        size = board.get_board_size()
        cur_square_coords = self.get_cur_square()

        direction = [1, -1]
        for x_dir in direction:
            x = cur_square_coords[0] + 1
            if x_dir > 0:
                x = size - cur_square_coords[0]

            for y_dir in direction:
                y = cur_square_coords[1] + 1
                if y_dir > 0:
                    y = size - cur_square_coords[1]

                # BISHOPS/QUEENS - Check if there are any enemy queens or bishops on open diagonals.
                loop_count = min([x, y])
                for i in range(1, loop_count):
                    sq_coords = (cur_square_coords[0] + (i * x_dir), cur_square_coords[1] + (i * y_dir))
                    sq = board.get_square(sq_coords)
                    if sq.is_piece():
                        if sq.is_white() != self.is_white():
                            if sq.char_rep() == Bishop.char_rep() or sq.char_rep() == Queen.char_rep():
                                return True, "In check: Enemy {} on {}".format(sq.long_name(), sq_coords)
                        break

                # KNIGHTS - If Knight is an L-shape away from king, then you're in check.
                knight_coords = [(cur_square_coords[0] + (2 * x_dir), cur_square_coords[1] + y_dir),
                                 (cur_square_coords[0] + x_dir, cur_square_coords[1] + (2 * y_dir))]

                for coord in knight_coords:
                    sq = board.get_square(coord)
                    if sq is not None and sq.char_rep() == Knight.char_rep() and self.is_white() != sq.is_white():
                        return True, "In check: Enemy {} on {}".format(sq.long_name(), coord)

                # ROOKS/QUEENS - Check if there are any enemy queens or rooks on open files
                for i in range(1, y):
                    sq_coords = (cur_square_coords[0], cur_square_coords[1] + (i * y_dir))
                    sq = board.get_square(sq_coords)
                    if sq.is_piece():
                        if sq.is_white() != self.is_white():
                            if sq.char_rep() == Rook.char_rep() or sq.char_rep() == Queen.char_rep():
                                return True, "In check: Enemy {} on {}".format(sq.long_name(), sq_coords)
                        break

            # ROOKS/QUEENS - Check if there are any enemy queens or rooks on open ranks
            for i in range(1, x):
                sq_coords = (cur_square_coords[0] + (i * x_dir), cur_square_coords[1])
                sq = board.get_square(sq_coords)
                if sq.is_piece():
                    if sq.is_white() != self.is_white():
                        if sq.char_rep() == Rook.char_rep() or sq.char_rep() == Queen.char_rep():
                            return True, "In check: Enemy {} on {}".format(sq.long_name(), sq_coords)
                    break

            # PAWNS - If Pawn is on top adjacent diagonal squares (bottom diagonals for white), then you're in check.
            if self.is_white():
                sq_coords = (cur_square_coords[0] + (1 * x_dir), cur_square_coords[1] + 1)
            else:
                sq_coords = (cur_square_coords[0] + (1 * x_dir), cur_square_coords[1] - 1)

            sq = board.get_square(sq_coords)

            if sq is not None and sq.char_rep() == Pawn.char_rep() and self.is_white() != sq.is_white():
                return True, "In check: Enemy {} on {}".format(sq.long_name(), sq_coords)

        # If King is adjacent its "check"
        square_to_check = [1, 0, -1]
        for x in square_to_check:
            for y in square_to_check:
                if x == 0 and y == 0:
                    continue

                sq_coords = (cur_square_coords[0] + x, cur_square_coords[1] + y)
                sq = board.get_square(sq_coords)
                if sq is not None and sq.char_rep() == King.char_rep():
                    return True, "In check: Enemy {} on {}".format(sq.long_name(),sq_coords)

        return False, ""

    @is_landing_square_occupied
    def is_valid_move(self, new_square, board):
        cur_square = self.get_cur_square()
        x_diff = cur_square[0] - new_square[0]
        y_diff = cur_square[1] - new_square[1]
        abs_x = abs(x_diff)
        abs_y = abs(y_diff)

        if self._has_moved is False and abs_x == 2 and abs_y == 0:
            if board.is_cur_player_in_check() is False:
                return False, "Cannot castle when in check"

            # TODO: If expanding for Chess960 rules, will need to be more dynamic.
            if x_diff > 0:
                rook_x = 0
                for i in range(rook_x+1, cur_square[0]):
                    piece = board.get_square((i, cur_square[1]))
                    if piece.is_piece():
                        return False, "Cannot castle, {} on {}".format(piece.char_rep(), (i, cur_square[1]))

                # Would king be in check if moved to any of travelled squares?
                for i in range(rook_x+2, cur_square[0]):
                    tmp_board = deepcopy(board)
                    tmp_board.move_piece(cur_square, (i, cur_square[1]))
                    is_check, err = tmp_board.is_cur_player_in_check()
                    if is_check is True:
                        return False, "Cannot castle, Would result in check on {}".format((i, cur_square[1]))

            else:
                rook_x = 7
                for i in range(cur_square[0]+1, rook_x):
                    piece = board.get_square((i, cur_square[1]))
                    if piece.is_piece():
                        return False, "Cannot castle, {} on {}".format(piece.char_rep(), (i, cur_square[1]))

                for i in range(cur_square[0]+1, rook_x-1):
                    tmp_board = deepcopy(board)
                    tmp_board.move_piece(cur_square, (i, cur_square[1]))
                    is_check, err = tmp_board.is_cur_player_in_check()
                    if is_check is True:
                        return False, "Cannot castle, Would result in check on {}".format((i, cur_square[1]))

            rook = board.get_square((rook_x, cur_square[1]))
            if rook.char_rep() != Rook.char_rep() or rook.get_has_moved() is True:
                return False, "Rook on {} has already moved!".format((rook_x, cur_square[1]))

            return True, ""

        if abs_x > 1 or abs_y > 1:
            return False, "The King can only move one square at a time!"

        return True, ""

    def move(self, new_square):
        logging.info("Updating Rook variables after move")
        self._cur_square = new_square
        if not self.get_has_moved():
            self.set_has_moved(True)
