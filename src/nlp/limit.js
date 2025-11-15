// limit.js
export function detectLimit(text) {
  const lower = text.toLowerCase();

  const topMatch = lower.match(/топ[- ]?(\d+)|top[- ]?(\d+)/);
  if (topMatch) {
    const num = parseInt(topMatch[1] || topMatch[2], 10);
    if (!isNaN(num)) return num;
  }

  const firstMatch = lower.match(/первые\s+(\d+)/);
  if (firstMatch) {
    const num = parseInt(firstMatch[1], 10);
    if (!isNaN(num)) return num;
  }

  const lastMatch = lower.match(/последние\s+(\d+)/);
  if (lastMatch) {
    const num = parseInt(lastMatch[1], 10);
    if (!isNaN(num)) return num;
  }

  return null;
}
