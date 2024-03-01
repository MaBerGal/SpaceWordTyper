import pyglet
import random
import math
import os

from pyglet.media import Player
from pyglet.window import Window, key
from pyglet.text import Label
from pyglet.shapes import Line, Rectangle, Star, Circle
from pyglet.resource import image

from audio_load import AudioLoad
from highscore_manager import HighscoreManager
from highscore_menu import HighscoreMenu
from image_load import ImageLoad
from main_menu import MainMenu
from particles import Particles
from stage_select_menu import StageSelectMenu


# Class that handles the main game window and rendering
class GameWindow(Window):
    def __init__(self, game, stage):
        # Call to the super constructor (window), setting the dimensions and title
        super().__init__(width=800, height=600, caption="Typing Game")
        # Initialize the game renderer window (instance of WordManager)
        self.game = game
        # Initialize the main menu
        self.main_menu = MainMenu(self)
        # Initialize the stage select menu
        self.stage_select_menu = StageSelectMenu(self)
        # Initialize the highscore menu
        self.highscore_menu = HighscoreMenu(self)
        # Set the initial menu to the main menu
        self.current_menu = self.main_menu
        # Flag to track if the game is currently in progress
        self.in_game = False
        # Flag to track if the game is currently paused
        self.paused = False
        # Flag to check if the background image is loaded
        self.background_loaded = False

        # Initialize the HighscoreManager to handle highscores
        self.highscore_manager = HighscoreManager('highscores.db')

        # Load the stage-specific background music player
        AudioLoad.load_stage_sounds()
        self.stage_bgm_player = Player()

        # Current stage of the game
        self.stage = stage
        # Initial speed of the words falling
        self.word_speed = 100

        # First pause label
        self.pause_label = Label("Pause", font_size=36, x=self.width // 2, y=self.height // 2,
                                 anchor_x="center", anchor_y="center", color=(255, 0, 0, 255))

        # Second pause label
        self.resume_label = Label("Press Esc to resume or Enter to return to main menu", font_size=12, x=self.width // 2,
                             y=self.height // 2 - 50,
                             anchor_x="center", anchor_y="center", color=(255, 255, 255, 255))

        # Player's score
        self.score = 0

        # Load health images for displaying player's health
        self.health_image = image('images/health.png')
        self.health_images = []
        health_width = 25
        health_height = 25
        # Create sprites from the images, and then fill an array with them
        for i in range(3):
            health_sprite = pyglet.sprite.Sprite(self.health_image,
                                                 x=(self.width - health_width * (i + 1)) // 2 + health_width * i,
                                                 y=self.height - health_height - 20)
            self.health_images.append(health_sprite)

        # Initialize the limitLine line (makes words disappear when they reach it and the player lose one health unit)
        self.limitLine_x = self.width / 5
        self.limitLine = Line(self.limitLine_x, 0, self.limitLine_x, self.height, width=4, color=(214, 93, 177, 255))

        # Time for shake animation when a word character is missed
        self.shake_animation_time = 0.0

        # Initialize time for the limitLine's pulsating effect
        self.pulsate_time = 0.0

        # Background dust
        self.dust = None

    # Method to update the current stage, both in this class and the game (WordManager instance)
    def update_stage(self, stage):
        self.stage = stage
        self.game.update_stage(stage)
        # Call the initialize_dust method to set up the dust array
        self.initialize_dust()

    # Draw the contents of the window
    def on_draw(self):
        # Clear the window
        self.clear()

        # Check the current menu and draw accordingly
        if self.current_menu == self.main_menu and not self.in_game:
            self.main_menu.draw()
        elif self.current_menu == self.highscore_menu and not self.in_game:
            self.highscore_menu.draw()
        elif self.current_menu == self.stage_select_menu and not self.in_game:
            self.stage_select_menu.draw()
        elif self.in_game:
            if self.is_game_over():
                self.draw_game_over()
            else:
                self.load_background()
                self.draw_game()
                if self.paused:
                    self.pause_label.draw()
                    self.resume_label.draw()

    # Method to draw the background based on the stage
    def load_background(self):
        if self.stage == 1 or self.stage == 2 or self.stage == 3:
            # Check whether the images have not been loaded yet - load them if so
            if not ImageLoad.loaded:
                ImageLoad.load_images()

            # Create a sprite with the background image, make it fit the window and draw it
            stage_background = pyglet.sprite.Sprite(ImageLoad.stage_images[self.stage - 1])
            stage_background.scale_x = self.width / stage_background.width
            stage_background.scale_y = self.height / stage_background.height
            stage_background.draw()
        # Don't load an image if it's stage 1
        else:
            pass

    def draw_game(self):
        # Load the background if not yet loaded
        if not self.background_loaded:
            self.load_background()
            self.background_loaded = True

        # Draw the limit line
        self.limitLine.draw()

        # Draw the dust, characters, and hit particles
        for dust_particle in self.dust:
            dust_particle.draw()

        for character in self.characters:
            character.draw()

        for particle in self.particles:
            particle.draw()

        # Draw the player's score
        score_label = Label(f"Score: {self.score}", font_size=18, x=10, y=self.height - 40,
                            anchor_x="left", color=(255, 255, 255, 255))
        score_label.draw()

        # Draw the player's remaining health
        for health_sprite in self.health_images:
            health_sprite.draw()


        pause_label = Label("Esc → Pause", font_size=14, x=self.width - 10, y=self.height - 15,
                            anchor_x="right",
                            anchor_y="top", color=(210, 255, 80, 255))
        pause_label.draw()

    # Method to draw the game over screen
    def draw_game_over(self):
        # Draw the game over labels
        game_over_label = Label("GAME OVER", font_size=48, x=self.width // 2, y=self.height // 2,
                                anchor_x="center", anchor_y="center", color=(255, 0, 0, 255))
        game_over_label.draw()

        retry_label = Label("Press R to retry", font_size=24, x=self.width // 2, y=self.height // 2 - 50,
                            anchor_x="center", anchor_y="center", color=(255, 255, 255, 255))
        retry_label.draw()

        main_menu_label = Label("Press Esc to return to the main menu", font_size=24,
                                x=self.width // 2, y=self.height // 2 - 100, anchor_x="center", anchor_y="center",
                                color=(255, 255, 255, 255))
        main_menu_label.draw()

    # Method to update the game state during each frame
    def on_update(self, elapsed_time):
        # Check if the game is in progress and not paused
        if self.in_game and not self.paused:
            # Adjust the word speed multiplier based on the current stage
            self.word_speed_multiplier = 1.0
            if self.stage == 2:
                self.word_speed_multiplier = 2.0
            elif self.stage == 3:
                self.word_speed_multiplier = 3.0

            # Update time for pulsating effect
            self.pulsate_time += elapsed_time

            # Modulate the limitLine's color alpha channel using a sine function for the pulsating effect
            alpha_multiplier = 0.5 + 0.5 * math.sin(self.pulsate_time * 5)
            limitLine_color = (238, 75, 43, int(255 * alpha_multiplier))
            self.limitLine.color = limitLine_color

            # Move each character (word) on the screen based on the word speed and multiplier
            for particle in self.characters:
                particle.x -= self.word_speed * self.word_speed_multiplier * elapsed_time

            # Check if the first character (word) has reached the limitLine line
            if self.characters[0].x < self.limitLine_x + 12:
                # Start a new round
                self.start()
                # Remove one unit of health
                self.remove_health()

            # Update particle effects
            for particle in self.particles:
                particle.update(elapsed_time)

            # Move dust in the background to create a scrolling effect
            for dust_particle in self.dust:
                dust_particle.x += elapsed_time * 20
                # Reset dust to the left side when they go beyond the screen width
                if dust_particle.x > self.width:
                    dust_particle.x = 0

            # Handle shake animation when the player misses a word
            if self.shake_animation_time > 0:
                self.shake_animation_time -= elapsed_time
                # Apply rotation to the first character for a shaking effect
                self.characters[0].rotation = math.sin(self.shake_animation_time * 50) * 20
            # Reset rotation if shake animation time is over
            else:
                self.characters[0].rotation = 0

        # If not in-game or paused, do nothing during this update frame
        else:
            pass

    # Method to remove one unit of health
    def remove_health(self):
        if self.health_images:
            self.health_images.pop()

    # Handle key presses based on the game state and menu
    def on_key_press(self, symbol, modifiers):
        # Check if the game is currently in progress
        if self.in_game:
            # Check if the game is over
            if self.is_game_over():
                # Allow the player to restart the game by pressing R
                if symbol == key.R:
                    self.reset_game(True)
                # Allow the player to return to the main menu by pressing Esc
                elif symbol == key.ESCAPE:
                    self.return_to_main_menu()
            # Check if the game is not paused to pause it
            elif symbol == key.ESCAPE:
                self.toggle_pause()
            # Check if the game is not paused and handle key presses for gameplay
            elif not self.paused:
                self.handle_game_key_press(symbol, modifiers)
            # Check if the game is paused and the player presses Enter to return to the main menu
            elif self.paused and symbol == key.ENTER:
                self.return_to_main_menu()

        # If not in-game, handle key presses for the current menu
        else:
            self.current_menu.handle_key_press(symbol)

    # Method to toggle the game pause state
    def toggle_pause(self):
        # Switch the flag's value
        self.paused = not self.paused
        # Switch the pause label's text
        if self.paused:
            self.pause_label.text = "Pause"
        else:
            self.pause_label.text = ""

    # Method to check the game state based on the player's health
    def is_game_over(self):
        return not self.health_images

    # Method to reset the game state
    def reset_game(self, start_game):
        # Save the player's highscore
        self.save_highscore()

        # Set in_game and paused based on the specified values
        self.in_game = start_game
        self.paused = False

        # Reset the player's score to zero
        self.score = 0

        # Initialize the player's health images
        self.health_images = []
        for i in range(3):
            health_sprite = pyglet.sprite.Sprite(self.health_image,
                                                 x=(self.width - 25 * (i + 1)) // 2 + 25 * i,
                                                 y=self.height - 25 - 20)
            self.health_images.append(health_sprite)

        # Clear the characters, particles, and other game elements
        self.characters = []
        self.particles = []

        # Reset the limitLine and draw it on the screen
        self.limitLine_x = self.width / 5
        self.limitLine = Line(self.limitLine_x, 0, self.limitLine_x, self.height, width=4, color=(214, 93, 177, 255))

        # Clear and generate dust once again
        self.initialize_dust()

        # Start the game immediately if in_game is True
        if self.in_game:
            self.start()

    # Method to return to the main menu
    def return_to_main_menu(self):
        # Set the in-game and pause flags to False
        self.in_game = False
        self.paused = False

        # Set the current menu to the main menu
        self.current_menu = self.main_menu

        # Reset the game state without starting the game immediately after doing so
        self.reset_game(start_game=False)

        # Pause the stage background music player and reset it
        self.stage_bgm_player.pause()
        self.stage_bgm_player = Player()

        # Play the background music again (it picks up from where it left off)
        self.main_menu.play_menu_bgm()

    # Method to save the player's score to the highscores database
    def save_highscore(self):
        # Save the player's score to the highscores database
        self.highscore_manager.save_highscore(self.stage, os.getlogin(), self.score)

    # Method to handle key presses during gameplay
    def handle_game_key_press(self, symbol, modifiers):
        try:
            # (DEBUGGING) Print the uppercase character corresponding to the pressed key
            print(f"Game key pressed: {chr(symbol).upper()}")

            # Get the uppercase character corresponding to the pressed key
            key_char = chr(symbol).upper()

            # Check if the pressed key matches the current game word
            if self.game.verify_key(key_char):
                # Get the character label at the front of the character labels list
                character = self.characters[0]

                # Check if the game word is not empty
                if self.game.word:
                    # Remove the first character label from the characters list
                    self.characters = self.characters[1:]
                else:
                    # Start a new round and increase the score if the game word is empty
                    self.start()
                    self.score += 1

                # Add particles at the position of the removed character label
                self.particles.append(Particles(character.x, character.y))
            else:
                # Set shake animation time to create a visual shake effect
                self.shake_animation_time = 0.3

        # Handle the cases when chr() fails to convert the symbol to a character
        except ValueError:
            print("Invalid key pressed.")
        except OverflowError:
            print("Invalid key pressed.")

    # Method to handle key presses in the menus
    def handle_menu_key_press(self, symbol, modifiers):
        # Check the pressed key and perform corresponding actions in the menu
        if symbol == key.ENTER:
            # If the Enter key is pressed, inform the main menu to handle the key press
            self.main_menu.handle_key_press(key.ENTER)
            self.main_menu.get_menu_select_player().play()
        elif symbol == key.UP:
            # If the Up key is pressed, update the menu selection to the previous option
            self.main_menu.update_selection(-1)
            # Play the menu click sound
            self.main_menu.get_menu_click_player().play()
        elif symbol == key.DOWN:
            # If the Down key is pressed, update the menu selection to the next option
            self.main_menu.update_selection(1)
            self.main_menu.get_menu_click_player().play()

    # Method to start the game
    def start(self):
        # Set in_game to True to indicate that the game is now in progress
        self.in_game = True

        # Stop the menu background music
        self.main_menu.stop_menu_bgm()

        # Initialize a new round in the game
        self.game.grab_new_word()

        # Clear existing characters and particles
        self.characters = []
        self.particles = []

        # Initialize starting positions for characters
        x = self.width
        y = random.randint(self.height / 4, self.height / 4 * 3)

        # Create labels for each character in the current game word and position them
        # Create labels for each character in the current game word and position them
        for t in self.game.word:
            bright_yellow_color = (255, 255, 0, 255)  # Bright yellow color
            character_label = Label(t, font_name="Impact", font_size=30, x=x, y=y, anchor_x="center",
                                    color=bright_yellow_color)
            self.characters.append(character_label)

            # Distance between character labels
            x = x + 40

        # Check if the stage background music player is not already playing
        if not self.stage_bgm_player.playing:
            # Queue the corresponding stage BGM based on the current stage
            if self.stage == 1:
                self.stage_bgm_player.queue(AudioLoad.stage1_bgm)
            elif self.stage == 2:
                self.stage_bgm_player.queue(AudioLoad.stage2_bgm)
            elif self.stage == 3:
                self.stage_bgm_player.queue(AudioLoad.stage3_bgm)

            # Set the BGM player to loop and play the queued music
            self.stage_bgm_player.loop = True
            self.stage_bgm_player.play()

    # Generator for yielding random colors
    def color_generator(self, stage):
        if stage == 1:
            # Shades of purple
            yield (
                random.randint(100, 180),
                random.randint(50, 120),
                random.randint(150, 220),
                255
            )
        elif stage == 2:
            # Shades of blue
            yield (
                random.randint(50, 120),
                random.randint(100, 180),
                random.randint(150, 220),
                255
            )
        elif stage == 3:
            # Shades of red
            yield (
                random.randint(150, 220),
                random.randint(50, 120),
                random.randint(100, 180),
                255
            )

    # Method to create an array of dust depending on the stage
    def initialize_dust(self):
        self.dust = []
        for _ in range(20):
            dust_size = (10, 10)
            # Add some variation to the size
            size_variation = random.uniform(0.8, 1.2)
            dust_size = (int(dust_size[0] * size_variation), int(dust_size[1] * size_variation))

            # Show different types of particles depending on the stage
            if self.stage == 1:
                dust = Rectangle(
                    x=random.randint(0, self.width),
                    y=random.randint(0, self.height),
                    width=dust_size[0],
                    height=dust_size[1],
                    color=next(self.color_generator(self.stage))
                )
            elif self.stage == 2:
                dust = Circle(
                    x=random.randint(0, self.width),
                    y=random.randint(0, self.height),
                    radius=dust_size[0] // 2,
                    color=next(self.color_generator(self.stage))
                )
            elif self.stage == 3:
                dust = Star(
                    x=random.randint(0, self.width),
                    y=random.randint(0, self.height),
                    outer_radius=12,
                    inner_radius=6,
                    num_spikes=5,
                    color=next(self.color_generator(self.stage))
                )
            self.dust.append(dust)


