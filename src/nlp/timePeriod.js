export function detectTimePeriod(text) {
  const lower = text.toLowerCase();

  // пример: "за 2023 год"
  const yearMatch = lower.match(/за\s+(\d{4})\s*год/);
  if (yearMatch) {
    const year = yearMatch[1];
    return [`${year}-01-01`, `${year}-12-31`];
  }

  // пример: "q1 2023"
  const qMatch = lower.match(/q1\s+(\d{4})/i);
  if (qMatch) {
    const year = qMatch[1];
    return [`${year}-01-01`, `${year}-03-31`];
  }

  // TODO: "за прошлый год", "за последний месяц" и т.д.
  return null;
}
