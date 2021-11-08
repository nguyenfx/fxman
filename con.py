from db import get_db


def get_accounts():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM accounts"
    cursor.execute(statement)
    return cursor.fetchall()


def upsert_account(number, name, broker, server, deposit, credit, withdraw, balance,
                   equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                   depositload, drawdown, lastupdate):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR REPLACE INTO accounts(number, name, broker, server, deposit, credit, withdraw, balance, " \
                "equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit, " \
                "depositload, drawdown, lastupdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(statement, [number, name, broker, server, deposit, credit, withdraw, balance,
                               equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                               depositload, drawdown, lastupdate])
    db.commit()
    return True


def get_deals():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM deals"
    cursor.execute(statement)
    return cursor.fetchall()


def insert_deal(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic, comment):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR IGNORE INTO deals(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, " \
                "profit, magic, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    cursor.execute(statement, [ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic, comment])
    db.commit()
    return True


def get_positions():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM positions"
    cursor.execute(statement)
    return cursor.fetchall()


def insert_position(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic, comment):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT OR REPLACE INTO positions(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, " \
                "profit, magic, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    cursor.execute(statement, [ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic, comment])
    db.commit()
    return True


def reset_positions(number):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM positions WHERE number = ?"
    cursor.execute(statement, [number])
    db.commit()
    return True
