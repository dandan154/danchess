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


class ChessGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ALMOND)

        self.board = pieces.Board()

        self.tile_count_x = self.board.get_board_size()
        self.tile_count_y = self.board.get_board_size()

        self.tile_draw_start_x = int(SCREEN_WIDTH / 2) - (SQUARE_WIDTH * ((self.tile_count_x/2)-1) + (SQUARE_WIDTH/2))
        self.tile_draw_start_y = int(SCREEN_HEIGHT / 2) - (SQUARE_HEIGHT * ((self.tile_count_y/2)-1) + (SQUARE_HEIGHT/2))

    def setup(self):
        pass

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
        # Draw letters along bottom of board
        for y in range(self.tile_count_y):
            arcade.draw_text(
                str(y+1),
                self.tile_draw_start_x- SQUARE_WIDTH,
                self.tile_draw_start_y + SQUARE_WIDTH * y - 10,
                arcade.color.BLACK,
                18,

            )


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass

class Piece(arcade.Sprite):
    pass


def main():
    window = ChessGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
