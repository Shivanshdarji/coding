# Personal Music App (Mobile)

This is a private, offline, Spotify-style music player you can install on your own devices.

## Features

- Import local audio files (copies into the app so it works offline)
- Library + search
- Playlists
- Queue
- Shuffle / Repeat
- Spotify playlist import (metadata only: track + artist list)
- Background audio (best-effort, depends on OS settings)

## Run on any phone (no publishing)

### 1) Install Expo Go

- On Android: install **Expo Go** from Play Store
- On iPhone: install **Expo Go** from App Store

### 2) Start the app on your PC

From this folder:

```bash
cd mobile
npm run start
```

This opens the Expo dev server and shows a QR code.

### 3) Open it on your device

- Android: scan the QR code inside Expo Go
- iPhone: scan with Camera app, open in Expo Go

## Build a downloadable APK (Android)

If you want a real installable file (APK) for your own phone:

1. Install EAS CLI:

```bash
npm i -g eas-cli
```

2. Login and build:

```bash
cd mobile
eas login
eas build -p android --profile preview
```

EAS will give you a direct APK download link.

## Spotify playlist import note

- You can import playlist metadata (song names/artists) using Spotify Web API token.
- Directly downloading Spotify audio is restricted by Spotify terms and copyright rules.
- To actually play tracks in this app, import local audio files.

## Notes / limitations

- iOS installable builds (IPA) typically require an Apple Developer setup or TestFlight.
- Import uses the system file picker; you may need to grant storage permissions.

