import arcade
import pieces

from string import ascii_uppercase

# Screen constants
SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1024
SCREEN_TITLE = "DanChess"


# Square constants
SQUARE_HEIGHT = 80
SQUARE_WIDTH = 80

# Piece constants
PIECE_HEIGHT = 40
PIECE_WIDTH = 40
IMAGE_SCALE = 3.0

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


class ChessView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)

        self.board = pieces.Board()

        self.tile_count_x = self.board.get_board_size()
        self.tile_count_y = self.board.get_board_size()

        self.tile_draw_start_x = int(SCREEN_WIDTH / 2) - (SQUARE_WIDTH * ((self.tile_count_x/2)-1) + (SQUARE_WIDTH/2))
        self.tile_draw_start_y = int(SCREEN_HEIGHT / 2) - (SQUARE_HEIGHT * ((self.tile_count_y/2)-1) + (SQUARE_HEIGHT/2))

        self.chess_piece_sprite_list = None

    def setup(self):

        #Create initial sprite list for pieces
        self.chess_piece_sprite_list = arcade.SpriteList()
        oriented_board = self.board.get_board()
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                piece_img_path = SPRITE_LOOKUP_DICT[str(oriented_board[x][y])]
                if piece_img_path is not None:
                    piece_sprite = arcade.Sprite(
                        "images/{}".format(piece_img_path),
                        IMAGE_SCALE
                    )
                    piece_sprite.center_x = self.tile_draw_start_x + SQUARE_WIDTH * x
                    piece_sprite.center_y = self.tile_draw_start_y + SQUARE_HEIGHT * y

                    self.chess_piece_sprite_list.append(piece_sprite)

    def on_draw(self):
        arcade.start_render()

        # Draw Squares of Board
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                tmp_colour = arcade.color.LIGHT_GRAY
                if (x + y) % 2:
                    tmp_colour = arcade.color.ARSENIC

                arcade.draw_rectangle_filled(
                    self.tile_draw_start_x + SQUARE_WIDTH * x,
                    self.tile_draw_start_y + SQUARE_HEIGHT * y,
                    SQUARE_WIDTH,
                    SQUARE_HEIGHT,
                    tmp_colour
                )

        # Draw Outline around board.
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT/2,
            self.tile_draw_start_x + int(SQUARE_WIDTH * 5.1),
            self.tile_draw_start_x + int(SQUARE_HEIGHT * 5.1),
            arcade.color.BLACK,
            5
        )

        # Draw letters along bottom of board
        for x in range(self.tile_count_x):
            arcade.draw_text(
                ascii_uppercase[x],
                self.tile_draw_start_x + SQUARE_WIDTH * x - 10,
                self.tile_draw_start_y - SQUARE_HEIGHT,
                arcade.color.BLACK,
                18,
            )

        # Draw numbers along side of board
        for y in range(self.tile_count_y):
            arcade.draw_text(
                str(y+1),
                self.tile_draw_start_x- SQUARE_WIDTH,
                self.tile_draw_start_y + SQUARE_WIDTH * y - 10,
                arcade.color.BLACK,
                18,
            )

        self.chess_piece_sprite_list.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        clicked_tile = self._calc_board_coord(x, y)

        # Check if a piece has been selected
        if clicked_tile[0] < 0 or clicked_tile[0] > (self.board.get_board_size()-1):
            return

        if clicked_tile[1] < 0 or clicked_tile[1] > (self.board.get_board_size()-1):
            return

        print(clicked_tile)

    def _calc_board_coord(self, x, y):
        file = x - self.tile_draw_start_x + (SQUARE_WIDTH/2)
        file = file // SQUARE_WIDTH

        rank = y - self.tile_draw_start_y + (SQUARE_HEIGHT/2)
        rank = rank // SQUARE_HEIGHT

        return file, rank

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    chess_view = ChessView()

    window.show_view(chess_view)
    chess_view.setup()

    arcade.run()


if __name__ == "__main__":
    main()
