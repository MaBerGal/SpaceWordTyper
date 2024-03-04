from pyglet import clock
from pyglet.app import run

from game_window import GameWindow
from word_manager import WordManager

# Entry point to the program
if __name__ == "__main__":
    wordManager = WordManager(1)
    mainWindow = GameWindow(wordManager, 1)
    clock.schedule(mainWindow.on_update)
    run()
