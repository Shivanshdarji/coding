import * as DocumentPicker from "expo-document-picker";
import * as FileSystem from "expo-file-system";
import { makeId } from "./ids";

const MUSIC_DIR = `${FileSystem.documentDirectory}music/`;

async function ensureMusicDir() {
  const info = await FileSystem.getInfoAsync(MUSIC_DIR);
  if (!info.exists) {
    await FileSystem.makeDirectoryAsync(MUSIC_DIR, { intermediates: true });
  }
}

function sanitizeFilename(name) {
  return name.replace(/[^\w.\-() ]+/g, "_").slice(0, 120);
}

export async function pickAndImportSongs() {
  await ensureMusicDir();

  const result = await DocumentPicker.getDocumentAsync({
    type: "audio/*",
    multiple: true,
    copyToCacheDirectory: true,
  });

  if (result.canceled) return [];

  const assets = result.assets || [];
  const imported = [];

  for (const asset of assets) {
    const id = makeId();
    const displayName = asset.name ? asset.name.replace(/\.[^/.]+$/, "") : `Track ${id}`;
    const ext = asset.name?.includes(".") ? asset.name.split(".").pop() : "audio";
    const filename = `${sanitizeFilename(displayName)}-${id}.${ext}`;
    const destUri = `${MUSIC_DIR}${filename}`;

    // On both iOS/Android with Expo, copying from cache URI to app storage works.
    await FileSystem.copyAsync({ from: asset.uri, to: destUri });

    imported.push({
      id,
      title: displayName,
      uri: destUri,
      durationMs: null,
      addedAt: Date.now(),
    });
  }

  return imported;
}

