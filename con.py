from db import get_db, get_mem


def get_accounts():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM accounts ORDER BY broker, name, number "
    cursor.execute(statement)
    return cursor.fetchall()


def upsert_account(number, name, broker, server, deposit, credit, withdraw, balance,
                   equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                   depositload, drawdown, lastupdate):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR REPLACE INTO accounts(number, name, broker, server, deposit, credit, withdraw, balance, " \
                "equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit, " \
                "depositload, drawdown, lastupdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    cursor.execute(statement, [number, name, broker, server, deposit, credit, withdraw, balance,
                               equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                               depositload, drawdown, lastupdate])
    db.commit()
    return True


def get_deals():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM deals ORDER BY time DESC LIMIT 100 "
    cursor.execute(statement)
    return cursor.fetchall()


def insert_deal(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic, comment):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR IGNORE INTO deals(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, " \
                "profit, magic, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    cursor.execute(statement,
                   [ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                    comment])
    db.commit()
    return True


def get_positions():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM positions ORDER BY time DESC "
    cursor.execute(statement)
    return cursor.fetchall()


def insert_position(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                    comment):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR REPLACE INTO positions(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, " \
                "profit, magic, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    cursor.execute(statement,
                   [ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                    comment])
    db.commit()
    return True


def reset_positions(number):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM positions WHERE number = ? "
    cursor.execute(statement, [number])
    db.commit()
    return True


def get_status():
    mem = get_mem()
    cursor = mem.cursor()
    statement = "SELECT * FROM status ORDER BY number "
    cursor.execute(statement)
    return cursor.fetchall()


def reset_status():
    mem = get_mem()
    cursor = mem.cursor()
    statement = "UPDATE status SET online = 0 "
    cursor.execute(statement)
    mem.commit()
    return True


def upsert_status(number, online):
    mem = get_mem()
    cursor = mem.cursor()
    statement = "INSERT OR REPLACE INTO status(number, online) VALUES (?, ?) "
    cursor.execute(statement, [number, online])
    mem.commit()
    return True


def get_sentiments():
    mem = get_mem()
    cursor = mem.cursor()
    statement = "SELECT * FROM sentiments ORDER BY symbol "
    cursor.execute(statement)
    return cursor.fetchall()


def get_sentiment(symbol):
    mem = get_mem()
    cursor = mem.cursor()
    statement = "SELECT value FROM sentiments WHERE symbol = ?  "
    cursor.execute(statement, [symbol])
    return cursor.fetchone()


def insert_sentiment(symbol, value):
    mem = get_mem()
    cursor = mem.cursor()
    statement = "INSERT OR REPLACE INTO sentiments(symbol, value) VALUES (?, ?) "
    cursor.execute(statement, [symbol, value])
    mem.commit()
    return True


def get_statistic(number):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM statistic WHERE number = ? ORDER BY date "
    cursor.execute(statement, [number])
    return cursor.fetchall()


def get_symbol_profits(number):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT symbol, SUM(profit - commission + swap) AS sprofit FROM deals WHERE number = ? AND (type = 0 " \
                "OR type = 1) GROUP BY symbol ORDER BY sprofit DESC "
    cursor.execute(statement, [number])
    return cursor.fetchall()


def calculate_all_statistic():
    db = get_db()
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


def calculate_last_statistic():
    db = get_db()
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
#