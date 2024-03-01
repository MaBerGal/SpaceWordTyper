import random


# Class managing words for the game
class WordManager:
    def __init__(self, stage):
        # Initialize the WordManager with the specified stage and word lists for each stage
        self.stage = stage
        self.word_lists = {
            1: ["SUN", "MOON", "STAR", "COMET", "VENUS", "ROCKET", "RAYS", "ALIENS", "MILKYWAY", "DISTANCE",
                "SKY", "EARTH", "ORBIT", "SOLAR", "LIGHT", "GALAXY", "PLUTO", "MARS", "NEBULA", "COSMOS",
                "NIGHT", "DAY", "SATELLITE", "ASTROLOGY", "SPACE", "PLANET", "UNIVERSE", "WORLD", "ASTRONOMER",
                "ZODIAC", "CIRCLE", "ALERT", "QUEST", "CHART", "SWIFT", "SPHERE", "GLOBE", "BEAM", "SAGA"],
            2: ["ASTRONOMY", "CELESTIAL", "GALACTIC", "INTERSTELLAR", "EXPLOSION", "TELESCOPE", "EXTRATERRESTRIAL",
                "COSMOLOGICAL", "ASTROPHYSICS", "INTERGALACTIC", "CONSTELLATION", "OBSERVATORY", "QUASAR", "TELEMETRY",
                "ECLIPSE", "ASTRONAUT", "ASTEROID", "ATMOSPHERE", "INTERPLANETARY",
                "TECHNOLOGY", "SENSORS", "STARGAZING", "ASTROGEOLOGY", "SUPERNOVA", "ASTEROID", "EXOPLANET",
                "COSMICDUST", "BLACKHOLE", "UNIVERSE", "GALAXIES", "EXPLORATION", "RADIATION", "METEORITE", "COSMIC",
                "COSMONAUT", "INTERCOSMIC", "TELESCOPIC", "ASTROSURVEY", "INFRARED", "SOLARFLARE", "TELEKINETIC",
                "QUASAR", "AURORA", "CELESTIALMECHANICS", "ECLIPSES", "ATMOSPHERICENTRY"],
            3: ["COSMOGONY", "PARALLAX", "ASTROBIOLOGY", "MICROGRAVITY", "SPECTROGRAPH", "MAGNETOSPHERE", "METEOROID",
                "NEBULIZATION", "TELESCOPICALLY", "RADIOTELESCOPE", "GALACTOLOGICAL", "METEOROLOGICAL",
                "MICROGRAVITATIONAL", "ASTROPHOTOGRAPHY", "SOLARSYSTEMATIC", "COSMOGRAPHER", "ASTRONAVIGATION",
                "GEOSTATIONARY", "HYPERVELOCITY", "TIMEWARPING", "ASTRONOMICAL", "GRAVITATIONALPULL", "ASTROCHEMISTRY",
                "NEBULARCLOUD", "CELESTIALBODY", "ASTROSURVEY", "INFRARED", "TELESCOPING", "ORBITALMECHANICS",
                "COSMICRAYS", "ANTIMATTER", "GRAVITYWELL", "PHOTONICALLY", "EXTRAGALACTIC", "EINSTEINIAN", "NEUTRINOS",
                "THERMONUCLEAR", "PYROPHOSPHORIC", "STELLARFORMATION"]
        }
        # Initialize with an empty word
        self.word = ""

    # Method for updating the stage for the WordManager
    def update_stage(self, stage):
        self.stage = stage

    # Method for checking if the pressed key matches the first character of the current word
    def verify_key(self, character):
        # If it matches, remove the matched character from the current word
        if character == self.word[0]:
            self.word = self.word[1:]
            # Return True if the key is correct
            return True
        # Return False if the key is incorrect
        return False

    # Method for getting a new word by randomly selecting a word from the word list corresponding to the stage
    def grab_new_word(self):
        word_list = self.word_lists.get(self.stage, [])
        self.word = random.choice(word_list)

        # Adjust the rate at which new words appear based on the stage
        if self.stage == 1:
            self.word_speed = 100
        elif self.stage == 2:
            self.word_speed = 150
        elif self.stage == 3:
            self.word_speed = 200
