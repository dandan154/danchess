import logging
import arcade
import arcade.gui

from string import ascii_uppercase

import pieces

# Screen constants
SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1024
SCREEN_TITLE = "DanChess"


# Square constants
SQUARE_HEIGHT = 80
SQUARE_WIDTH = 80

# Margins
BOARD_X_OFFSET = -100
BOARD_Y_OFFSET = 0
LETTER_OFFSET = 10
NUMBER_OFFSET = 10
OUTLINE_MARGIN_WIDTH = 5

# Piece constants
PIECE_HEIGHT = 40
PIECE_WIDTH = 40
IMAGE_SCALE = 3.2

# Colours
BLACK_SQUARE_COLOUR = arcade.color.ARSENIC
WHITE_SQUARE_COLOUR = arcade.color.LIGHT_GRAY
SELECTED_SQUARE_COLOUR = arcade.color.ARYLIDE_YELLOW
POTENTIAL_SQUARE_COLOUR = arcade.color.ANDROID_GREEN
CHECK_COLOUR = arcade.color.DARK_PASTEL_RED

MAIN_MENU_BACKGROUND = arcade.color.DARK_BYZANTIUM
MAIN_MENU_TEXT = arcade.color.WHITE_SMOKE


SPRITE_LOOKUP_DICT = {
    "B(B)": "bishop-black-16x16.png",
    "B(W)": "bishop-white-16x16.png",
    "K(B)": "king-black-16x16.png",
    "K(W)": "king-white-16x16.png",
    "N(B)": "knight-black-16x16.png",
    "N(W)": "knight-white-16x16.png",
    "P(B)": "pawn-black-16x16.png",
    "P(W)": "pawn-white-16x16.png",
    "Q(B)": "queen-black-16x16.png",
    "Q(W)": "queen-white-16x16.png",
    "R(B)": "rook-black-16x16.png",
    "R(W)": "rook-white-16x16.png",
    "0": None
}


class MainMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(MAIN_MENU_BACKGROUND)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("DANCHESS", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         MAIN_MENU_TEXT, font_size=50, anchor_x="center")
        arcade.draw_text("Click to start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         MAIN_MENU_TEXT, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        chess_view = ChessView()
        chess_view.setup()
        self.window.show_view(chess_view)


class VictoryView(arcade.View):
    def __init__(self, was_stalemate, winner_was_white):
        super().__init__()
        if was_stalemate:
            self.title_text = "STALEMATE"
            self.display_text = "ITS A DRAW: 1/2 - 1/2"
            self.font_color = arcade.color.DARK_GRAY
            self.background_color = arcade.color.LIGHT_GRAY
        else:
            self.title_text = "CHECKMATE"
            if winner_was_white:
                self.display_text = "WHITE WAS VICTORIOUS: 1 - 0"
                self.font_color = arcade.color.BLACK
                self.background_color = arcade.color.WHITE_SMOKE

            else:
                self.display_text = "BLACK WAS VICTORIOUS: 0 - 1"
                self.font_color = arcade.color.WHITE_SMOKE
                self.background_color = arcade.color.BLACK

    def on_show(self):
        arcade.set_background_color(self.background_color)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.title_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100,
                         self.font_color, font_size=80, anchor_x="center")

        arcade.draw_text(self.display_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         self.font_color, font_size=30, anchor_x="center")
        arcade.draw_text("Click to return to main menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         self.font_color, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        main_menu_view = MainMenuView()
        self.window.show_view(main_menu_view)


class ChessView(arcade.View):
    def __init__(self):
        super().__init__()

        # GAME VARS
        self.board = pieces.Board()
        self.piece_selected = None
        self.piece_selected_moves = None

        self.is_white_perspective_active = True
        self.highlight_checked_king = False
        self.show_possible_moves_active = False

        # RENDERING LOGIC
        arcade.set_background_color(arcade.color.ALMOND)

        self.tile_count_x = self.board.get_board_size()
        self.tile_count_y = self.board.get_board_size()

        self.tile_draw_start_x = int(SCREEN_WIDTH / 2)
        self.tile_draw_start_y = int(SCREEN_HEIGHT / 2)

        self.tile_draw_start_x -= (SQUARE_WIDTH * ((self.tile_count_x/2)-1) + (SQUARE_WIDTH/2))
        self.tile_draw_start_y -= (SQUARE_HEIGHT * ((self.tile_count_y/2)-1) + (SQUARE_HEIGHT/2))

        self.tile_draw_start_x += BOARD_X_OFFSET
        self.tile_draw_start_y += BOARD_Y_OFFSET

        self.chess_piece_sprite_list = None

    def setup(self):
        self._gen_piece_placement()

    def on_draw(self):
        arcade.start_render()

        self._draw_board()
        self.chess_piece_sprite_list.draw()

    def _gen_piece_placement(self):
        oriented_board = self.board.get_board()

        self.chess_piece_sprite_list = arcade.SpriteList()

        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):

                piece_img_path = SPRITE_LOOKUP_DICT[str(oriented_board[y][x])]  # Reverse x and y for proper orientation

                if piece_img_path is not None:
                    piece_sprite = arcade.Sprite(
                        "resources/images/{}".format(piece_img_path),
                        IMAGE_SCALE
                    )

                    if self.is_white_perspective_active:
                        piece_sprite.center_x = self.tile_draw_start_x + SQUARE_WIDTH * x
                        piece_sprite.center_y = self.tile_draw_start_y + SQUARE_HEIGHT * y
                    else:
                        piece_sprite.center_x = self.tile_draw_start_x + SQUARE_WIDTH * (self.tile_count_x - 1 - x)
                        piece_sprite.center_y = self.tile_draw_start_y + SQUARE_HEIGHT * (self.tile_count_y - 1 - y)

                    self.chess_piece_sprite_list.append(piece_sprite)

    def _draw_board(self):
        # Draw Squares of Board
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if (x + y) % 2:
                    arcade.draw_rectangle_filled(
                        self.tile_draw_start_x + SQUARE_WIDTH * x,
                        self.tile_draw_start_y + SQUARE_HEIGHT * y,
                        SQUARE_WIDTH,
                        SQUARE_HEIGHT,
                        WHITE_SQUARE_COLOUR
                    )
                else:
                    arcade.draw_rectangle_filled(
                        self.tile_draw_start_x + SQUARE_WIDTH * x,
                        self.tile_draw_start_y + SQUARE_HEIGHT * y,
                        SQUARE_WIDTH,
                        SQUARE_HEIGHT,
                        BLACK_SQUARE_COLOUR
                    )

        # Draw Outline around board.
        arcade.draw_rectangle_outline(
            (SCREEN_WIDTH / 2) + BOARD_X_OFFSET,
            (SCREEN_HEIGHT / 2) + BOARD_Y_OFFSET,
            (self.tile_count_x * SQUARE_WIDTH) + OUTLINE_MARGIN_WIDTH,
            (self.tile_count_y * SQUARE_HEIGHT) + OUTLINE_MARGIN_WIDTH,
            arcade.color.BLACK,
            OUTLINE_MARGIN_WIDTH
        )

        file_chars = ascii_uppercase[:self.tile_count_x]
        if self.is_white_perspective_active is False:
            file_chars = file_chars[::-1]

        # Draw letters along bottom of board
        for x in range(self.tile_count_x):
            arcade.draw_text(
                file_chars[x],
                self.tile_draw_start_x + SQUARE_WIDTH * x - LETTER_OFFSET,
                self.tile_draw_start_y - SQUARE_HEIGHT,
                arcade.color.BLACK,
                18,
            )

        rank_chars = "12345678"
        if self.is_white_perspective_active is False:
            rank_chars = rank_chars[::-1]

        # Draw numbers along side of board
        for y in range(self.tile_count_y):
            arcade.draw_text(
                rank_chars[y],
                self.tile_draw_start_x - SQUARE_WIDTH,
                self.tile_draw_start_y + SQUARE_WIDTH * y - NUMBER_OFFSET,
                arcade.color.BLACK,
                18,
            )

        # Draw highlight around checked king
        if self.highlight_checked_king:
            king_coords = self.board.get_cur_king_coords()
            if self.is_white_perspective_active:
                select_x = king_coords[0]
                select_y = king_coords[1]
            else:
                select_x = self.tile_count_x - 1 - king_coords[0]
                select_y = self.tile_count_y - 1 - king_coords[1]

            arcade.draw_rectangle_filled(
                self.tile_draw_start_x + (SQUARE_WIDTH * select_x),
                self.tile_draw_start_y + (SQUARE_HEIGHT * select_y),
                SQUARE_WIDTH,
                SQUARE_HEIGHT,
                CHECK_COLOUR
            )

        # Draw highlight around selected piece and possible squares
        if self.piece_selected is not None:
            if self.is_white_perspective_active:
                select_x = self.piece_selected[0]
                select_y = self.piece_selected[1]
            else:
                select_x = self.tile_count_x - 1 - self.piece_selected[0]
                select_y = self.tile_count_y - 1 - self.piece_selected[1]

            arcade.draw_rectangle_filled(
                self.tile_draw_start_x + (SQUARE_WIDTH * select_x),
                self.tile_draw_start_y + (SQUARE_HEIGHT * select_y),
                SQUARE_WIDTH,
                SQUARE_HEIGHT,
                SELECTED_SQUARE_COLOUR
            )

            if self.show_possible_moves_active:
                # Highlight squares that piece can move to:
                for square in self.piece_selected_moves:
                    if self.is_white_perspective_active:
                        possible_x = square[0]
                        possible_y = square[1]
                    else:
                        possible_x = self.tile_count_x - 1 - square[0]
                        possible_y = self.tile_count_y - 1 - square[1]

                    arcade.draw_ellipse_filled(
                        self.tile_draw_start_x + (SQUARE_WIDTH * possible_x),
                        self.tile_draw_start_y + (SQUARE_HEIGHT * possible_y),
                        SQUARE_WIDTH/2,
                        SQUARE_HEIGHT/2,
                        POTENTIAL_SQUARE_COLOUR
                    )
                    arcade.draw_ellipse_outline(
                        self.tile_draw_start_x + (SQUARE_WIDTH * possible_x),
                        self.tile_draw_start_y + (SQUARE_HEIGHT * possible_y),
                        SQUARE_WIDTH/2,
                        SQUARE_HEIGHT/2,
                        arcade.color.BLACK,
                        3,
                        num_segments=150
                    )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        clicked_tile = self._calc_board_coord(x, y)

        # Check if a piece has been selected
        if clicked_tile[0] < 0 or clicked_tile[0] > (self.board.get_board_size()-1):
            return

        if clicked_tile[1] < 0 or clicked_tile[1] > (self.board.get_board_size()-1):
            return

        # Reverse selected tile if playing as Black
        if not self.is_white_perspective_active:
            clicked_tile = (self.tile_count_x - 1 - clicked_tile[0], self.tile_count_y - 1 - clicked_tile[1])

        if self.piece_selected is None:
            selection_is_valid, err = self.board.check_if_selection_valid(clicked_tile)

            if selection_is_valid:
                self.piece_selected = clicked_tile
                self.piece_selected_moves = self.board.list_valid_moves_for_piece(self.piece_selected)
        else:

            move_is_valid, err = self.board.check_if_move_valid(self.piece_selected, clicked_tile)

            if move_is_valid:
                self.board.move_piece(self.piece_selected, clicked_tile)
                self.board.change_player()
                self._gen_piece_placement()
                self.highlight_checked_king, _ = self.board.is_cur_player_in_check()

                x = self.board.is_statemate_or_checkmate()
                if x is not None:
                    if x == "CHECKMATE":
                        victory_view = VictoryView(False, not self.board.is_cur_player_white())
                    else:
                        victory_view = VictoryView(True, not self.board.is_cur_player_white())
                    self.window.show_view(victory_view)

            self.piece_selected = None
            self.piece_selected_moves = None

    def _calc_board_coord(self, x, y):
        file = x - self.tile_draw_start_x + (SQUARE_WIDTH/2)
        file = int(file // SQUARE_WIDTH)

        rank = y - self.tile_draw_start_y + (SQUARE_HEIGHT/2)
        rank = int(rank // SQUARE_HEIGHT)

        return file, rank

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.is_white_perspective_active = not self.is_white_perspective_active
            self._gen_piece_placement()
        elif symbol == arcade.key.ENTER:
            self.show_possible_moves_active = not self.show_possible_moves_active
        elif symbol == arcade.key.ESCAPE:
            exit(0)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass


def main():

    logging.basicConfig(filename="app.log", format='%(asctime)s - %(message)s', level=logging.INFO)

    # MAIN SCRIPT
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
