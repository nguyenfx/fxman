import json

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from con import Controller

Symbols = {"EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCHF", "USDJPY", "USDCAD", "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY",
           "CHFJPY", "CADJPY", "EURGBP", "EURAUD", "EURNZD", "EURCHF", "EURCAD", "GBPAUD", "GBPNZD", "GBPCHF", "GBPCAD",
           "AUDNZD", "AUDCHF", "AUDCAD", "NZDCHF", "NZDCAD", "CADCHF", "XAUUSD", "BTCUSD"}

con = Controller()


def sentiment_chart():
    sentiments = con.get_sentiments()
    sentiments.reverse()
    sentiments = filter(lambda sen: sen[0] in Symbols, sentiments)
    symbols, sens, cons, timestamp = zip(*sentiments)
    sens = np.asarray(sens)
    colors = np.array(['#ff9100'] * len(sens))
    colors[sens >= 0] = '#00bfa5'
    plt.figure(figsize=(3, 4))
    plt.xticks([])
    plt.yticks(fontsize=6)
    bar_plot = plt.barh(symbols, sens, color=colors, label="Sentiment", zorder=3)
    plt.bar_label(bar_plot, fontsize=6)
    plt.grid(linestyle="dotted", zorder=0)
    plt.twinx()
    cons = np.asarray(cons)
    cons = cons * 10
    colors = np.array(['#ec407a'] * len(cons))
    colors[cons >= 0] = '#3f51b5'
    plt.xticks([])
    plt.yticks([])
    plt.barh(symbols, cons, color=colors, label="Contrarian", zorder=6)
    plt.title("Market Sentiment & Contrarian\n" + timestamp[0] + " GMT", fontsize=8)
    plt.tight_layout()
    file = "static/sentiments.png"
    plt.savefig(file)
    print("Charts generated:", file)
    sentiments = con.get_sentiments()
    sentiments.reverse()
    sentiments = filter(lambda sen: sen[0] in Symbols, sentiments)
    symbols, sens, cons, timestamp = zip(*sentiments)
    sens = np.asarray(sens)
    colors = np.array(['#ff9100'] * len(sens))
    colors[sens >= 0] = '#00bfa5'
    plt.figure(figsize=(3.5, 5))
    plt.xticks([])
    plt.yticks(fontsize=7)
    bar_plot = plt.barh(symbols, sens, color=colors, label="Sentiment", zorder=3)
    plt.bar_label(bar_plot, fontsize=7)
    plt.grid(linestyle="dotted", zorder=0)
    plt.twinx()
    cons = np.asarray(cons)
    cons = cons * 10
    colors = np.array(['#ec407a'] * len(cons))
    colors[cons >= 0] = '#3f51b5'
    plt.xticks([])
    plt.yticks([])
    plt.barh(symbols, cons, color=colors, label="Contrarian", zorder=6)
    selling = mpatches.Patch(color='#ff9100', label='Selling')
    buying = mpatches.Patch(color='#00bfa5', label='Buying')
    bearish = mpatches.Patch(color='#ec407a', label='Bearish')
    bullish = mpatches.Patch(color='#3f51b5', label='Bullish')
    plt.legend(handles=[selling, buying, bearish, bullish], prop={'size': 6})
    plt.title("Updated " + timestamp[0] + " GMT, ©FXMan", fontsize=8)
    plt.tight_layout()
    file = "public/sentiments.png"
    plt.savefig(file)
    print("Charts generated:", file)
    plt.clf()


def symbol_chart():
    for symbol in Symbols:
        history = con.get_sentiment_history(symbol)
        sentiment, date = zip(*history)
        plt.figure(figsize=(3.5, 1.5))
        plt.ylim([0, 100])
        plt.yticks([])
        plt.twinx()
        plt.xticks([])
        plt.yticks(fontsize=6)
        plt.ylim([0, 100])
        plt.plot(date, sentiment, color="#ffc400", label="Sentiment", zorder=6, alpha=0.7)
        plt.fill_between(date, sentiment, color="#ffc400", alpha=0.3)
        selling = mpatches.Patch(color='#ff9100', label='Short')
        buying = mpatches.Patch(color='#00bfa5', label='Long')
        plt.legend(handles=[selling, buying], prop={'size': 6}, loc='upper left')
        plt.title(symbol, fontsize=7)
        plt.tight_layout()
        file = "public/sen" + symbol + ".png"
        plt.savefig(file)
        print("Charts generated:", file)
        plt.cla()
    plt.clf()


