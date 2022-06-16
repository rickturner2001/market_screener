def get_success_rate_for_n_days_holding(n_days=60):
    return f"""SELECT
            count(CASE WHEN return > 0 THEN 1 END) as positive_return,
            count(CASE WHEN return < 0 THEN 1 END) as negative_return,
            round(cast(count(CASE WHEN return > 0 THEN 1 END) AS float) / count(return) * 100) AS positivity_rate FROM (
                SELECT ((cast(price_sold AS float) - cast(purchase_price AS float)) / purchase_price) * 100 AS return
                                             FROM api_results AS t1
                                                      INNER JOIN (SELECT ticker,
                                                                         date,
                                                                         lead(close, {n_days}) OVER (
                                                                             PARTITION BY ticker
                                                                             ORDER BY date
                                                                             ROWS BETWEEN 1 FOLLOWING AND {n_days} FOLLOWING
                                                                             ) AS price_sold,
                                                                        lead(close, 1) OVER (
                                                                             PARTITION BY ticker
                                                                             ORDER BY date
                                                                             ROWS BETWEEN 1 FOLLOWING AND {n_days} FOLLOWING
                                                                             ) AS purchase_price
                                                                  FROM historical_data
                                                                  ORDER BY ticker, date) AS t2
                                                                 ON t1.ticker = t2.ticker AND t1.date = t2.date)"""


def get_grouped_data(group_by, n_days=60):
    return f"""              select {group_by},
                       count(CASE WHEN return > 0 THEN 1 END) AS positive_return,
                       count(CASE WHEN return < 0 THEN 1 END) AS negative_return,
                       round(cast(count(CASE WHEN return > 0 THEN 1 END) as float) / count(return) * 100, 2) as positivity_ratio from(
                                        SELECT {group_by},
                                                    ((cast(price_sold as float) - cast(purchase_price as float)) / purchase_price) * 100 as return
                                             FROM api_results AS t1
                                                      INNER JOIN (SELECT ticker,
                                                                         date,
                                                                         Lead(close, {n_days}) OVER (
                                                                             PARTITION BY ticker
                                                                             ORDER BY date
                                                                             ROWS BETWEEN 1 FOLLOWING AND {n_days} FOLLOWING
                                                                             ) AS price_sold,
                                                                        Lead(close, 1) OVER (
                                                                             PARTITION BY ticker
                                                                             ORDER BY date
                                                                             ROWS BETWEEN 1 FOLLOWING AND {n_days} FOLLOWING
                                                                             ) AS purchase_price
                                                                  FROM historical_data
                                                                  ORDER BY ticker, date) AS t2
                                                                 ON t1.ticker = t2.ticker AND t1.date = t2.date)
                                                group by {group_by}"""
