const tones = [
  ['#d9cbb8', '#c4b49a', '#8a8f73'],
  ['#e6d8c8', '#c9b8a4', '#6f6a5d'],
  ['#efe4d4', '#b7aa93', '#7d6b58'],
  ['#e4ddcf', '#a8ad8e', '#5c574e'],
  ['#f0e6d8', '#c2b09a', '#6b705c'],
] as const

export function coverTone(seed: string) {
  let hash = 0
  for (const char of seed) hash = (hash + char.charCodeAt(0) * 17) % tones.length
  return tones[hash]
}
