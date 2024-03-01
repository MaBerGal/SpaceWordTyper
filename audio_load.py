from pyglet.media import load


# Class that handles loading the audio from different resources
class AudioLoad:
    # Variables to store the loaded audio resources
    menu_bgm = None
    menu_click_sound = None
    menu_select_sound = None
    # Flag to track whether menu sounds are loaded or not
    menu_sounds_loaded = False

    stage_select_sound = None
    stage1_bgm = None
    stage2_bgm = None
    stage3_bgm = None
    # Flag to track whether stage sounds are loaded or not
    stage_sounds_loaded = False

    # Class method to load menu sounds (class methods can be called without instantiating the class)
    @classmethod
    def load_menu_sounds(cls):
        # Check if menu sounds are not loaded yet
        if not cls.menu_sounds_loaded:
            # Load menu background music and sounds
            cls.menu_bgm = load('media/menu_bgm.mp3', streaming=False)
            cls.menu_click_sound = load('media/menu_click.wav', streaming=False)
            cls.menu_select_sound = load('media/menu_select.wav', streaming=False)
            cls.stage_select_sound = load('media/stage_select.wav', streaming=False)
            # Set the flag to True indicating that menu sounds are loaded
            cls.menu_sounds_loaded = True

    # Class method to load stage sounds
    @classmethod
    def load_stage_sounds(cls):
        # Check if stage sounds are not loaded yet
        if not cls.stage_sounds_loaded:
            # Load stage background music
            cls.stage1_bgm = load('media/stage1_bgm.mp3', streaming=False)
            cls.stage2_bgm = load('media/stage2_bgm.mp3', streaming=False)
            cls.stage3_bgm = load('media/stage3_bgm.mp3', streaming=False)
            # Set the flag to True indicating that stage sounds are loaded
            cls.stage_sounds_loaded = True
