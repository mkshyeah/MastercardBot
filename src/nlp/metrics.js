import { metricSynonyms } from "./synonyms.js";

export function detectMetrics(text) {
  const lower = text.toLowerCase();
  const result = [];

  Object.keys(metricSynonyms).forEach((metric) => {
    const synonyms = metricSynonyms[metric];
    const found = synonyms.some((s) => lower.includes(s.toLowerCase()));
    if (found) result.push(metric);
  });

  return result;
}
