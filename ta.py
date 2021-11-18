import json

from tradingview_ta import *

from con import Controller

Symbols = ["FX_IDC:EURUSD", "FX_IDC:GBPUSD", "FX_IDC:AUDUSD", "FX_IDC:NZDUSD", "FX_IDC:USDCHF", "FX_IDC:USDJPY",
           "FX_IDC:USDCAD", "FX_IDC:EURJPY", "FX_IDC:GBPJPY", "FX_IDC:AUDJPY", "FX_IDC:NZDJPY", "FX_IDC:CHFJPY",
           "FX_IDC:CADJPY", "FX_IDC:EURGBP", "FX_IDC:EURAUD", "FX_IDC:EURNZD", "FX_IDC:EURCHF", "FX_IDC:EURCAD",
           "FX_IDC:GBPAUD", "FX_IDC:GBPNZD", "FX_IDC:GBPCHF", "FX_IDC:GBPCAD", "FX_IDC:AUDNZD", "FX_IDC:AUDCHF",
           "FX_IDC:AUDCAD", "FX_IDC:NZDCHF", "FX_IDC:NZDCAD", "FX_IDC:CADCHF"]

Intervals = {Interval.INTERVAL_1_DAY, Interval.INTERVAL_4_HOURS, Interval.INTERVAL_1_HOUR, Interval.INTERVAL_15_MINUTES}

con = Controller()


def get_price(symbol):
    if symbol == "XAUUSD":
        handle = TA_Handler(
            symbol="GOLD",
            screener="cfd",
            exchange="TVC",
            interval=Interval.INTERVAL_1_MINUTE
        )
    elif symbol == "BTCUSD":
        handle = TA_Handler(
            symbol="BTCUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_MINUTE
        )
    else:
        handle = TA_Handler(
            symbol=symbol,
            screener="forex",
            exchange="FX_IDC",
            interval=Interval.INTERVAL_1_MINUTE
        )
    analysis = handle.get_analysis()
    return analysis.indicators["close"]


def upsert(symbol, timeframe, analysis):
    ma = 0
    if analysis.moving_averages['RECOMMENDATION'] == "STRONG_BUY" or analysis.moving_averages[
        'RECOMMENDATION'] == "BUY":
        ma = 1
    elif analysis.moving_averages['RECOMMENDATION'] == "STRONG_SELL" or analysis.moving_averages[
        'RECOMMENDATION'] == "SELL":
        ma = -1
    os = 0
    if analysis.oscillators['RECOMMENDATION'] == "STRONG_BUY" or analysis.oscillators['RECOMMENDATION'] == "BUY":
        os = 1
    elif analysis.oscillators['RECOMMENDATION'] == "STRONG_SELL" or analysis.oscillators['RECOMMENDATION'] == "SELL":
        os = -1
    con.upsert_ta(symbol, timeframe, ma, os)


def fetch():
    for interval in Intervals:
        data = get_multiple_analysis(screener="forex", interval=interval, symbols=Symbols)
        for symbol in Symbols:
            analysis = data[symbol]
            upsert(analysis.symbol, interval, analysis)
        handle = TA_Handler(
            symbol="GOLD",
            screener="cfd",
            exchange="TVC",
            interval=interval
        )
        analysis = handle.get_analysis()
        upsert("XAUUSD", interval, analysis)
        handle = TA_Handler(
            symbol="BTCUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=interval
        )
        analysis = handle.get_analysis()
        upsert("BTCUSD", interval, analysis)
    tas = con.get_tas()
    print(json.dumps(tas))


def find_signals():
    tas = con.get_tas()
    for ta in tas:
        symbol = ta[0]
        contrarian = ta[1]
        trend = ta[2]
        entry = ta[3]
        if contrarian > 0 and trend > 1 and entry > 1:
            price = get_price(symbol)
            con.upsert_signal(0, symbol, 1, 1, price)
        if contrarian < 0 and trend < -1 and entry < -1:
            price = get_price(symbol)
            con.upsert_signal(0, symbol, -1, 1, price)
    signals = con.get_signals()
    with open('public/tas.json', 'w') as file:
        json.dump(tas, file)
    with open('public/signals.json', 'w') as file:
        json.dump(signals, file)


if __name__ == "__main__":
    fetch()
    con.calculate_contrarian()
    find_signals()
