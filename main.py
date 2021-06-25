import logging
import os

import pieces


def get_coordinate_pair(board_size):
    successful_input = False

    while not successful_input:
        try:
            piece_x = int(input("Enter x coordinate: "))
            piece_y = int(input("Enter y coordinate: "))

            if piece_x < 1 or piece_x > board_size:
                raise ValueError

            if piece_y < 1 or piece_y > board_size:
                raise ValueError

            successful_input = True
        except ValueError:
            print("INVALID, choose an int between 1 and 8 ")
            successful_input = False

    return (piece_x, piece_y)


def process_player_move(board):


    confirm = False
    while confirm is False:

        res = False
        while res is False:
            print("Select piece to move")
            select_piece = get_coordinate_pair(board.get_board_size())
            res, err_msg = board.check_if_selection_valid(select_piece)

            if res is False:
                print(err_msg)

        res = False
        while res is False:
            print("select square to move {} on {}".format(select_piece, board.get_square(select_piece).long_name()))
            square_to_move = get_coordinate_pair(board.get_board_size())
            res, err_msg = board.check_if_move_valid(select_piece, square_to_move)

            if res is False:
                print(err_msg)

        successful_confirm = False
        while successful_confirm is False:
            confirm_input = str(input("Confirm move (y/n): ")).strip().lower()
            if confirm_input == "y" or confirm_input == "yes":
                confirm = True
                successful_confirm = True
            elif confirm_input == "n" or "no":
                confirm = False
                successful_confirm = True
            else:
                print("Please write \'yes\' or \'no\'.")

        board.move_piece(select_piece, square_to_move)

    logging.info("Square selected: {}, Square to move to: {}".format(select_piece, square_to_move))


def main():
    logging.basicConfig(filename="app.log", format='%(asctime)s - %(message)s', level=logging.INFO)

    cur_player = "white"
    turn = 1

    board = pieces.Board()

    while turn < 10:
        os.system('clear')
        board.pprint_board()
        print("White to move - Turn {}".format(turn))
        process_player_move(board)
        board.change_player()

        board.pprint_board()
        print("Black to move - Turn {}".format(turn))
        process_player_move(board)
        board.change_player()
        turn += 1


if __name__ == '__main__':
    main()
