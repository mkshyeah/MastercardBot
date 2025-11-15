import { groupBySynonyms } from "./synonyms.js";

export function detectGroupBy(text, language = "ru") {
  const lower = text.toLowerCase();
  const result = [];

  Object.keys(groupBySynonyms).forEach((groupKey) => {
    const synonyms = groupBySynonyms[groupKey][language] || [];
    const found = synonyms.some((s) => lower.includes(s.toLowerCase()));
    if (found) result.push(groupKey);
  });

  return result;
}
