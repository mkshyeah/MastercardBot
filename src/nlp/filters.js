import { detectTimePeriod } from "./timePeriod.js";

export function detectFilters(text, merchantsList = [], language = "ru") {
  const lower = text.toLowerCase();
  const filters = [];

  const kazakhstanSynonyms = {
    ru: ["казахстан"],
    en: ["kazakhstan"],
    kz: ["қазақстан", "kazakstan"],
  };

  const currentLangSyns = kazakhstanSynonyms[language] || [];

  const isKazakhstanMentioned = currentLangSyns.some((s) =>
    lower.includes(s.toLowerCase())
  );

  if (isKazakhstanMentioned) {
    filters.push({
      field: "country",
      operator: "=",
      value: "Kazakhstan",
    });
  }

  merchantsList.forEach((m) => {
    if (lower.includes(m.toLowerCase())) {
      filters.push({
        field: "merchant_name",
        operator: "=",
        value: m,
      });
    }
  });

  const period = detectTimePeriod(text, language);

  if (period) {
    filters.push({
      field: "time_period",
      operator: "=",
      value: period, // ["YYYY-MM-DD", "YYYY-MM-DD"]
    });
  }

  return filters;
}
