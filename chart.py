import matplotlib.pyplot as plt
import numpy as np
from con import Controller


def gen_chart():
    con = Controller()
    con.calculate_last_statistic()
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        statistic = con.get_statistic(number)
        _, date, profit, balance, percent, growth = zip(*statistic)
        profit = np.asarray(profit)
        colors = np.array([(1, 0, 0)] * len(profit))
        colors[profit >= 0] = (0, 0, 1)
        plt.figure(figsize=(10, 2))
        plt.xticks(rotation=45, fontsize=6, ha="right", )
        plt.yticks([])
        bar_plot = plt.bar(date, profit, color=colors, label="Profit")
        plt.bar_label(bar_plot, fontsize=6)
        plt.twinx()
        plt.yticks(fontsize=6)
        plt.grid(linestyle="dotted", color='m')
        plt.plot(date, balance, color="m", label="Balance")
        plt.twinx()
        plt.ylabel("Growth", size=7)
        plt.yticks(fontsize=6)
        plt.grid(linestyle="dotted", color='y')
        plt.plot(date, growth, color="y", label="Growth")
        plt.title("Daily profit, balance and growth", fontsize=8)
        plt.tight_layout()
        file = "static/d" + str(number) + ".png"
        plt.savefig(file)
        print("Charts generated:", file)
        profits = con.get_symbol_profits(number)
        x, y = zip(*profits)
        y = np.asarray(y)
        colors = np.array([(1, 0, 0)] * len(y))
        colors[y >= 0] = (0, 0, 1)
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
