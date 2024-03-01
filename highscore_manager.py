import sqlite3


# Class for handling DB operations
class HighscoreManager:
    def __init__(self, db_file):
        # Connect to a SQLite3 file saved within the project
        self.connection = sqlite3.connect(db_file)
        # Create a cursor from the connection to execute queries and statements
        self.cursor = self.connection.cursor()
        # Start off by calling the following method to create a table if it doesn't yet exist
        self.create_highscores_table()

    # Method to create the highscores table if it doesn't exist yet
    def create_highscores_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS highscores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stage INTEGER,
                player_name TEXT,
                score INTEGER
            )
        ''')
        self.connection.commit()

    # Method to save a new highscore into the table
    def save_highscore(self, stage, player_name, score):
        self.cursor.execute('''
            INSERT INTO highscores (stage, player_name, score)
            VALUES (?, ?, ?)
        ''', (stage, player_name, score))
        self.connection.commit()

    # Method to retrieve highscores from a certain stage, limited to 10 and ordered in descending order
    def get_highscores(self, stage):
        self.cursor.execute('''
            SELECT player_name, score
            FROM highscores
            WHERE stage = ?
            ORDER BY score DESC
            LIMIT 10
        ''', (stage,))
        return self.cursor.fetchall()

    # Close the connection on object deletion
    def __del__(self):
        self.connection.close()