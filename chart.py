import matplotlib.pyplot as plt
import numpy as np
import con


def dailychart(number):
    profits = con.get_dailyprofits(number)
    balances = con.get_dailybalances(number)
    x, y = zip(*profits)
    x1, y1 = zip(*balances)
    y = np.asarray(y)
    colors = np.array([(1, 0, 0)] * len(y))
    colors[y >= 0] = (0, 0, 1)
    plt.figure(figsize=(10, 2))
    plt.xticks(rotation=45, fontsize=6, ha="right")
    plt.yticks(fontsize=6)
    plt.bar(x, y, color=colors)
    plt.twinx()
    plt.yticks(fontsize=6)
    plt.plot(x, y1, color='g')
    plt.title("Daily balance and profit", fontsize=8)
    plt.tight_layout()
    plt.savefig("static/d" + str(number) + ".png")
    # plt.show()


def symbolchart(number):
    profits = con.get_symbolprofits(number)
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
    plt.savefig("static/s" + str(number) + ".png")
    # plt.show()


def save_images():
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        dailychart(number)
        symbolchart(number)


if __name__ == "__main__":
    save_images()
