# hexspotify

**hexspotify** is a hexchat plugin that emits currently played song on Spotify to the current hexchat window.

# Installation

Just grab `hexspotify.py` and put it in the hexchat's addons folder. Make a directory in `.config` folder called `hexspotify`, and place a `config.toml` file containing your client ID, client secret, and your Spotify username inside.

Here's an example config:

```toml
HEXSPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID"
HEXSPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
HEXSPOTIFY_USERNAME = "YOUR_USERNAME"
```

The client ID and the secret can be obtained when you register your app with Spotify.

## Usage

```
/spotify
```