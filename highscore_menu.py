from pyglet.media import Player
from pyglet.shapes import Circle
from pyglet.sprite import Sprite
from pyglet.window import key
from pyglet.text import Label

from audio_load import AudioLoad
from highscore_manager import HighscoreManager
from image_load import ImageLoad

# Constants for colors
WHITE = (255, 255, 255, 255)
YELLOW = (255, 199, 95, 255)
BRIGHT_YELLOW = (255, 255, 0, 255)
SILVER = (192, 192, 192, 255)
BRONZE = (205, 127, 50, 255)
BLUE = (0, 0, 255, 255)
ORANGE = (255, 130, 5, 255)


# Class that shows the highscore and handles logic related to navigating it
class HighscoreMenu:
    def __init__(self, window):
        # Establishes the window context
        self.window = window
        # Indicates the currently selected stage
        self.selected_stage = 1
        # To help navigate through the different stages
        self.stages = [1, 2, 3]
        # Initialize an HighscoreManager object with the database to be used to show the highscores
        self.highscore_manager = HighscoreManager('highscores.db')
        # Dictionary whose keys are the stage numbers and the values are the list of highscores saved for each
        self.highscores = {stage: self.load_highscores_from_db(stage) for stage in self.stages}
        # Creation and positioning of the different labels
        self.back_label = Label("Back", font_size=24, x=window.width // 2, y=window.height // 2 - 250,
                                anchor_x="center", color=YELLOW)
        self.stage_label = Label("Stage: {}".format(self.selected_stage), font_size=24,
                                 x=window.width // 2, y=window.height // 2 + 50, anchor_x="center",
                                 color=YELLOW)
        self.score_labels = self.create_score_labels()
        self.highscores_label = Label("HIGHSCORES", font_size=36, x=window.width // 2, y=window.height - 50,
                                      anchor_x="center", color=ORANGE)

        # Initialize the stage preview image
        ImageLoad.load_images()
        stage_image = ImageLoad.stage_previews[self.selected_stage - 1]
        self.stage_preview = Sprite(stage_image, x=window.width // 2 - 127, y=window.height - 210)

        # Load the different menu sounds
        AudioLoad.load_menu_sounds()
        self.menu_click_player = Player()
        self.menu_click_player.queue(AudioLoad.menu_click_sound)

        self.menu_select_player = Player()
        self.menu_select_player.queue(AudioLoad.menu_select_sound)

        self.stage_select_player = Player()
        self.stage_select_player.queue(AudioLoad.stage_select_sound)

        self.stage_label.color = WHITE

        # Blue circle properties (will be shown next to the selected option)
        self.blue_circle_radius = 10
        self.blue_circle_color = BLUE
        selected_label = self.get_selected_label()
        self.blue_circle_x = selected_label.x - selected_label.content_width / 2 - self.blue_circle_radius - 10
        self.blue_circle_y = selected_label.y + 12

        # Load and display highscores for the selected stage (first one by default)
        self.update_stage_selection(0)

    # Method to retrieve scores from the DB for a given stage
    def load_highscores_from_db(self, stage):
        # Load highscores from the database for the specified stage
        return self.highscore_manager.get_highscores(stage)

    # Method for creating the different highscore labels, coloring them accordingly
    def create_score_labels(self):
        # Array to contain the different labels
        labels = []
        # Default positioning
        x_position = self.window.width // 2
        y_position = self.window.height // 2 + 20

        # Create the labels, coloring them depending on their placement
        for i in range(10):
            label_color = WHITE
            if i == 0:
                label_color = BRIGHT_YELLOW  # Bright Yellow for 1st place
            elif i == 1:
                label_color = SILVER  # Silver for 2nd place
            elif i == 2:
                label_color = BRONZE  # Bronze for 3rd place

            # Adjusted y_position to consecutively place them under each other
            label = Label("", font_size=18, x=x_position, y=y_position - i * 25, anchor_x="center", color=label_color)
            labels.append(label)

        return labels

    # Method to draw all the different labels on screen, as well as the preview image
    def draw(self):
        self.highscores_label.draw()
        self.back_label.draw()
        self.stage_label.draw()

        # Draw arrows when the stage label is selected
        if self.stage_label.color == WHITE:
            # Draw left arrow
            left_arrow_label = Label("◄", font_size=24, x=self.stage_label.x - 80, y=self.stage_label.y,
                                     anchor_x="center", color=BLUE)
            left_arrow_label.draw()

            # Draw right arrow
            right_arrow_label = Label("►", font_size=24, x=self.stage_label.x + 80,
                                      y=self.stage_label.y, anchor_x="center", color=BLUE)
            right_arrow_label.draw()

        # Draw blue circle only when the "Back" label is selected
        if self.back_label.color == WHITE:
            blue_circle = Circle(self.blue_circle_x, self.blue_circle_y, self.blue_circle_radius,
                                 color=self.blue_circle_color)
            blue_circle.draw()

        self.stage_label.draw()

        # Draw stage preview image
        self.stage_preview.draw()
        for label in self.score_labels:
            label.draw()

    # Method to handle user input in this menu
    def handle_key_press(self, symbol):
        # Confirm the user's choice (will only work when the "Back" label is selected)
        if symbol == key.ENTER:
            if self.back_label.color == WHITE:
                self.window.current_menu = self.window.main_menu
                self.get_menu_select_player().play()
            elif self.stage_label.color == WHITE:
                pass
        # Move the selection upwards or downwards
        elif symbol == key.UP or symbol == key.DOWN:
            self.toggle_selection()
            self.get_menu_click_player().play()
        # Move the selection high or left (will only work when the "Stage" label is selected)
        elif symbol == key.LEFT or symbol == key.RIGHT:
            if self.stage_label.color == WHITE:
                self.update_stage_selection(1 if symbol == key.RIGHT else -1)
                self.get_stage_select_player().play()

    # Method to change the selected option by switching the label colors between "Stage" and "Back"
    def toggle_selection(self):
        # Existing code in toggle_selection method
        if self.back_label.color == WHITE:
            self.back_label.color = YELLOW
            self.stage_label.color = WHITE
        else:
            self.back_label.color = WHITE
            self.stage_label.color = YELLOW

        # Update the position of the blue circle next to the selected option
        self.update_blue_circle_position()

    # Method to, similarly to the previous toggle_selection method, change the selected stage
    def update_stage_selection(self, direction):
        # Update the selected stage based on the arrow key direction received
        # Calculating the module with the length of the stages array (3) ensures the result stays within the 3 values
        self.selected_stage = (self.selected_stage + direction - 1) % len(self.stages) + 1

        # Update the color of labels based on selection
        # The format method substitutes the curly braces in the string with the passed value
        self.stage_label.text = "Stage: {}".format(self.selected_stage)
        # Traverse the score labels setting the default text as well as colors
        for i, label in enumerate(self.score_labels):
            label.text = f"{i + 1}. ---"
            label_color = WHITE
            if i == 0:
                label_color = BRIGHT_YELLOW  # Bright Yellow for 1st place
            elif i == 1:
                label_color = SILVER  # Silver for 2nd place
            elif i == 2:
                label_color = BRONZE  # Bronze for 3rd place
            label.color = label_color

        # Update the stage preview image
        stage_preview = ImageLoad.stage_previews[self.selected_stage - 1]
        self.stage_preview.image = stage_preview

        # Load and display highscores for the updated selected stage
        self.highscores[self.selected_stage] = self.load_highscores_from_db(self.selected_stage)

        # Call display_highscores to update the displayed scores
        self.display_highscores()

        # Update the position of the blue circle next to the selected option
        self.update_blue_circle_position()

    # Update the position of the blue circle next to the selected option
    def update_blue_circle_position(self):

        if self.back_label.color == WHITE:
            selected_label = self.back_label
        else:
            selected_label = self.stage_label

        self.blue_circle_x = selected_label.x - selected_label.content_width / 2 - self.blue_circle_radius - 10
        self.blue_circle_y = selected_label.y + 12

    # Method to get the currently selected label by checking the colors
    def get_selected_label(self):
        return self.back_label if self.back_label.color == WHITE else self.stage_label

    # Method to update
    def display_highscores(self):
        # Display highscores for the selected stage
        # The notation [:10] makes it extract the top 10 scores from the list
        for i, (player_name, score) in enumerate(self.highscores[self.selected_stage][:10]):
            self.score_labels[i].text = f"{i + 1}. {player_name}: {score}"

    # Method to re-initialize the menu click sound player
    def get_menu_click_player(self):
        self.menu_click_player = Player()
        self.menu_click_player.queue(AudioLoad.menu_click_sound)
        self.menu_click_player.seek(0)
        return self.menu_click_player

    # Method to re-initialize the menu select sound player
    def get_menu_select_player(self):
        self.menu_select_player = Player()
        self.menu_select_player.queue(AudioLoad.menu_select_sound)
        self.menu_select_player.seek(0)
        return self.menu_select_player

    # Method to re-initialize the stage select sound player
    def get_stage_select_player(self):
        self.stage_select_player = Player()
        self.stage_select_player.queue(AudioLoad.menu_select_sound)
        self.stage_select_player.seek(0)
        return self.stage_select_player
