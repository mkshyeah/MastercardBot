// filters.js
import { detectTimePeriod } from "./timePeriod.js";

export function detectFilters(text, merchantsList = []) {
  const lower = text.toLowerCase();
  const filters = [];

  // страна (пример только Kazakhstan)
  if (lower.includes("kazakhstan") || lower.includes("казахстан")) {
    filters.push({
      field: "country",
      operator: "=",
      value: "Kazakhstan",
    });
  }

  // мерчанты — из списка, который тебе даст Человек А
  merchantsList.forEach((m) => {
    if (lower.includes(m.toLowerCase())) {
      filters.push({
        field: "merchant_name",
        operator: "=",
        value: m,
      });
    }
  });

  // период
  const period = detectTimePeriod(text);
  if (period) {
    filters.push({
      field: "time_period",
      operator: "=",
      value: period, // ["YYYY-MM-DD", "YYYY-MM-DD"]
    });
  }

  return filters;
}
