import unittest

import pieces


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board1 = pieces.Board()
        self.board2 = pieces.Board()
        
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

        self.assertEqual(square1, self.board1._board[3][2])
        self.assertEqual(square2, self.board2._board[7][7])



if __name__ == '__main__':
    unittest.main()
