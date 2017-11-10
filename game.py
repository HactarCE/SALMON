import json


class GameState(object):

    def to_json(self):
        saved_data = {}
        # pack saved data into dictionary
        return JSONEncoder().encode(saved_data)

    @staticmethod
    def from_json(text):
        saved_data = JSONDecoder().decode(text)
        game_state = GameState()
        # unpack saved data from dictionary
        return game_state
