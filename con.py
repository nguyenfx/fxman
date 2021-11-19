from db import Database


class Controller:

    def __init__(self):
        self.database = Database()

    def get_db(self):
        return self.database.get_db_conn()

    def get_accounts(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM accounts ORDER BY broker, name, number "
        cursor.execute(statement)
        return cursor.fetchall()

    def upsert_account(self, number, name, broker, server, deposit, credit, withdraw, balance,
                       equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                       depositload, drawdown, lastupdate):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO accounts(number, name, broker, server, deposit, credit, withdraw, balance, " \
                    "equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit, " \
                    "depositload, drawdown, lastupdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        cursor.execute(statement, [number, name, broker, server, deposit, credit, withdraw, balance,
                                   equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                                   depositload, drawdown, lastupdate])
        db.commit()
        return True

    def get_deals(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM deals ORDER BY time DESC LIMIT (SELECT COUNT(*) FROM positions) "
        cursor.execute(statement)
        return cursor.fetchall()

    def insert_deal(self, ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                    comment):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR IGNORE INTO deals(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, " \
                    "profit, magic, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        cursor.execute(statement,
                       [ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                        comment])
        db.commit()
        return True

    def get_positions(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM positions ORDER BY time DESC "
        cursor.execute(statement)
        return cursor.fetchall()

    def insert_position(self, ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit,
                        magic,
                        comment):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO positions(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, " \
                    "profit, magic, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        cursor.execute(statement,
                       [ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                        comment])
        db.commit()
        return True

    def reset_positions(self, number):
        db = self.get_db()
        cursor = db.cursor()
        statement = "DELETE FROM positions WHERE number = ? "
        cursor.execute(statement, [number])
        db.commit()
        return True

    def get_status(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM status ORDER BY number "
        cursor.execute(statement)
        return cursor.fetchall()

    def reset_status(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "UPDATE status SET online = 0 "
        cursor.execute(statement)
        db.commit()
        return True

    def upsert_status(self, number, online, error):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO status(number, online, error) VALUES (?, ?, ?) "
        cursor.execute(statement, [number, online, error])
        db.commit()
        return True

    def get_signals(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM signals WHERE (JULIANDAY('now') - JULIANDAY(timestamp)) * 86400 / 60 < 1440 ORDER " \
                    "BY timestamp DESC "
        cursor.execute(statement)
        return cursor.fetchall()

    def get_signals_delay(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM signals WHERE (JULIANDAY('now') - JULIANDAY(timestamp)) * 86400 / 60 > 60 AND (" \
                    "JULIANDAY('now') - JULIANDAY(timestamp)) * 86400 / 60 < 1440 * 30 ORDER BY timestamp DESC "
        cursor.execute(statement)
        return cursor.fetchall()

    def get_signal(self, symbol):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT type * risk FROM signals WHERE symbol = ? AND  (JULIANDAY('now') - JULIANDAY(timestamp))  " \
                    "* 86400 / 60 < 60 ORDER BY timestamp DESC "
        cursor.execute(statement, [symbol])
        return cursor.fetchone()

    def upsert_signal(self, number, symbol, type, risk, open_price):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO signals(number, symbol, type, risk, open_price, current_price, datehour) " \
                    "VALUES (?, ?, ?, ?, ?, ?, strftime('%Y-%m-%d %H', CURRENT_TIMESTAMP)) "
        cursor.execute(statement, [number, symbol, type, risk, open_price, open_price])
        db.commit()
        return True

    def update_signal(self, symbol, current_price):
        db = self.get_db()
        cursor = db.cursor()
        statement = "UPDATE signals SET current_price = ? WHERE symbol = ? "
        cursor.execute(statement, [current_price, symbol])
        db.commit()
        return True

    def get_sentiments(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT symbol, ROUND(AVG(sentiment) - 0.5), SUM(contrarian), timestamp FROM sentiments " \
                    "WHERE date = DATE('now') GROUP BY symbol ORDER BY symbol "
        cursor.execute(statement)
        return cursor.fetchall()

    def get_sentiment_history(self, symbol):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT ROUND(50 + AVG(sentiment) / 2 - 0.5), date FROM sentiments WHERE symbol = ? " \
                    "GROUP BY date ORDER BY date LIMIT 10 "
        cursor.execute(statement, [symbol])
        return cursor.fetchall()

    def get_contrarian(self, symbol):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT SUM(contrarian) FROM sentiments WHERE symbol = ? AND date = DATE('now') GROUP BY symbol "
        cursor.execute(statement, [symbol])
        return cursor.fetchone()

    def upsert_sentiment(self, site, symbol, sentiment, contrarian):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO sentiments(site, symbol, sentiment, contrarian, date) VALUES (?, ?, ?, ?, DATE('now')) "
        cursor.execute(statement, [site, symbol, sentiment, contrarian])
        db.commit()
        return True

    def get_tas(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "select distinct tas.symbol, sub3.contrarian, sub1.ma, sub2.os from tas inner join (select symbol, sum(ma) as ma " \
                    "from tas where interval = '1d' or interval = '4h' group by symbol) as sub1 on tas.symbol = " \
                    "sub1.symbol inner join (select symbol, sum(os) as os from tas where interval = '1h' or interval " \
                    "= '15m' group by symbol) as sub2 on tas.symbol = sub2.symbol inner join (select symbol, sum(contrarian) as contrarian " \
                    "from sentiments where date = DATE('now') group by symbol) as sub3 on tas.symbol = sub3.symbol "
        cursor.execute(statement)
        return cursor.fetchall()

    def upsert_ta(self, symbol, interval, ma, os):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO tas(symbol, interval, ma, os) VALUES (?, ?, ?, ?) "
        cursor.execute(statement, [symbol, interval, ma, os])
        db.commit()
        return True

    def calculate_contrarian(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO sentiments(site, symbol, sentiment, contrarian, date) " \
                    "SELECT 'avg', symbol, ROUND(AVG(sentiment) - 0.5), 0, date FROM sentiments " \
                    "WHERE site != 'avg' AND date = DATE('now') GROUP BY symbol, date "
        cursor.execute(statement)
        statement = "UPDATE sentiments SET contrarian = (CASE " \
                    "    WHEN (sentiment < -40 OR (sentiment < -20 AND sentiment < (SELECT sentiment FROM sentiments AS sub WHERE sub.site = 'avg' AND sub.symbol = sentiments.symbol AND sub.date = DATE(sentiments.date,'-1 day')))) " \
                    "        AND (SELECT SUM(ma) FROM tas WHERE sentiments.symbol = tas.symbol AND (interval = '1d' OR interval= '4h')) > 1 " \
                    "        THEN 1 " \
                    "    WHEN (sentiment > 40 OR (sentiment > 20 AND sentiment > (SELECT sentiment FROM sentiments AS sub WHERE sub.site = 'avg' AND sub.symbol = sentiments.symbol AND sub.date = DATE(sentiments.date,'-1 day')))) " \
                    "        AND (SELECT SUM(ma) FROM tas WHERE sentiments.symbol = tas.symbol AND (interval = '1d' OR interval= '4h')) < -1 " \
                    "        THEN -1 " \
                    "    ELSE 0 " \
                    "END) " \
                    "WHERE site = 'avg' AND date = DATE('now') "
        cursor.execute(statement)
        db.commit()
        return True

    def get_statistic(self, number):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT number, substr(date, 3) AS date, profit, balance, percent, growth FROM statistic WHERE number = ? " \
                    "ORDER BY date "
        cursor.execute(statement, [number])
        return cursor.fetchall()

    def get_statistic_m(self, number):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT number, strftime('%Y-%m', date) AS month, SUM(profit), AVG(balance), SUM(percent), " \
                    "AVG(growth) FROM statistic WHERE number = ? GROUP BY month ORDER BY month "
        cursor.execute(statement, [number])
        return cursor.fetchall()

    def get_symbol_profits(self, number):
        db = self.get_db()
        cursor = db.cursor()
        statement = "SELECT symbol, SUM(profit - commission + swap) AS sprofit FROM deals WHERE number = ? AND (type = 0 " \
                    "OR type = 1) GROUP BY symbol ORDER BY sprofit DESC "
        cursor.execute(statement, [number])
        return cursor.fetchall()

    def calculate_all_statistic(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO statistic SELECT number, DATE(REPLACE(time, '.', '-')) AS date, SUM(profit  " \
                    "- commission + swap) AS dprofit, 0, 0, 0 FROM deals WHERE type = 0 OR type = 1 GROUP BY number, date "
        cursor.execute(statement)
        statement = "UPDATE statistic SET balance = (SELECT balance FROM (SELECT number, date, SUM(dprofit) OVER (PARTITION BY number ORDER " \
                    "BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance FROM (SELECT number, " \
                    "DATE(REPLACE(time, '.', '-')) AS date, SUM(profit - commission + swap) AS dprofit FROM deals GROUP " \
                    "BY number, date ORDER BY date) GROUP BY number, date) AS sub WHERE statistic.number = sub.number AND statistic.date = " \
                    "sub.date) "
        cursor.execute(statement)
        statement = "UPDATE statistic SET percent = profit / balance * 100 "
        cursor.execute(statement)
        statement = "UPDATE statistic SET growth = (SELECT growth FROM (SELECT number, date, SUM(percent) OVER (PARTITION BY number ORDER BY date ROWS " \
                    "BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS growth FROM statistic GROUP BY number, date ORDER by date) AS sub WHERE " \
                    "statistic.number = sub.number AND statistic.date = sub.date) "
        cursor.execute(statement)
        db.commit()
        return True

    def calculate_last_statistic(self):
        db = self.get_db()
        cursor = db.cursor()
        statement = "INSERT OR REPLACE INTO statistic SELECT number, DATE(REPLACE(time, '.', '-')) AS date, SUM(profit  " \
                    "- commission + swap) AS dprofit, 0, 0, 0 FROM deals WHERE type = 0 OR type = 1 GROUP BY number, date ORDER BY date DESC LIMIT 100 "
        cursor.execute(statement)
        statement = "UPDATE statistic SET balance = (SELECT balance FROM (SELECT number, date, SUM(dprofit) OVER (PARTITION BY number ORDER " \
                    "BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance FROM (SELECT number, " \
                    "DATE(REPLACE(time, '.', '-')) AS date, SUM(profit - commission + swap) AS dprofit FROM deals GROUP " \
                    "BY number, date ORDER BY date DESC LIMIT 100) GROUP BY number, date) AS sub WHERE statistic.number = sub.number AND statistic.date = " \
                    "sub.date) "
        cursor.execute(statement)
        statement = "UPDATE statistic SET percent = profit / balance * 100 ORDER BY date DESC LIMIT 100 "
        cursor.execute(statement)
        statement = "UPDATE statistic SET growth = (SELECT growth FROM (SELECT number, date, SUM(percent) OVER (PARTITION BY number ORDER BY date ROWS " \
                    "BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS growth FROM statistic GROUP BY number, date ORDER by date DESC LIMIT 100) AS sub WHERE " \
                    "statistic.number = sub.number AND statistic.date = sub.date) "
        cursor.execute(statement)
        db.commit()
        return True
