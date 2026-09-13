const songInput = document.getElementById("songInput");
const clearLibraryBtn = document.getElementById("clearLibraryBtn");
const songList = document.getElementById("songList");
const searchInput = document.getElementById("searchInput");
const libraryCount = document.getElementById("libraryCount");
const viewTitle = document.getElementById("viewTitle");

const playlistList = document.getElementById("playlistList");
const newPlaylistName = document.getElementById("newPlaylistName");
const createPlaylistBtn = document.getElementById("createPlaylistBtn");

const queueList = document.getElementById("queueList");
const clearQueueBtn = document.getElementById("clearQueueBtn");

const audioPlayer = document.getElementById("audioPlayer");
const currentSongTitle = document.getElementById("currentSongTitle");
const currentSongMeta = document.getElementById("currentSongMeta");
const playPauseBtn = document.getElementById("playPauseBtn");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const shuffleBtn = document.getElementById("shuffleBtn");
const repeatBtn = document.getElementById("repeatBtn");
const seekBar = document.getElementById("seekBar");
const currentTime = document.getElementById("currentTime");
const duration = document.getElementById("duration");
const volumeBar = document.getElementById("volumeBar");

const STORAGE_KEY = "personal_music_app_state_v1";

const state = {
  songs: [],
  playlists: [],
  queue: [],
  currentSongId: null,
  currentView: { type: "library", id: null },
  shuffle: false,
  repeat: false,
  history: [],
};

function saveState() {
  const persistable = {
    songs: state.songs.map((song) => ({
      id: song.id,
      name: song.name,
      size: song.size,
      type: song.type,
      lastModified: song.lastModified,
    })),
    playlists: state.playlists,
    queue: state.queue,
    currentSongId: state.currentSongId,
    currentView: state.currentView,
    shuffle: state.shuffle,
    repeat: state.repeat,
    history: state.history,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(persistable));
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    state.playlists = parsed.playlists || [];
    state.queue = parsed.queue || [];
    state.currentSongId = parsed.currentSongId || null;
    state.currentView = parsed.currentView || { type: "library", id: null };
    state.shuffle = Boolean(parsed.shuffle);
    state.repeat = Boolean(parsed.repeat);
    state.history = parsed.history || [];
  } catch (error) {
    console.warn("Could not load saved state.", error);
  }
}

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return "0:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

function songMeta(song) {
  const mb = (song.size / (1024 * 1024)).toFixed(1);
  return `${mb} MB`;
}

function getSongById(id) {
  return state.songs.find((song) => song.id === id) || null;
}

function getVisibleSongs() {
  if (state.currentView.type === "playlist") {
    const playlist = state.playlists.find((p) => p.id === state.currentView.id);
    if (!playlist) return [];
    return playlist.songIds
      .map((songId) => getSongById(songId))
      .filter(Boolean);
  }
  return [...state.songs];
}

function filterSongs(songs) {
  const term = searchInput.value.trim().toLowerCase();
  if (!term) return songs;
  return songs.filter((song) => song.name.toLowerCase().includes(term));
}

function renderSongs() {
  const songs = filterSongs(getVisibleSongs());
  songList.innerHTML = "";

  if (!songs.length) {
    const li = document.createElement("li");
    li.textContent = "No songs found.";
    songList.appendChild(li);
    libraryCount.textContent = "0 songs";
    return;
  }

  songs.forEach((song) => {
    const li = document.createElement("li");
    const info = document.createElement("div");
    info.className = "song-info";
    info.innerHTML = `<div class="song-title">${song.name}</div><div class="song-meta">${songMeta(song)}</div>`;

    const actions = document.createElement("div");
    actions.className = "song-actions";

    const playBtn = document.createElement("button");
    playBtn.textContent = "Play";
    playBtn.onclick = () => playSong(song.id);

    const queueBtn = document.createElement("button");
    queueBtn.textContent = "Queue";
    queueBtn.onclick = () => {
      state.queue.push(song.id);
      saveState();
      renderQueue();
    };

    const addToPlaylistBtn = document.createElement("button");
    addToPlaylistBtn.textContent = "Add";
    addToPlaylistBtn.onclick = () => addSongToPlaylistPrompt(song.id);

    const removeBtn = document.createElement("button");
    removeBtn.textContent = state.currentView.type === "playlist" ? "Remove" : "Delete";
    removeBtn.onclick = () => {
      if (state.currentView.type === "playlist") {
        removeFromCurrentPlaylist(song.id);
      } else {
        deleteSong(song.id);
      }
    };

    actions.append(playBtn, queueBtn, addToPlaylistBtn, removeBtn);
    li.append(info, actions);
    songList.appendChild(li);
  });

  libraryCount.textContent = `${songs.length} songs`;
}

