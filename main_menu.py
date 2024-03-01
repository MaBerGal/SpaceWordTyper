from pyglet.media import Player
from pyglet.window import key
from pyglet.text import Label
from pyglet.shapes import Circle
from audio_load import AudioLoad


# Class that shows the main menu and handles logic related to navigating it
class MainMenu:
    def __init__(self, window):
        # Reference to the main window
        self.window = window

        # Create labels for menu options
        self.labels = [
            Label("Start", font_size=24, x=window.width // 2, y=window.height // 2 + 50, anchor_x="center",
                  color=(255, 199, 95, 255)),
            Label("Highscore", font_size=24, x=window.width // 2, y=window.height // 2, anchor_x="center",
                  color=(255, 199, 95, 255)),
            Label("Exit", font_size=24, x=window.width // 2, y=window.height // 2 - 50, anchor_x="center",
                  color=(255, 199, 95, 255))
        ]

        # Initialize the selected menu option
        self.selected_option = 0

        # Blue circle properties (will be shown next to the selected option)
        self.circle_radius = 10
        self.circle_color = (0, 0, 255, 255)
        self.circle_x = self.labels[self.selected_option].x - 30
        self.circle_y = self.labels[self.selected_option].y

        # Call the update_selection method to highlight an initial option and also draw the blue circle
        self.update_selection(0)

        # Load the menu sounds
        AudioLoad.load_menu_sounds()
        # Create players for the sounds
        self.menu_click_player = Player()
        self.menu_click_player.queue(AudioLoad.menu_click_sound)

        self.menu_select_player = Player()
        self.menu_select_player.queue(AudioLoad.menu_select_sound)

        # Create a player for the BGM
        self.menu_bgm_player = Player()
        self.menu_bgm_player.queue(AudioLoad.menu_bgm)
        # Make it loop
        self.menu_bgm_player.loop = True
        # Call the play_menu_bgm method to make the BGM player start playing
        self.play_menu_bgm()

    # Method to re-initialize the click sound player in order to re-use it multiple times
    def get_menu_click_player(self):
        # Create and return a new menu click sound player instance
        self.menu_click_player = Player()
        self.menu_click_player.queue(AudioLoad.menu_click_sound)
        self.menu_click_player.seek(0)
        return self.menu_click_player

    # Method to re-initialize the selection sound player in order to re-use it multiple times
    def get_menu_select_player(self):
        # Create and return a new menu select sound player instance
        self.menu_select_player = Player()
        self.menu_select_player.queue(AudioLoad.menu_select_sound)
        self.menu_select_player.seek(0)
        return self.menu_select_player

    # Method to make the BGM player start playing (useful for being called from the GameWindow class)
    def play_menu_bgm(self):
        # Play the menu background music
        self.menu_bgm_player.play()

    # Method to make the BGM player stop playing (useful for being called from the GameWindow class)
    def stop_menu_bgm(self):
        # Pause the menu background music
        self.menu_bgm_player.pause()

    # Method to draw the option labels and the blue circle next to the selected one
    def draw(self):
        # Draw menu option labels
        for label in self.labels:
            label.draw()

        # Draw blue circle next to the selected option
        blue_circle = Circle(self.circle_x, self.circle_y, self.circle_radius, color=self.circle_color)
        blue_circle.draw()

    # Method to handle player input on the main menu
    def handle_key_press(self, symbol):
        # Confirms the highlighted selection
        if symbol == key.ENTER:
            # Show the stage select menu
            if self.selected_option == 0:
                self.window.current_menu = self.window.stage_select_menu
                self.get_menu_select_player().play()
            # Show the highscore menu
            elif self.selected_option == 1:
                self.window.current_menu = self.window.highscore_menu
                self.get_menu_select_player().play()
            # Exit the program
            elif self.selected_option == 2:
                self.window.close()
        # Update selection (move up)
        elif symbol == key.UP:
            self.update_selection(-1)
            self.get_menu_click_player().play()
        # Update selection (move down)
        elif symbol == key.DOWN:
            self.update_selection(1)
            self.get_menu_click_player().play()

    # Method to update the selected label depending on the player's input
    def update_selection(self, direction):
        # Update the selected menu option and its appearance
        self.selected_option = (self.selected_option + direction) % len(self.labels)

        # Update the color of labels based on selection
        # The enumerate object produces tuples from data structures containing an index and their associated value
        # With that, we can check if the index corresponds with the selected option and then modify the label's color
        for i, label in enumerate(self.labels):
            # White for the selected option
            if i == self.selected_option:
                label.color = (255, 255, 255, 255)
            # Yellow for the rest
            else:
                label.color = (255, 199, 95, 255)

        # Update the position of the blue circle next to the selected option
        selected_label = self.labels[self.selected_option]
        self.circle_x = selected_label.x - selected_label.content_width / 2 - self.circle_radius - 10
        self.circle_y = selected_label.y + 12
