import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "personal_music_mobile_v1";

export async function loadLibraryState() {
  const raw = await AsyncStorage.getItem(KEY);
  if (!raw) {
    return { songs: [], playlists: [], queue: [], settings: { shuffle: false, repeat: false } };
  }
  try {
    const parsed = JSON.parse(raw);
    return {
      songs: Array.isArray(parsed.songs) ? parsed.songs : [],
      playlists: Array.isArray(parsed.playlists) ? parsed.playlists : [],
      queue: Array.isArray(parsed.queue) ? parsed.queue : [],
      settings: {
        shuffle: Boolean(parsed.settings?.shuffle),
        repeat: Boolean(parsed.settings?.repeat),
      },
    };
  } catch {
    return { songs: [], playlists: [], queue: [], settings: { shuffle: false, repeat: false } };
  }
}

export async function saveLibraryState(next) {
  await AsyncStorage.setItem(KEY, JSON.stringify(next));
}

