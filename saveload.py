from base64 import b64encode, b64decode
import game
import zlib

def save(game_state, file):
    all_data = b64encode(zlib.compress(game_state.to_json()))
    with open(file) as f:
        f.write(all_data)

def load(file):
    with open(file, 'r') as f:
        return game_state.from_json(zlib.decompress(b64.decode(f.read())))
