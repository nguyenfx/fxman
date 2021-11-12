from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import con


def save_image(title, number, data, width):
    x, y = zip(*data)
    y = np.asarray(y)
    colors = np.array([(1, 0, 0)] * len(y))
    colors[y >= 0] = (0, 0, 1)
    plt.figure(figsize=(width, 2))
    plt.xticks(rotation=45, fontsize=6, ha="right")
    plt.yticks(fontsize=7)
    plt.title(title, fontsize=8)
    plt.tight_layout()
    plt.bar(x, y, color=colors)
    plt.savefig("static/" + title[0].lower() + str(number) + ".png")
    # plt.show()


def save_images():
    accounts = con.get_accounts()
    for account in accounts:
        number = account[0]
        dp = con.get_dailyprofits(number)
        save_image("Daily profit", number, dp, 8)
        sp = con.get_symbolprofits(number)
        save_image("Symbols profit", number, sp, 4)


if __name__ == "__main__":
    save_images()
