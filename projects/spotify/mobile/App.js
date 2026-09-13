import { useEffect, useMemo, useRef, useState } from "react";
import { StatusBar } from "expo-status-bar";
import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from "expo-av";
import { Alert, FlatList, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { pickAndImportSongs } from "./src/lib/fileImport";
import { loadLibraryState, saveLibraryState } from "./src/lib/libraryStorage";
import { makeId } from "./src/lib/ids";

const colors = {
  bg: "#090909",
  panel: "#121212",
  panelSoft: "#1d1d1d",
  stroke: "#2a2a2a",
  text: "#ffffff",
  dim: "#b3b3b3",
  accent: "#1ed760",
  danger: "#ef4444",
};

const parseSpotifyPlaylistId = (raw) => {
  const input = (raw || "").trim();
  if (!input) return null;
  const match = input.match(/playlist\/([a-zA-Z0-9]+)/);
  if (match?.[1]) return match[1];
  if (/^[a-zA-Z0-9]+$/.test(input)) return input;
  return null;
};

const formatMs = (ms) => {
  if (!Number.isFinite(ms) || ms <= 0) return "0:00";
  const seconds = Math.floor(ms / 1000);
  const min = Math.floor(seconds / 60);
  return `${min}:${String(seconds % 60).padStart(2, "0")}`;
};

function Button({ title, onPress, variant = "default", active = false }) {
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [
        styles.btn,
        variant === "primary" && styles.btnPrimary,
        variant === "danger" && styles.btnDanger,
        active && styles.btnActive,
        pressed && { opacity: 0.9 },
      ]}
    >
      <Text style={[styles.btnText, (variant === "primary" || active) && { color: "#07110b" }]}>{title}</Text>
    </Pressable>
  );
}