def statistic_chart():
    con.calculate_last_statistic()
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        statistic = con.get_statistic(number)
        _, date, profit, balance, percent, growth = zip(*statistic)
        balance = np.asarray(balance)
        balance[-1] = balance[-1] + account[15]
        profit = np.asarray(profit)
        profit_colors = np.array(['#f44336'] * len(profit))
        profit_colors[profit >= 0] = '#3d5afe'
        growth = np.asarray(growth)
        pos_growth = growth.copy()
        neg_growth = growth.copy()
        pos_growth[pos_growth < 0] = np.nan
        neg_growth[neg_growth > 0] = np.nan
        plt.figure(figsize=(9, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right")
        plt.yticks(fontsize=6)
        plt.ylabel("Balance", size=7)
        plt.plot(date, balance, color="#ffc400", label="Balance", zorder=6, alpha=0.7)
        plt.fill_between(date, balance, color="#ffc400", alpha=0.3)
        plt.twinx()
        plt.yticks([])
        bar_plot = plt.bar(date, profit, color=profit_colors, label="Profit", zorder=3, alpha=0.7)
        plt.bar_label(bar_plot, fontsize=6)
        plt.twinx()
        plt.yticks(fontsize=6)
        plt.ylabel("Growth", size=7)
        plt.plot(date, pos_growth, color='#00e676', label="Growth", zorder=9, alpha=0.7)
        plt.plot(date, neg_growth, color='#d500f9', label="Growth", zorder=9, alpha=0.7)
        plt.grid(linestyle="dotted", color='#9e9e9e', zorder=0)
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
        profit_colors = np.array(['#f44336'] * len(profit))
        profit_colors[profit >= 0] = '#3d5afe'
        growth = np.asarray(growth)
        pos_growth = growth.copy()
        neg_growth = growth.copy()
        pos_growth[pos_growth < 0] = np.nan
        neg_growth[neg_growth > 0] = np.nan
        plt.figure(figsize=(5, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right")
        plt.yticks(fontsize=6)
        plt.ylabel("Balance", size=7)
        plt.plot(date, balance, color="#ffc400", label="Balance", zorder=6, alpha=0.7)
        plt.fill_between(date, balance, color="#ffc400", alpha=0.3)
        plt.twinx()
        plt.yticks([])
        bar_plot = plt.bar(date, profit, color=profit_colors, label="Profit", zorder=3, alpha=0.7)
        plt.bar_label(bar_plot, fontsize=6)
        plt.twinx()
        plt.yticks(fontsize=6)
        plt.ylabel("Growth", size=7)
        plt.plot(date, pos_growth, color='#00e676', label="Growth", zorder=9, alpha=0.7)
        plt.plot(date, neg_growth, color='#d500f9', label="Growth", zorder=9, alpha=0.7)
        plt.grid(linestyle="dotted", color='#9e9e9e', zorder=0)
        plt.title("Monthly profit, balance and growth", fontsize=8)
        plt.tight_layout()
        file = "static/m" + str(number) + ".png"
        plt.savefig(file)
        print("Charts generated:", file)
        profits = con.get_symbol_profits(number)
        x, y = zip(*profits)
        y = np.asarray(y)
        colors = np.array(['#f44336'] * len(y))
        colors[y >= 0] = '#3d5afe'
        plt.figure(figsize=(4, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right")
        plt.yticks(fontsize=6)
        plt.bar(x, y, color=colors, alpha=0.7)
        plt.title("Symbols profit", fontsize=8)
        plt.tight_layout()
        file = "static/s" + str(number) + ".png"
        plt.savefig(file)
        print("Charts generated:", file)
        plt.cla()
    plt.clf()


def save_signal():
    signals = con.get_signals()
    with open('public/signals.json', 'w') as file:
        json.dump(signals, file)


if __name__ == "__main__":
    sentiment_chart()
    symbol_chart()
    statistic_chart()
    save_signal()
