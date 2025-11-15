import { detectMetrics } from "./metrics.js";
import { detectGroupBy } from "./groupBy.js";
import { detectFilters } from "./filters.js";
import { detectLimit } from "./limit.js";

export function parseQuery(userQuery, merchantsList = [], language = "ru") {
  const metrics = detectMetrics(userQuery, language);
  const group_by = detectGroupBy(userQuery, language);
  const filters = detectFilters(userQuery, merchantsList, language);
  const limit = detectLimit(userQuery, language);

  const result = {
    user_query: userQuery,
    metrics,
  };

  if (group_by.length) {
    result.group_by = group_by;
  }

  if (filters.length) {
    result.filters = filters;
  }

  if (limit !== null) {
    result.limit = limit;
  }

  return result;
}
