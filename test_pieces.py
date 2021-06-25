import unittest

import pieces


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board1 = pieces.Board()
        self.board2 = pieces.Board()

    def test_initialize_board(self):
        # Confirm that all pieces are assigned in correct location and that initial vars are set correctly
        pass
        
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
    pass


class TestPawn(unittest.TestCase):
    pass


class TestRook(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
