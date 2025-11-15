import { metricSynonyms } from "./synonyms.js";

export function detectMetrics(text, language = "ru") {
  const lower = text.toLowerCase();
  const result = [];

  Object.keys(metricSynonyms).forEach((metricKey) => {
    const langSyns = metricSynonyms[metricKey][language] || [];
    const found = langSyns.some((s) => lower.includes(s.toLowerCase()));
    if (found) {
      result.push(metricKey);
    }
  });

  return result;
}
