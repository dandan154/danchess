import unittest

import pieces


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board1 = pieces.Board()
        self.board2 = pieces.Board()

    def test_initialize_board(self):
        # Confirm that all pieces are assigned in correct location and that initial vars are set correctly
        for x in range(2, self.board1._board_size-2):
            for y in range(2, self.board1._board_size-2):
                square = self.board1._board[x][y]
                self.assertIsInstance(square, pieces.Square)
                self.assertEqual(square._cur_square, (x, y))

        # Confirm that second rank is all white pawns.
        for x in range(self.board1._board_size):
            pawn = self.board1._board[1][x]
            self.assertIsInstance(pawn, pieces.Pawn)
            self.assertEqual(pawn._cur_square, (x, 1))
            self.assertTrue(pawn.is_white())

        # Confirm that 7th rank is all black pawns
        for x in range(self.board1._board_size):
            pawn = self.board1._board[6][x]
            self.assertIsInstance(pawn, pieces.Pawn)
            self.assertEqual(pawn._cur_square, (x, 6))
            self.assertFalse(pawn.is_white())

        # Confirm corner squares are rooks of appropriate colours
        white_rook1 = self.board1._board[0][0]
        white_rook2 = self.board1._board[0][7]

        black_rook1 = self.board1._board[7][0]
        black_rook2 = self.board1._board[7][7]

        self.assertIsInstance(white_rook1, pieces.Rook)
        self.assertEqual(white_rook1._cur_square, (0,0))
        self.assertTrue(white_rook1.is_white())

        self.assertIsInstance(white_rook2, pieces.Rook)
        self.assertEqual(white_rook2._cur_square, (7,0))
        self.assertTrue(white_rook2.is_white())

        self.assertIsInstance(black_rook1, pieces.Rook)
        self.assertEqual(black_rook1._cur_square, (0,7))
        self.assertFalse(black_rook1.is_white())

        self.assertIsInstance(black_rook2, pieces.Rook)
        self.assertEqual(black_rook2._cur_square, (7,7))
        self.assertFalse(black_rook2.is_white())

    def test_get_square(self):
        square1 = pieces.Square((4, 4))
        square2 = pieces.Pawn((7, 7), True)

        self.board1._board[1][0] = square1
        self.board2._board[7][7] = square2

        self.assertEqual(self.board1.get_square((0,1)), square1)
        self.assertEqual(self.board2.get_square((7,7)), square2)

    def test_set_square(self):

        coord1 = (2, 3)
        coord2 = (7, 7)

        square1 = pieces.Square(coord1)
        square2 = pieces.Pawn(coord2, True)

        self.board1.set_square(coord1, square1)
        self.board2.set_square(coord2, square2)

        self.assertEqual(self.board1._board[3][2], square1)
        self.assertEqual(self.board2._board[7][7], square2)

    def test_get_board_size(self):

        val1 = 12345
        val2 = 99999

        self.board1._board_size = val1
        self.board2._board_size = val2

        self.assertEqual(self.board1.get_board_size(), val1)
        self.assertEqual(self.board2.get_board_size(), val2)

    def test_change_player(self):

        self.board1._cur_player_is_white = True
        self.board2._cur_player_is_white = False

        self.board1.change_player()
        self.board2.change_player()

        self.assertFalse(self.board1._cur_player_is_white)
        self.assertTrue(self.board2._cur_player_is_white)

        self.board1.change_player()
        self.board2.change_player()

        self.assertTrue(self.board1._cur_player_is_white)
        self.assertFalse(self.board2._cur_player_is_white)

    def test_check_if_selection_valid(self):

        coord1 = (1, 2)
        coord2 = (3, 4)
        square1 = pieces.Square(coord1)
        square2 = pieces.Square(coord2)

        white_pawn1 = pieces.Pawn(coord1, True)
        white_pawn2 = pieces.Pawn(coord2, True)

        black_pawn1 = pieces.Pawn(coord1, False)
        black_pawn2 = pieces.Pawn(coord2, False)

        # Should return False and error message if square selected is not a piece.
        self.board1._board[coord1[1]][coord1[0]] = square1
        self.board2._board[coord2[1]][coord2[0]] = square2

        res1, err1 = self.board1.check_if_selection_valid(coord1)
        res2, err2 = self.board2.check_if_selection_valid(coord2)

        self.assertFalse(res1)
        self.assertFalse(res2)
        self.assertEqual("Selected square {} doesn't contain a piece".format(coord1), err1)
        self.assertEqual("Selected square {} doesn't contain a piece".format(coord2), err2)

        # Should return False and error message if square is a piece but piece doesn't belong to current player.
        self.board1._board[coord1[1]][coord1[0]] = black_pawn1
        self.board2._board[coord2[1]][coord2[0]] = black_pawn2

        res1, err1 = self.board1.check_if_selection_valid(coord1)
        res2, err2 = self.board2.check_if_selection_valid(coord2)

        self.assertFalse(res1)
        self.assertFalse(res2)
        self.assertEqual("Selected Pawn on {} is not your piece!".format(coord1), err1)
        self.assertEqual("Selected Pawn on {} is not your piece!".format(coord2), err2)

        # Should Return True if Piece belongs to player
        self.board1._board[coord1[1]][coord1[0]] = white_pawn1
        self.board2._board[coord2[1]][coord2[0]] = white_pawn2

        res1, err1 = self.board1.check_if_selection_valid(coord1)
        res2, err2 = self.board2.check_if_selection_valid(coord2)

        self.assertTrue(res1)
        self.assertTrue(res2)
        self.assertEqual("", err1)
        self.assertEqual("", err2)

    def test_check_if_move_valid(self):
        pass

    def test_move_piece(self):
        pass


