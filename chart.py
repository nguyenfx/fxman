import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from con import Controller

Symbols = {"EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCHF", "USDJPY", "USDCAD", "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY",
           "CHFJPY", "CADJPY", "EURGBP", "EURAUD", "EURNZD", "EURCHF", "EURCAD", "GBPAUD", "GBPNZD", "GBPCHF", "GBPCAD",
           "AUDNZD", "AUDCHF", "AUDCAD", "NZDCHF", "NZDCAD", "XAUUSD", "BTCUSD"}


def gen_chart():
    con = Controller()
    sentiments = con.get_sentiments()
    sentiments.reverse()
    sentiments = filter(lambda sen: sen[0] in Symbols, sentiments)
    symbols, values = zip(*sentiments)
    values = np.asarray(values)
    colors = np.array(['#e69138'] * len(values))
    colors[values >= 0] = '#6aa84f'
    plt.figure(figsize=(3, 4))
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)
    bar_plot = plt.barh(symbols, values, color=colors, label="Sentiment", zorder=3)
    plt.bar_label(bar_plot, fontsize=6)
    plt.grid(linestyle="dotted", zorder=0)
    today = datetime.utcnow()
    plt.title("Market Sentiment - " + today.strftime('%Y-%m-%d %H:%M GMT'), fontsize=8)
    plt.tight_layout()
    file = "static/sentiments.png"
    plt.savefig(file)
    print("Charts generated:", file)
    con.calculate_last_statistic()
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        statistic = con.get_statistic(number)
        _, date, profit, balance, percent, growth = zip(*statistic)
        balance = np.asarray(balance)
        balance[-1] = balance[-1] + account[15]
        profit = np.asarray(profit)
        colors = np.array(['#cc0000'] * len(profit))
        colors[profit >= 0] = '#3c78d8'
        plt.figure(figsize=(9, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right")
        plt.yticks(fontsize=6)
        plt.ylabel("Balance", size=7)
        plt.plot(date, balance, color="#f1c232", label="Balance", zorder=6)
        plt.fill_between(date, balance, color="#f1c232", alpha=0.5)
        plt.grid(linestyle="dotted", color='#f1c232', zorder=0)
        plt.twinx()
        plt.yticks([])
        bar_plot = plt.bar(date, profit, color=colors, label="Profit", zorder=3)
        plt.bar_label(bar_plot, fontsize=6)
        plt.twinx()
        plt.yticks(fontsize=6)
        plt.ylabel("Growth", size=7)
        plt.plot(date, growth, color="#00cc00", label="Growth", zorder=9)
        plt.grid(linestyle="dotted", color='#00cc00', zorder=0)
        plt.title("Daily profit, balance and growth", fontsize=8)
        plt.tight_layout()
        file = "static/d" + str(number) + ".png"
        plt.savefig(file)
        print("Charts generated:", file)
        statistic = con.get_statistic_m(number)
        _, date, profit, balance, percent, growth = zip(*statistic)
        balance = np.asarray(balance)
        balance[-1] = balance[-1] + account[15]
        profit = np.asarray(profit)
        colors = np.array(['#cc0000'] * len(profit))
        colors[profit >= 0] = '#3c78d8'
        plt.figure(figsize=(5, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right")
        plt.yticks(fontsize=6)
        plt.ylabel("Balance", size=7)
        plt.plot(date, balance, color="#f1c232", label="Balance", zorder=6)
        plt.fill_between(date, balance, color="#f1c232", alpha=0.5)
        plt.grid(linestyle="dotted", color='#f1c232', zorder=0)
        plt.twinx()
        plt.yticks([])
        bar_plot = plt.bar(date, profit, color=colors, label="Profit", zorder=3)
        plt.bar_label(bar_plot, fontsize=6)
        plt.twinx()
        plt.yticks(fontsize=6)
        plt.ylabel("Growth", size=7)
        plt.plot(date, growth, color="#00cc00", label="Growth", zorder=9)
        plt.grid(linestyle="dotted", color='#00cc00', zorder=0)
        plt.title("Daily profit, balance and growth", fontsize=8)
        plt.tight_layout()
        file = "static/m" + str(number) + ".png"
        plt.savefig(file)
        print("Charts generated:", file)
        profits = con.get_symbol_profits(number)
        x, y = zip(*profits)
        y = np.asarray(y)
        colors = np.array(['#cc0000'] * len(y))
        colors[y >= 0] = '#3c78d8'
        plt.figure(figsize=(4, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right")
        plt.yticks(fontsize=6)
        plt.bar(x, y, color=colors)
        plt.title("Symbols profit", fontsize=8)
        plt.tight_layout()
        file = "static/s" + str(number) + ".png"
        plt.savefig(file)
        print("Charts generated:", file)


if __name__ == "__main__":
    gen_chart()
