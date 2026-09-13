export function makeId() {
  // Good enough for a personal offline app; avoids extra deps.
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