function renderPlaylists() {
  playlistList.innerHTML = "";

  const allLi = document.createElement("li");
  const allButton = document.createElement("button");
  allButton.textContent = "All Songs";
  allButton.className = state.currentView.type === "library" ? "active" : "";
  allButton.onclick = () => {
    state.currentView = { type: "library", id: null };
    viewTitle.textContent = "Library";
    renderSongs();
    renderPlaylists();
    saveState();
  };
  allLi.append(allButton);
  playlistList.appendChild(allLi);

  state.playlists.forEach((playlist) => {
    const li = document.createElement("li");
    const title = document.createElement("button");
    title.textContent = `${playlist.name} (${playlist.songIds.length})`;
    title.className =
      state.currentView.type === "playlist" && state.currentView.id === playlist.id ? "active" : "";
    title.onclick = () => {
      state.currentView = { type: "playlist", id: playlist.id };
      viewTitle.textContent = `Playlist: ${playlist.name}`;
      renderSongs();
      renderPlaylists();
      saveState();
    };

    const actions = document.createElement("div");
    actions.className = "playlist-actions";

    const renameBtn = document.createElement("button");
    renameBtn.textContent = "Rename";
    renameBtn.onclick = () => {
      const nextName = prompt("Rename playlist", playlist.name);
      if (!nextName || !nextName.trim()) return;
      playlist.name = nextName.trim();
      saveState();
      renderPlaylists();
      if (state.currentView.id === playlist.id) {
        viewTitle.textContent = `Playlist: ${playlist.name}`;
      }
    };

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => {
      state.playlists = state.playlists.filter((p) => p.id !== playlist.id);
      if (state.currentView.id === playlist.id) {
        state.currentView = { type: "library", id: null };
        viewTitle.textContent = "Library";
      }
      saveState();
      renderPlaylists();
      renderSongs();
    };

    actions.append(renameBtn, deleteBtn);
    li.append(title, actions);
    playlistList.appendChild(li);
  });
}

function renderQueue() {
  queueList.innerHTML = "";
  if (!state.queue.length) {
    const li = document.createElement("li");
    li.textContent = "Queue is empty.";
    queueList.appendChild(li);
    return;
  }
  state.queue.forEach((songId, index) => {
    const song = getSongById(songId);
    if (!song) return;
    const li = document.createElement("li");
    li.innerHTML = `<div class="song-info"><div class="song-title">${song.name}</div></div>`;
    const removeBtn = document.createElement("button");
    removeBtn.textContent = "Remove";
    removeBtn.onclick = () => {
      state.queue.splice(index, 1);
      saveState();
      renderQueue();
    };
    li.appendChild(removeBtn);
    queueList.appendChild(li);
  });
}

function deleteSong(songId) {
  const song = getSongById(songId);
  if (!song) return;
  URL.revokeObjectURL(song.url);
  state.songs = state.songs.filter((s) => s.id !== songId);
  state.playlists.forEach((playlist) => {
    playlist.songIds = playlist.songIds.filter((id) => id !== songId);
  });
  state.queue = state.queue.filter((id) => id !== songId);
  state.history = state.history.filter((id) => id !== songId);
  if (state.currentSongId === songId) {
    audioPlayer.pause();
    state.currentSongId = null;
    updateNowPlaying(null);
  }
  saveState();
  renderSongs();
  renderPlaylists();
  renderQueue();
}

function playSong(songId) {
  const song = getSongById(songId);
  if (!song) return;

  state.currentSongId = songId;
  state.history.push(songId);
  if (state.history.length > 100) state.history.shift();

  audioPlayer.src = song.url;
  audioPlayer.play();
  playPauseBtn.textContent = "⏸";
  updateNowPlaying(song);
  saveState();
}

function updateNowPlaying(song) {
  if (!song) {
    currentSongTitle.textContent = "No track selected";
    currentSongMeta.textContent = "Add songs to start listening";
    return;
  }
  currentSongTitle.textContent = song.name;
  currentSongMeta.textContent = songMeta(song);
}

function playNext() {
  if (state.queue.length) {
    const nextId = state.queue.shift();
    saveState();
    renderQueue();
    playSong(nextId);
    return;
  }

  const songs = getVisibleSongs();
  if (!songs.length) return;
  if (!state.currentSongId) {
    playSong(songs[0].id);
    return;
  }

  if (state.shuffle) {
    const random = songs[Math.floor(Math.random() * songs.length)];
    playSong(random.id);
    return;
  }

  const currentIndex = songs.findIndex((song) => song.id === state.currentSongId);
  const nextIndex = currentIndex + 1;
  if (nextIndex < songs.length) {
    playSong(songs[nextIndex].id);
  } else if (state.repeat) {
    playSong(songs[0].id);
  }
}

function playPrevious() {
  if (state.history.length < 2) return;
  state.history.pop();
  const previousId = state.history.pop();
  if (previousId) playSong(previousId);
}

function removeFromCurrentPlaylist(songId) {
  if (state.currentView.type !== "playlist") return;
  const playlist = state.playlists.find((p) => p.id === state.currentView.id);
  if (!playlist) return;
  playlist.songIds = playlist.songIds.filter((id) => id !== songId);
  saveState();
  renderSongs();
  renderPlaylists();
}

