import chart
from con import Controller
import sen

if __name__ == "__main__":
    sen.fetch()
    chart.gen_chart()
    con = Controller()
    sentiments = con.get_sentiments()
    print(sentiments)
    status = con.get_status()
    print(status)
    con.calculate_all_statistic()
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        stats = con.get_statistic(number)
        print(stats)
