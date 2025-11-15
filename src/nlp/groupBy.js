import { groupBySynonyms } from "./synonyms.js";

export function detectGroupBy(text) {
  const lower = text.toLowerCase();
  const result = [];

  Object.keys(groupBySynonyms).forEach((key) => {
    const synonyms = groupBySynonyms[key];
    const found = synonyms.some((s) => lower.includes(s.toLowerCase()));
    if (found) result.push(key);
  });

  return result;
}
