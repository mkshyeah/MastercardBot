// import { METRICS, GROUP_BY } from "./constants.js";

export const metricSynonyms = {
  transaction_count: {
    ru: [
      "количество транзакций",
      "число транзакций",
      "сколько было транзакций",
    ],
    en: ["transaction count", "number of transactions", "transactions"],
    kz: ["транзакциялар саны", "операциялар саны", "төлемдер саны"],
  },

  revenue: {
    ru: ["выручка", "общая выручка", "оборот", "сумма транзакций"],
    en: ["revenue", "total amount", "turnover"],
    kz: ["түсім", "жалпы түсім", "айналым", "транзакциялар сомасы"],
  },

  average_check: {
    ru: ["средний чек"],
    en: ["average check", "avg check"],
    kz: ["орташа чек"],
  },

  decline_rate: {
    ru: ["уровень отказов", "процент отказов", "доля отказов"],
    en: ["decline rate", "decline ratio", "reject rate"],
    kz: ["бас тарту деңгейі", "қабылдамау деңгейі", "бас тарту үлесі"],
  },
};

export const groupBySynonyms = {
  merchant_name: {
    ru: ["по мерчантам", "по магазинам", "по продавцам"],
    en: ["by merchant", "by merchants", "by shop", "by shops"],
    kz: ["мерчанттар бойынша", "дүкендер бойынша", "сатушылар бойынша"],
  },

  mcc_category: {
    ru: ["по категориям", "по категории", "по типу бизнеса"],
    en: ["by category", "by categories", "by business type"],
    kz: ["санаттар бойынша", "санат бойынша", "бизнес түрі бойынша"],
  },

  merchant_city: {
    ru: ["по городам", "по городу"],
    en: ["by city", "by cities"],
    kz: ["қалалар бойынша", "қала бойынша"],
  },

  country: {
    ru: ["по странам", "по стране"],
    en: ["by country", "by countries"],
    kz: ["елдер бойынша", "ел бойынша"],
  },

  date_day: {
    ru: ["по дням", "ежедневно", "каждый день"],
    en: ["by day", "daily", "every day"],
    kz: ["күндер бойынша", "күн сайын", "күнделікті"],
  },

  date_month: {
    ru: ["по месяцам", "ежемесячно", "каждый месяц"],
    en: ["by month", "monthly", "every month"],
    kz: ["айлар бойынша", "ай сайын", "ай сайынғы"],
  },

  date_year: {
    ru: ["по годам", "ежегодно", "каждый год"],
    en: ["by year", "yearly", "every year"],
    kz: ["жылдар бойынша", "жыл сайын", "жыл сайынғы"],
  },
};
