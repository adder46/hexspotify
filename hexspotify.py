import pathlib
import random
import string

import hexchat
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import toml


__module_name__ = "hexspotify"
__module_version__ = "0.1.0"
__module_description__ = "Emit currently played song on Spotify"

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3000

REDIRECT_URI = f'http://{SERVER_HOST}:{SERVER_PORT}/callback'
SCOPE = 'user-read-currently-playing'
CACHE_FOLDER = './.spotify_caches/'

CONFIG_PATH = pathlib.Path("~/.config/hexspotify").expanduser() / "config.toml"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = toml.load(f)
        return config
    except FileNotFoundError:
        return None

config = load_config()

assert (config is not None), "You have to make a config file as per instructions"

CLIENT_ID = config.get("HEXSPOTIFY_CLIENT_ID")
CLIENT_SECRET = config.get("HEXSPOTIFY_CLIENT_SECRET")
USERNAME = config.get("HEXSPOTIFY_USERNAME")

def generate_state():
    return "".join([
        random.choice(
            string.ascii_letters
            + string.digits
            + r"!@#$%^&*()_+,./;'\\[]<>?:\"|{}"
        )
        for _ in range(10)
    ])


STATE = generate_state()

if not pathlib.Path(CACHE_FOLDER).exists():
    pathlib.Path(CACHE_FOLDER).mkdir()

client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI,
        STATE,
        SCOPE,
        None,
        USERNAME       
    )
)


def get_currently_played_song():
    response = client.current_user_playing_track()
    artist = response['item']['artists'][0]['name']
    song = response['item']['name']
    return f"{artist} - {song}"


def emit_now_playing(*args):
    hexchat.command(f'SAY {get_currently_played_song()}')
    return hexchat.EAT_ALL


if __name__ == '__main__':
    hexchat.hook_command(
        'spotify',
        emit_now_playing,
        help='Emit currently played song on Spotify'
    )