class TestSquare(unittest.TestCase):

    def setUp(self):
        self.coords1 = (1, 2)
        self.coords2 = (2, 1)

        self.square1 = pieces.Square(self.coords1)
        self.square2 = pieces.Square(self.coords2)

    def test_is_piece(self):
        self.assertFalse(self.square1.is_piece())
        self.assertFalse(self.square2.is_piece())

    def test_char_rep(self):
        self.assertEqual(self.square1.char_rep(), '0')
        self.assertEqual(self.square2.char_rep(), '0')

    def test_long_name(self):
        self.assertEqual(self.square1.long_name(), "Square")
        self.assertEqual(self.square2.long_name(), "Square")

    def test_get_cur_square(self):
        self.assertEqual(self.square1.get_cur_square(), self.coords1)
        self.assertEqual(self.square2.get_cur_square(), self.coords2)


class TestPiece(unittest.TestCase):

    def setUp(self):
        self.coords1 = (1, 2)
        self.coords2 = (2, 1)

        self.piece1 = pieces.Piece(True, cur_square=self.coords1)
        self.piece2 = pieces.Piece(False, cur_square=self.coords2)

    def test_is_valid_move(self):
        res1, err1 = self.piece1.is_valid_move((1,2), None)
        res2, err2 = self.piece2.is_valid_move((2,2), None)

        self.assertFalse(res1)
        self.assertEqual(err1, "No move rules are defined for this - coords: {}".format(self.coords1))

        self.assertFalse(res2)
        self.assertEqual(err2, "No move rules are defined for this - coords: {}".format(self.coords2))


class TestPawn(unittest.TestCase):

    def setUp(self):

        self.coords1 = (1, 2)
        self.coords2 = (3, 4)

        self.white_pawn1 = pieces.Pawn(self.coords1, True)
        self.white_pawn2 = pieces.Pawn(self.coords2, True)

        self.black_pawn1 = pieces.Pawn(self.coords1, False)
        self.black_pawn2 = pieces.Pawn(self.coords2, False)

    def test_is_piece(self):

        self.assertTrue(self.white_pawn1.is_piece())
        self.assertTrue(self.white_pawn2.is_piece())
        self.assertTrue(self.black_pawn1.is_piece())
        self.assertTrue(self.black_pawn2.is_piece())

    def test_char_rep(self):

        rep = 'P'
        self.assertEqual(rep, self.white_pawn1.char_rep())
        self.assertEqual(rep, self.white_pawn2.char_rep())
        self.assertEqual(rep, self.black_pawn1.char_rep())
        self.assertEqual(rep, self.black_pawn2.char_rep())

    def test_long_name(self):

        long_name = "Pawn"
        self.assertEqual(long_name, self.white_pawn1.long_name())
        self.assertEqual(long_name, self.white_pawn2.long_name())
        self.assertEqual(long_name, self.black_pawn1.long_name())
        self.assertEqual(long_name, self.black_pawn2.long_name())

    def test_is_white(self):

        self.assertTrue(self.white_pawn1.is_white())
        self.assertTrue(self.white_pawn2.is_white())
        self.assertFalse(self.black_pawn1.is_white())
        self.assertFalse(self.black_pawn2.is_white())

    def test_is_valid_move(self):
        pass

    def test_move(self):
        pass


class TestRook(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
