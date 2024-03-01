import pyglet
from pyglet.media import Player
from pyglet.shapes import Circle
from pyglet.window import key
from pyglet.text import Label
from pyglet.resource import image
from audio_load import AudioLoad

# Constants for colors
WHITE = (255, 255, 255, 255)
YELLOW = (255, 199, 95, 255)
BLUE = (0, 0, 255, 255)
ORANGE = (255, 130, 5, 255)


# Class that shows the stage select menu and handles logic related to navigating it
class StageSelectMenu:
    def __init__(self, window):
        # Establishes the window context
        self.window = window
        # To help navigate through the different stages
        self.stage_options = [
            "Stage 1: Cyber Adagio",
            "Stage 2: Lake Andante",
            "Stage 3: Space Vivace"
        ]
        # Selected vertical option
        self.selected_option = 0
        # Selected horizontal option (stage)
        self.selected_stage = 0
        # Paths to the stage background images
        self.stage_image_paths = ["images/stage1.jpg", "images/stage2.gif", "images/stage3.gif"]
        # Selected stage background image
        self.stage_image = image(self.stage_image_paths[self.selected_option])
        # Label for the selected stage option
        self.stage_label = Label(self.stage_options[self.selected_option], font_size=24,
                                 x=window.width // 2, y=window.height // 2 + 20, anchor_x="center",
                                 color=WHITE)
        # Label for the option that starts the game
        self.start_game_label = Label("Start Game", font_size=24, x=window.width // 2,
                                      y=window.height // 2 - 30, anchor_x="center",
                                      color=YELLOW)
        # Label for the option that returns the player to the main menu
        self.back_label = Label("Back", font_size=24, x=window.width // 2, y=window.height // 2 - 80,
                                anchor_x="center", color=YELLOW)

        # Loading sounds and initializing the different players
        AudioLoad.load_menu_sounds()
        self.menu_click_player = Player()
        self.menu_click_player.queue(AudioLoad.menu_click_sound)

        self.menu_select_player = Player()
        self.menu_select_player.queue(AudioLoad.menu_select_sound)

        self.stage_select_player = Player()
        self.stage_select_player.queue(AudioLoad.stage_select_sound)

        # Get the selected option
        self.selected_label = self.get_selected_label()

        # Blue circle properties
        self.blue_circle_radius = 10
        self.blue_circle_color = BLUE
        self.blue_circle_x = self.get_selected_label().x - 30
        self.blue_circle_y = self.get_selected_label().y

        # Method call to update the blue circle's position initially
        self.update_blue_circle_position()

        # Arrows properties (they'll show when the stage label is selected)
        self.arrow_size = 24
        self.arrow_color = BLUE
        self.arrow_left_x = self.stage_label.x - 180
        self.arrow_right_x = self.stage_label.x + 180
        self.arrow_y = self.stage_label.y

    # Method to draw all the different labels on screen, as well as the preview image
    def draw(self):
        # Create a sprite for the stage image
        stage_image_sprite = pyglet.sprite.Sprite(self.stage_image)

        # Scale the sprite to fill the window
        stage_image_sprite.scale_x = self.window.width / stage_image_sprite.width
        stage_image_sprite.scale_y = self.window.height / stage_image_sprite.height

        # Draw the stage image sprite
        stage_image_sprite.draw()

        # Draw blue circle next to the selected option, excluding the stage label
        if self.selected_label.color == WHITE and self.selected_label != self.stage_label:
            blue_circle = Circle(self.blue_circle_x, self.blue_circle_y, self.blue_circle_radius,
                                 color=self.blue_circle_color)
            blue_circle.draw()

        # Draw arrows when the stage label is selected
        if self.stage_label.color == WHITE:
            # Draw left arrow
            left_arrow_label = Label("◄", font_size=self.arrow_size, x=self.arrow_left_x, y=self.arrow_y,
                                     anchor_x="center", color=self.arrow_color)
            left_arrow_label.draw()

            # Draw right arrow
            right_arrow_label = Label("►", font_size=self.arrow_size, x=self.arrow_right_x, y=self.arrow_y,
                                      anchor_x="center", color=self.arrow_color)
            right_arrow_label.draw()

        # Draw the stage label
        self.stage_label.draw()

        # Draw the start game and back labels
        self.start_game_label.draw()
        self.back_label.draw()

    # Method to handle user input in this menu
    def handle_key_press(self, symbol):
        if symbol == key.ENTER:
            # Do nothing when pressing enter on the stage select option
            if self.stage_label.color == WHITE:
                pass
            # Start the game when the start label is selected
            elif self.start_game_label.color == WHITE:
                # Set the appropriate stage
                self.window.update_stage(self.selected_stage + 1)
                # Prepare a new round
                self.window.game.grab_new_word()
                # Start the game
                self.window.start()
            # Go back to the main menu when the back label is selected
            elif self.back_label.color == WHITE:
                # Change the current window context back to the main menu
                self.window.current_menu = self.window.main_menu
                self.get_menu_select_player().play()
        # For vertical menu traversing
        elif symbol == key.UP or symbol == key.DOWN:
            # Go up or down depending on key input
            self.update_vertical_selection(symbol)
            self.get_menu_click_player().play()
        # For horizontal menu traversing (stage picking)
        elif symbol == key.LEFT or symbol == key.RIGHT:
            # When the stage label is selected
            if self.stage_label.color == WHITE:
                # Go left or right depending on key input
                self.update_horizontal_selection(symbol)
                self.get_stage_select_player().play()
            # Do nothing when the other options are selected
            elif self.start_game_label.color == WHITE:
                pass
            elif self.back_label.color == WHITE:
                pass

    # Method to update the horizontal selection (stage picking)
    def update_horizontal_selection(self, symbol):
        # Advance forwards in the array when user presses right and backwards when user presses left
        direction = 1 if symbol == key.RIGHT else -1
        # Use of len (length) helps with not going out of bounds
        self.selected_stage = (self.selected_stage + direction) % len(self.stage_options)
        # Set the appropriate stage text
        self.stage_label.text = self.stage_options[self.selected_stage]
        # Set the stage's corresponding image
        self.stage_image = image(self.stage_image_paths[self.selected_stage])

    # # Method to update the horizontal selection (menu traversing)
    def update_vertical_selection(self, symbol):
        # Toggle the selection between "Stage", "Start Game", and "Back"
        if symbol == key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.stage_options)
        elif symbol == key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.stage_options)

        # Iterate through the different labels, assigning them a color depending on which one was previously selected
        for i, label in enumerate([self.stage_label, self.start_game_label, self.back_label]):
            if i == self.selected_option:
                label.color = WHITE
                self.selected_label = label
                # Also update the blue circle's position
                self.update_blue_circle_position()
            else:
                label.color = YELLOW

    # Method to update the position of the blue circle next to the selected option
    def update_blue_circle_position(self):
        self.blue_circle_x = self.selected_label.x - self.selected_label.content_width / 2 - self.blue_circle_radius - 10
        self.blue_circle_y = self.selected_label.y + 12

    # Method to get the currently selected label by checking the colors
    def get_selected_label(self):
        return self.back_label if self.back_label.color == WHITE else self.start_game_label

    # Getter methods for returning the different sound players (useful for being called from the GameWindow class)
    def get_menu_click_player(self):
        self.menu_click_player = Player()
        self.menu_click_player.queue(AudioLoad.menu_click_sound)
        self.menu_click_player.seek(0)
        return self.menu_click_player

    def get_menu_select_player(self):
        self.menu_select_player = Player()
        self.menu_select_player.queue(AudioLoad.menu_select_sound)
        self.menu_select_player.seek(0)
        return self.menu_select_player

    def get_stage_select_player(self):
        self.stage_select_player = Player()
        self.stage_select_player.queue(AudioLoad.menu_select_sound)
        self.stage_select_player.seek(0)
        return self.stage_select_player
