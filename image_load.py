
from pyglet.resource import image


# Class to handle image asset loading
class ImageLoad:
    # Array to store the different stage background images
    stage_images = []
    # Array to store the different stage background previews
    stage_previews = []
    # Class-level flag to track whether resources are loaded or not
    loaded = False

    # Class method to load the images in case they're not loaded already
    @classmethod
    def load_images(cls):
        if not cls.loaded:
            cls.stage_images = [image("images/stage1.jpg"), image("images/stage2.gif"), image("images/stage3.gif")]
            cls.stage_previews = [image("images/preview1.png"), image("images/preview2.png"), image("images/preview3.png")]
            cls.loaded = True