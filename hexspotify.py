import random
import string
from pathlib import Path
from typing import Any, MutableMapping, Optional

import hexchat
import spotipy
import toml
from spotipy.oauth2 import SpotifyOAuth

__module_name__ = "hexspotify"
__module_version__ = "0.1.0"
__module_description__ = "Emit currently played song on Spotify"

SERVER_HOST: str = "127.0.0.1"
SERVER_PORT: int = 3000

REDIRECT_URI: str = f"http://{SERVER_HOST}:{SERVER_PORT}/callback"
SCOPE: str = "user-read-currently-playing"
CACHE_FOLDER: str = "./.spotify_caches/"

CONFIG_PATH: Path = Path("~/.config/hexspotify").expanduser() / "config.toml"


def load_config() -> Optional[MutableMapping[str, str]]:
    try:
        with open(CONFIG_PATH, "r") as f:
            config = toml.load(f)
        return config
    except FileNotFoundError:
        return None


config = load_config()

assert config is not None, "You have to make a config file as per instructions."

CLIENT_ID: Optional[str] = config.get("HEXSPOTIFY_CLIENT_ID")
CLIENT_SECRET: Optional[str] = config.get("HEXSPOTIFY_CLIENT_SECRET")
USERNAME: Optional[str] = config.get("HEXSPOTIFY_USERNAME")

for value, env_var in {
    CLIENT_ID: "HEXSPOTIFY_CLIENT_ID",
    CLIENT_SECRET: "HEXSPOTIFY_CLIENT_SECRET",
    USERNAME: "HEXSPOTIFY_USERNAME",
}.items():
    assert value is not None, f"You must configure {env_var}."


def generate_state() -> str:
    return "".join(
        [
            random.choice(
                string.ascii_letters + string.digits + r"!@#$%^&*()_+,./;'\\[]<>?:\"|{}"
            )
            for _ in range(10)
        ]
    )


STATE: str = generate_state()

if not Path(CACHE_FOLDER).exists():
    Path(CACHE_FOLDER).mkdir()

client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, STATE, SCOPE, None, USERNAME
    )
)


def get_currently_played_song() -> str:
    response = client.current_user_playing_track()
    artist = response["item"]["artists"][0]["name"]
    song = response["item"]["name"]
    return f"{artist} - {song}"


def emit_now_playing(*args) -> int:
    hexchat.command(f"SAY {get_currently_played_song()}")
    return hexchat.EAT_ALL


if __name__ == "__main__":
    hexchat.hook_command(
        "spotify", emit_now_playing, help="Emit currently played song on Spotify"
    )
