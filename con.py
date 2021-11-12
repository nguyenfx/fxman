from db import get_db


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
    statement = "SELECT * FROM positions ORDER BY time "
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


def get_sentiments():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM sentiments ORDER BY symbol "
    cursor.execute(statement)
    return cursor.fetchall()


def get_sentiment(symbol):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT value FROM sentiments WHERE symbol = ?  "
    cursor.execute(statement, [symbol])
    return cursor.fetchone()


def insert_sentiment(symbol, value):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR REPLACE INTO sentiments(symbol, value) VALUES (?, ?) "
    cursor.execute(statement, [symbol, value])
    db.commit()
    return True


def get_dailyprofits(number):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT DATE(REPLACE(time, '.', '-')) AS date, SUM(profit - commission + swap) AS dprofit FROM deals " \
                "WHERE number = ? GROUP BY date ORDER BY date "
    cursor.execute(statement, [number])
    return cursor.fetchall()


def get_symbolprofits(number):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT symbol, SUM(profit - commission + swap) AS sprofit FROM deals WHERE number = ? GROUP BY " \
                "symbol ORDER BY sprofit DESC "
    cursor.execute(statement, [number])
    return cursor.fetchall()
