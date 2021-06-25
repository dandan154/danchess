import logging
import pieces

def get_coordinate_pair(board):
    successful_input = False

    while not successful_input:
        try:
            piece_x = int(input("Enter x coordinate of piece: "))
            piece_y = int(input("Enter y coordinate of piece: "))

            if piece_x < 0 or piece_x > board.get_size()-1:
                raise ValueError

            if piece_y < 0 or piece_y > board.get_size()-1:
                raise ValueError

            res, msg = board.check_if_selection_valid()

        except ValueError:
            print("INVALID, choose an int between 1 and 8")
            successful_input = False

    return (piece_x, piece_y)

def get_move():




    logging.info("Square selected: {}, Square to move to: {}".format((piece_x, piece_y), (square_x, square_y)))
    return (piece_x, piece_y), (square_x, square_y)


def main():
    logging.basicConfig(filename="app.log", format='%(asctime)s - %(message)s', level=logging.INFO)

    cur_player = "white"
    turn = 1

    board = pieces.Board()
    board.pprint_board()

    select_square, new_square = get_move()


if __name__ == '__main__':
    main()
