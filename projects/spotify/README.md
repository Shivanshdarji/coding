# Personal Music App (Offline, Local)

A private Spotify-style music app for your own computer.

## What it does

- Plays local audio files (`mp3`, `wav`, `m4a`, etc.)
- Library with search
- Queue management
- Custom playlists
- Shuffle / Repeat
- Seek + volume controls
- Saves playlists and app state to browser local storage

## Important note

For privacy/security, browsers do **not** let websites keep permanent access to local music files after refresh.  
So after reopening the app, you need to click **Add Songs** and choose files again.

Your playlists and settings are still remembered.

## Run it

### Option 1 (simplest)

Open `index.html` directly in your browser.

### Option 2 (recommended local server)

If you have Python:

```bash
python -m http.server 5500
```

Then open:

[http://localhost:5500](http://localhost:5500)