export default function App() {
  const [hydrated, setHydrated] = useState(false);
  const [songs, setSongs] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [queue, setQueue] = useState([]);
  const [settings, setSettings] = useState({ shuffle: false, repeat: false });
  const [search, setSearch] = useState("");
  const [view, setView] = useState({ type: "library", playlistId: null });
  const [newPlaylistName, setNewPlaylistName] = useState("");
  const [spotifyUrl, setSpotifyUrl] = useState("");
  const [spotifyToken, setSpotifyToken] = useState("");

  const soundRef = useRef(null);
  const historyRef = useRef([]);
  const [currentId, setCurrentId] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [positionMs, setPositionMs] = useState(0);
  const [durationMs, setDurationMs] = useState(0);

  const currentSong = useMemo(() => songs.find((s) => s.id === currentId) || null, [songs, currentId]);
  const currentPlaylist = useMemo(() => playlists.find((p) => p.id === view.playlistId) || null, [playlists, view.playlistId]);

  const visibleSongs = useMemo(() => {
    const base =
      view.type === "playlist" && currentPlaylist
        ? currentPlaylist.songIds.map((id) => songs.find((s) => s.id === id)).filter(Boolean)
        : songs;
    const term = search.trim().toLowerCase();
    if (!term) return base;
    return base.filter((item) => `${item.title} ${item.artist || ""}`.toLowerCase().includes(term));
  }, [songs, currentPlaylist, view.type, search]);

  useEffect(() => {
    (async () => {
      const loaded = await loadLibraryState();
      setSongs(loaded.songs);
      setPlaylists(loaded.playlists);
      setQueue(loaded.queue);
      setSettings(loaded.settings);
      setHydrated(true);
    })();
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    saveLibraryState({ songs, playlists, queue, settings }).catch(() => {});
  }, [hydrated, songs, playlists, queue, settings]);

  useEffect(() => {
    Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      staysActiveInBackground: true,
      interruptionModeIOS: InterruptionModeIOS.DuckOthers,
      interruptionModeAndroid: InterruptionModeAndroid.DuckOthers,
      shouldDuckAndroid: true,
      playThroughEarpieceAndroid: false,
    }).catch(() => {});
  }, []);

  const unloadSound = async () => {
    const sound = soundRef.current;
    soundRef.current = null;
    if (!sound) return;
    try {
      await sound.unloadAsync();
    } catch {
      // no-op
    }
  };

  const playById = async (id) => {
    const song = songs.find((s) => s.id === id);
    if (!song) return;
    if (!song.uri) {
      Alert.alert("No local file", "This item came from Spotify playlist metadata. Import the audio file to play it.");
      return;
    }

    await unloadSound();
    const { sound } = await Audio.Sound.createAsync({ uri: song.uri }, { shouldPlay: true }, (status) => {
      if (!status.isLoaded) return;
      setIsPlaying(Boolean(status.isPlaying));
      setPositionMs(status.positionMillis || 0);
      setDurationMs(status.durationMillis || 0);
      if (status.didJustFinish) playNext();
    });

    soundRef.current = sound;
    setCurrentId(id);
    historyRef.current.push(id);
    if (historyRef.current.length > 150) historyRef.current.shift();
  };

  const playNext = async () => {
    if (queue.length > 0) {
      const [next, ...rest] = queue;
      setQueue(rest);
      await playById(next);
      return;
    }

    if (!visibleSongs.length) return;
    if (!currentId) {
      await playById(visibleSongs[0].id);
      return;
    }

    if (settings.shuffle) {
      const pick = visibleSongs[Math.floor(Math.random() * visibleSongs.length)];
      await playById(pick.id);
      return;
    }

    const idx = visibleSongs.findIndex((s) => s.id === currentId);
    const next = visibleSongs[idx + 1];
    if (next) await playById(next.id);
    else if (settings.repeat) await playById(visibleSongs[0].id);
  };

  const playPrev = async () => {
    if (historyRef.current.length < 2) return;
    historyRef.current.pop();
    const previous = historyRef.current.pop();
    if (previous) await playById(previous);
  };

  const togglePlayPause = async () => {
    if (!currentId && visibleSongs[0]) {
      await playById(visibleSongs[0].id);
      return;
    }
    const sound = soundRef.current;
    if (!sound) return;
    const status = await sound.getStatusAsync();
    if (!status.isLoaded) return;
    if (status.isPlaying) await sound.pauseAsync();
    else await sound.playAsync();
  };

  const importSongs = async () => {
    try {
      const imported = await pickAndImportSongs();
      if (!imported.length) return;
      const normalized = imported.map((item) => ({ ...item, source: "local", artist: "Local file" }));
      setSongs((prev) => [...normalized, ...prev]);
      Alert.alert("Imported", `Added ${normalized.length} local songs.`);
    } catch (e) {
      Alert.alert("Import failed", String(e?.message || e));
    }
  };

  const importSpotifyPlaylistMetadata = async () => {
    const playlistId = parseSpotifyPlaylistId(spotifyUrl);
    if (!playlistId) {
      Alert.alert("Invalid playlist", "Paste a valid Spotify playlist URL or ID.");
      return;
    }
    if (!spotifyToken.trim()) {
      Alert.alert("Access token required", "Paste a Spotify user access token to read playlist metadata.");
      return;
    }

    try {
      const res = await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks?limit=100`, {
        headers: { Authorization: `Bearer ${spotifyToken.trim()}` },
      });
      if (!res.ok) {
        const body = await res.text();
        throw new Error(`Spotify API ${res.status}: ${body.slice(0, 100)}`);
      }
      const data = await res.json();
      const tracks = (data.items || [])
        .map((row) => row.track)
        .filter(Boolean)
        .map((track) => ({
          id: makeId(),
          title: track.name || "Unknown track",
          artist: track.artists?.map((a) => a.name).join(", ") || "Unknown artist",
          uri: null,
          source: "spotify",
          durationMs: track.duration_ms || null,
          addedAt: Date.now(),
        }));

      if (!tracks.length) {
        Alert.alert("No tracks found", "This playlist has no readable tracks.");
        return;
      }

      setSongs((prev) => [...tracks, ...prev]);
      Alert.alert("Imported metadata", `${tracks.length} Spotify tracks added as metadata.\nLocal audio is still needed for playback.`);
    } catch (e) {
      Alert.alert("Spotify import failed", String(e?.message || e));
    }
  };

  const createPlaylist = () => {
    const name = newPlaylistName.trim();
    if (!name) return;
    setPlaylists((prev) => [...prev, { id: makeId(), name, songIds: [] }]);
    setNewPlaylistName("");
  };

  const addToPlaylist = (songId, playlistId) => {
    setPlaylists((prev) =>
      prev.map((p) => (p.id === playlistId && !p.songIds.includes(songId) ? { ...p, songIds: [...p.songIds, songId] } : p))
    );
  };

  const removeFromPlaylist = (songId, playlistId) => {
    setPlaylists((prev) => prev.map((p) => (p.id === playlistId ? { ...p, songIds: p.songIds.filter((id) => id !== songId) } : p)));
  };

  const clearAll = () => {
    Alert.alert("Reset app", "Delete songs, playlists, and queue?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Reset",
        style: "destructive",
        onPress: async () => {
          await unloadSound();
          setSongs([]);
          setPlaylists([]);
          setQueue([]);
          setCurrentId(null);
          setSearch("");
          historyRef.current = [];
          setView({ type: "library", playlistId: null });
        },
      },
    ]);
  };

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar style="light" />
      <View style={styles.root}>
        <ScrollView contentContainerStyle={styles.scroll}>
          <View style={styles.hero}>
            <Text style={styles.heroTitle}>Your Music</Text>
            <Text style={styles.heroSub}>Clean local player + Spotify playlist metadata import</Text>
            <View style={styles.heroButtons}>
              <Button title="Import Local Songs" variant="primary" onPress={importSongs} />
              <Button title="Reset" variant="danger" onPress={clearAll} />
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Spotify Playlist Import (Metadata)</Text>
            <Text style={styles.helper}>Direct Spotify song downloads are restricted. This imports track names/artists only.</Text>
            <TextInput placeholder="Spotify playlist URL or ID" placeholderTextColor={colors.dim} value={spotifyUrl} onChangeText={setSpotifyUrl} style={styles.input} />
            <TextInput placeholder="Spotify access token (Bearer token)" placeholderTextColor={colors.dim} value={spotifyToken} onChangeText={setSpotifyToken} style={styles.input} />
            <Button title="Import Spotify Playlist Metadata" onPress={importSpotifyPlaylistMetadata} />
          </View>

          <View style={styles.card}>
            <TextInput placeholder="Search songs..." placeholderTextColor={colors.dim} value={search} onChangeText={setSearch} style={styles.input} />
            <View style={styles.tabRow}>
              <Button title="Library" active={view.type === "library"} onPress={() => setView({ type: "library", playlistId: null })} />
              <Button title={`Shuffle ${settings.shuffle ? "On" : "Off"}`} active={settings.shuffle} onPress={() => setSettings((s) => ({ ...s, shuffle: !s.shuffle }))} />
              <Button title={`Repeat ${settings.repeat ? "On" : "Off"}`} active={settings.repeat} onPress={() => setSettings((s) => ({ ...s, repeat: !s.repeat }))} />
            </View>
            <Text style={styles.helper}>{visibleSongs.length} visible tracks · queue {queue.length}</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Playlists</Text>
            <View style={styles.inlineRow}>
              <TextInput placeholder="New playlist name" placeholderTextColor={colors.dim} value={newPlaylistName} onChangeText={setNewPlaylistName} style={[styles.input, { flex: 1 }]} />
              <Button title="Create" onPress={createPlaylist} />
            </View>
            <View style={{ gap: 8 }}>
              {playlists.map((p) => (
                <View key={p.id} style={styles.playlistRow}>
                  <Pressable onPress={() => setView({ type: "playlist", playlistId: p.id })} style={{ flex: 1 }}>
                    <Text style={styles.itemTitle}>{p.name}</Text>
                    <Text style={styles.itemMeta}>{p.songIds.length} tracks</Text>
                  </Pressable>
                </View>
              ))}
              {playlists.length === 0 && <Text style={styles.helper}>No playlists yet.</Text>}
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>{view.type === "playlist" ? `Playlist: ${currentPlaylist?.name || "Unknown"}` : "Library"}</Text>
            <FlatList
              scrollEnabled={false}
              data={visibleSongs}
              keyExtractor={(item) => item.id}
              ItemSeparatorComponent={() => <View style={{ height: 8 }} />}
              renderItem={({ item }) => (
                <View style={styles.songRow}>
                  <Pressable style={{ flex: 1 }} onPress={() => playById(item.id)}>
                    <Text numberOfLines={1} style={styles.itemTitle}>{item.title}</Text>
                    <Text numberOfLines={1} style={styles.itemMeta}>
                      {item.artist || "Unknown artist"} · {item.durationMs ? formatMs(item.durationMs) : "--:--"}
                    </Text>
                  </Pressable>
                  <Text style={[styles.badge, item.source === "spotify" && styles.badgeSpotify]}>{item.source === "spotify" ? "SPOTIFY" : "LOCAL"}</Text>
                  <View style={styles.songActions}>
                    <Button title="Queue" onPress={() => setQueue((prev) => [...prev, item.id])} />
                    {view.type === "playlist" ? (
                      <Button title="Remove" variant="danger" onPress={() => removeFromPlaylist(item.id, view.playlistId)} />
                    ) : (
                      <Button
                        title="Add"
                        onPress={() => {
                          if (!playlists.length) {
                            Alert.alert("No playlists", "Create a playlist first.");
                            return;
                          }
                          Alert.alert("Add to playlist", "Select a playlist", playlists.slice(0, 6).map((p) => ({ text: p.name, onPress: () => addToPlaylist(item.id, p.id) })).concat([{ text: "Cancel", style: "cancel" }]));
                        }}
                      />
                    )}
                  </View>
                </View>
              )}
              ListEmptyComponent={<Text style={styles.helper}>No tracks yet. Import local songs first.</Text>}
            />
          </View>
        </ScrollView>

        <View style={styles.player}>
          <View style={{ flex: 1 }}>
            <Text numberOfLines={1} style={styles.nowTitle}>{currentSong?.title || "No track selected"}</Text>
            <Text style={styles.nowMeta}>{formatMs(positionMs)} / {formatMs(durationMs)}</Text>
          </View>
          <View style={styles.playerButtons}>
            <Button title="Prev" onPress={playPrev} />
            <Button title={isPlaying ? "Pause" : "Play"} variant="primary" onPress={togglePlayPause} />
            <Button title="Next" onPress={playNext} />
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg },
  root: { flex: 1, backgroundColor: colors.bg },
  scroll: { padding: 14, paddingBottom: 110, gap: 12 },
  hero: { backgroundColor: "#0f2618", borderRadius: 16, padding: 14, borderWidth: 1, borderColor: "#1f4b2f", gap: 8 },
  heroTitle: { color: colors.text, fontSize: 28, fontWeight: "800" },
  heroSub: { color: "#d5f7df", fontSize: 13 },
  heroButtons: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  card: { backgroundColor: colors.panel, borderRadius: 14, borderWidth: 1, borderColor: colors.stroke, padding: 12, gap: 10 },
  sectionTitle: { color: colors.text, fontSize: 16, fontWeight: "800" },
  helper: { color: colors.dim, fontSize: 12 },
  input: { backgroundColor: colors.panelSoft, color: colors.text, borderRadius: 12, borderWidth: 1, borderColor: colors.stroke, paddingHorizontal: 12, paddingVertical: 10 },
  tabRow: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  inlineRow: { flexDirection: "row", gap: 8, alignItems: "center" },
  playlistRow: { backgroundColor: colors.panelSoft, borderRadius: 12, padding: 10, borderWidth: 1, borderColor: colors.stroke },
  songRow: { backgroundColor: colors.panelSoft, borderRadius: 12, borderWidth: 1, borderColor: colors.stroke, padding: 10, gap: 10 },
  itemTitle: { color: colors.text, fontWeight: "700" },
  itemMeta: { color: colors.dim, fontSize: 12, marginTop: 2 },
  badge: { alignSelf: "flex-start", fontSize: 10, color: "#132014", backgroundColor: "#95f1b5", paddingHorizontal: 7, paddingVertical: 3, borderRadius: 999 },
  badgeSpotify: { backgroundColor: "#7aa7ff", color: "#0a1221" },
  songActions: { flexDirection: "row", gap: 8, flexWrap: "wrap" },
  player: { position: "absolute", left: 12, right: 12, bottom: 12, backgroundColor: "#171717", borderWidth: 1, borderColor: colors.stroke, borderRadius: 16, padding: 10, flexDirection: "row", gap: 8, alignItems: "center" },
  nowTitle: { color: colors.text, fontWeight: "800" },
  nowMeta: { color: colors.dim, fontSize: 12, marginTop: 2 },
  playerButtons: { flexDirection: "row", gap: 8 },
  btn: { backgroundColor: colors.panelSoft, borderRadius: 12, borderWidth: 1, borderColor: colors.stroke, paddingVertical: 9, paddingHorizontal: 11 },
  btnPrimary: { backgroundColor: colors.accent, borderColor: colors.accent },
  btnDanger: { borderColor: "#5a2424", backgroundColor: "#2a1414" },
  btnActive: { backgroundColor: colors.accent, borderColor: colors.accent },
  btnText: { color: colors.text, fontWeight: "700", fontSize: 12 },
});
