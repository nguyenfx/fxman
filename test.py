import db, con





if __name__ == "__main__":
    db.create_tables()
    con.calculate_last_statistic()
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        stats = con.get_statistic(number)
        print(stats)
