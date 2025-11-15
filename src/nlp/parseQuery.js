// parseQuery.js
import { detectMetrics } from "./metrics.js";
import { detectGroupBy } from "./groupBy.js";
import { detectFilters } from "./filters.js";
import { detectLimit } from "./limit.js";

export function parseQuery(userQuery, merchantsList = []) {
  const metrics = detectMetrics(userQuery);
  const group_by = detectGroupBy(userQuery);
  const filters = detectFilters(userQuery, merchantsList);
  const limit = detectLimit(userQuery);

  const result = {
    user_query: userQuery,
  };

  if (metrics.length) result.metrics = metrics;
  if (group_by.length) result.group_by = group_by;
  if (filters.length) result.filters = filters;
  if (limit !== null) result.limit = limit;

  return result;
}