function addSongToPlaylistPrompt(songId) {
  if (!state.playlists.length) {
    alert("Create a playlist first.");
    return;
  }
  const choices = state.playlists
    .map((p, index) => `${index + 1}. ${p.name}`)
    .join("\n");
  const input = prompt(`Add to playlist:\n${choices}`);
  const index = Number(input) - 1;
  if (Number.isNaN(index) || index < 0 || index >= state.playlists.length) return;
  const playlist = state.playlists[index];
  if (!playlist.songIds.includes(songId)) {
    playlist.songIds.push(songId);
    saveState();
    renderPlaylists();
  }
}

songInput.addEventListener("change", (event) => {
  const files = Array.from(event.target.files || []);
  files.forEach((file) => {
    const id = `${file.name}-${file.size}-${file.lastModified}`;
    if (state.songs.some((song) => song.id === id)) return;
    state.songs.push({
      id,
      name: file.name.replace(/\.[^/.]+$/, ""),
      size: file.size,
      type: file.type,
      lastModified: file.lastModified,
      url: URL.createObjectURL(file),
    });
  });
  saveState();
  renderSongs();
  renderPlaylists();
  event.target.value = "";
});

createPlaylistBtn.addEventListener("click", () => {
  const name = newPlaylistName.value.trim();
  if (!name) return;
  state.playlists.push({ id: crypto.randomUUID(), name, songIds: [] });
  newPlaylistName.value = "";
  saveState();
  renderPlaylists();
});

clearLibraryBtn.addEventListener("click", () => {
  if (!confirm("Clear all songs and playlists?")) return;
  state.songs.forEach((song) => URL.revokeObjectURL(song.url));
  state.songs = [];
  state.playlists = [];
  state.queue = [];
  state.currentSongId = null;
  state.history = [];
  audioPlayer.pause();
  audioPlayer.src = "";
  updateNowPlaying(null);
  saveState();
  renderSongs();
  renderPlaylists();
  renderQueue();
});

clearQueueBtn.addEventListener("click", () => {
  state.queue = [];
  saveState();
  renderQueue();
});

searchInput.addEventListener("input", renderSongs);

playPauseBtn.addEventListener("click", () => {
  if (!state.currentSongId) {
    const first = getVisibleSongs()[0];
    if (!first) return;
    playSong(first.id);
    return;
  }
  if (audioPlayer.paused) {
    audioPlayer.play();
    playPauseBtn.textContent = "⏸";
  } else {
    audioPlayer.pause();
    playPauseBtn.textContent = "▶";
  }
});

nextBtn.addEventListener("click", playNext);
prevBtn.addEventListener("click", playPrevious);

shuffleBtn.addEventListener("click", () => {
  state.shuffle = !state.shuffle;
  shuffleBtn.textContent = `Shuffle: ${state.shuffle ? "On" : "Off"}`;
  shuffleBtn.classList.toggle("active", state.shuffle);
  saveState();
});

repeatBtn.addEventListener("click", () => {
  state.repeat = !state.repeat;
  repeatBtn.textContent = `Repeat: ${state.repeat ? "On" : "Off"}`;
  repeatBtn.classList.toggle("active", state.repeat);
  saveState();
});

volumeBar.addEventListener("input", () => {
  audioPlayer.volume = Number(volumeBar.value);
});

audioPlayer.addEventListener("timeupdate", () => {
  const progress = audioPlayer.duration
    ? (audioPlayer.currentTime / audioPlayer.duration) * 100
    : 0;
  seekBar.value = progress;
  currentTime.textContent = formatTime(audioPlayer.currentTime);
  duration.textContent = formatTime(audioPlayer.duration);
});

seekBar.addEventListener("input", () => {
  if (!audioPlayer.duration) return;
  const nextTime = (Number(seekBar.value) / 100) * audioPlayer.duration;
  audioPlayer.currentTime = nextTime;
});

audioPlayer.addEventListener("ended", () => {
  if (state.repeat) {
    audioPlayer.currentTime = 0;
    audioPlayer.play();
  } else {
    playNext();
  }
});

audioPlayer.addEventListener("play", () => {
  playPauseBtn.textContent = "⏸";
});

audioPlayer.addEventListener("pause", () => {
  playPauseBtn.textContent = "▶";
});

function bootstrap() {
  loadState();
  shuffleBtn.textContent = `Shuffle: ${state.shuffle ? "On" : "Off"}`;
  shuffleBtn.classList.toggle("active", state.shuffle);
  repeatBtn.textContent = `Repeat: ${state.repeat ? "On" : "Off"}`;
  repeatBtn.classList.toggle("active", state.repeat);
  audioPlayer.volume = Number(volumeBar.value);

  // Rehydrate songs metadata only. For security reasons, browsers do not allow
  // auto-restoring file access after refresh; user must re-select local files.
  if (state.currentSongId) state.currentSongId = null;
  state.songs = [];
  renderSongs();
  renderPlaylists();
  renderQueue();
}

bootstrap();
