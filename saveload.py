from base64 import b64encode, b64decode
import game
import json
import zlib

def save_settings(term):
    save({
        'font': term.get_font()['family'],
        'font_size': term.get_font_size()
    }, 'salmon.cfg')

def load_settings(term):
    data = load('salmon.cfg')
    term.set_font(data['font'], data['font_size'])

def save(data, file):
    # all_data = b64encode(zlib.compress(json.dumps(data).encode('utf-8')))
    all_data = json.dumps(data)
    with open(file, 'w') as f:
        # f.write(all_data.decode('utf-8'))
        f.write(all_data)

def load(file):
    with open(file) as f:
        # return json.loads(zlib.decompress(b64.decode(f.read())))
        return json.loads(f.read())
