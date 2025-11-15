import { METRICS, GROUP_BY } from "./constants.js";

export const metricSynonyms = {
  transaction_count: [
    "количество транзакций",
    "число транзакций",
    "transactions",
    "transaction count",
  ],
  revenue: ["выручка", "оборот", "сумма транзакций", "revenue"],
  average_check: ["средний чек", "average check"],
  decline_rate: ["уровень отказов", "decline rate", "доля отказов"],
};

export const groupBySynonyms = {
  merchant_name: ["по мерчантам", "по магазинам", "по продавцам"],
  mcc_category: ["по категориям", "по типу бизнеса"],
  merchant_city: ["по городам", "по городу"],
  country: ["по странам", "по стране"],
  date_day: ["по дням", "ежедневно", "daily"],
  date_month: ["по месяцам", "ежемесячно", "by month", "monthly"],
  date_year: ["по годам", "ежегодно", "yearly", "by year"],
};
