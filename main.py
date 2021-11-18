from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from uwsgidecorators import postfork

import sen
from con import Controller

con = Controller()

app = Flask(__name__, static_url_path='/static')
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)


@postfork
def init():
    sen.fetch()


@app.route('/accounts', methods=["GET"])
@cache.cached(timeout=300)
def get_accounts():
    accounts = con.get_accounts()
    return jsonify(accounts)


@app.route("/account", methods=["POST"])
def upsert_account():
    details = request.get_json()
    number = details["number"]
    name = details["name"]
    broker = details["broker"]
    server = details["server"]
    deposit = details["deposit"]
    credit = details["credit"]
    withdraw = details["withdraw"]
    balance = details["balance"]
    equity = details["equity"]
    margin = details["margin"]
    deals = details["deals"]
    netvolume = details["netvolume"]
    netprofit = details["netprofit"]
    positions = details["positions"]
    floatvolume = details["floatvolume"]
    floatprofit = details["floatprofit"]
    depositload = details["depositload"]
    drawdown = details["drawdown"]
    lastupdate = details["lastupdate"]
    result = con.upsert_account(number, name, broker, server, deposit, credit, withdraw, balance,
                                equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                                depositload, drawdown, lastupdate)
    return jsonify(result)


@app.route('/deals', methods=["GET"])
@cache.cached(timeout=300)
def get_deals():
    deals = con.get_deals()
    return jsonify(deals)


@app.route("/deal", methods=["POST"])
def insert_deal():
    details = request.get_json()
    ticket = details["ticket"]
    number = details["number"]
    time = details["time"]
    symbol = details["symbol"]
    type = details["type"]
    volume = details["volume"]
    price = details["price"]
    sl = details["sl"]
    tp = details["tp"]
    commission = details["commission"]
    swap = details["swap"]
    profit = details["profit"]
    magic = details["magic"]
    comment = details["comment"]
    result = con.insert_deal(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic,
                             comment)
    return jsonify(result)


@app.route('/positions', methods=["GET"])
@cache.cached(timeout=300)
def get_positions():
    positions = con.get_positions()
    return jsonify(positions)


@app.route("/position", methods=["POST"])
def insert_position():
    details = request.get_json()
    ticket = details["ticket"]
    number = details["number"]
    time = details["time"]
    symbol = details["symbol"]
    type = details["type"]
    volume = details["volume"]
    price = details["price"]
    sl = details["sl"]
    tp = details["tp"]
    commission = details["commission"]
    swap = details["swap"]
    profit = details["profit"]
    magic = details["magic"]
    comment = details["comment"]
    result = con.insert_position(ticket, number, time, symbol, type, volume, price, sl, tp, commission, swap, profit,
                                 magic, comment)
    return jsonify(result)


@app.route("/reset_positions", methods=["POST"])
def reset_positions():
    details = request.get_json()
    number = details["number"]
    result = con.reset_positions(number)
    return jsonify(result)


@app.route("/sentiment", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def get_sentiment():
    details = request.args
    symbol = details.get("symbol")
    number = details.get("number")
    error = details.get("error")
    con.upsert_status(number, 1, error)
    sentiment = con.get_sentiment(symbol)
    if sentiment:
        return jsonify(sentiment[0])
    else:
        return "0"


@app.route("/contrarian", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def get_contrarian():
    details = request.args
    symbol = details.get("symbol")
    number = details.get("number")
    error = details.get("error")
    con.upsert_status(number, 1, error)
    contrarian = con.get_contrarian(symbol)
    if contrarian:
        return jsonify(contrarian[0])
    else:
        return "0"


@app.route("/contrarian", methods=["POST"])
def update_contrarian():
    details = request.get_json()
    symbol = details["symbol"]
    contrarian = details["contrarian"]
    result = con.update_contrarian(symbol, contrarian)
    return jsonify(result)


@app.route("/sentiments", methods=["GET"])
@cache.cached(timeout=300)
def get_sentiments():
    sentiments = con.get_sentiments()
    return jsonify(sentiments)


@app.route("/tas", methods=["GET"])
@cache.cached(timeout=300)
def get_tas():
    signals = con.get_tas()
    return jsonify(signals)


@app.route("/status", methods=["GET"])
@cache.cached(timeout=30)
def get_status():
    status = con.get_status()
    con.reset_status()
    return jsonify(status)


@app.route("/signals", methods=["GET"])
@cache.cached(timeout=300)
def get_signals():
    signals = con.get_signals()
    return jsonify(signals)


@app.route("/signal", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def get_signal():
    details = request.args
    symbol = details.get("symbol")
    number = details.get("number")
    error = details.get("error")
    con.upsert_status(number, 1, error)
    signal = con.get_signal(symbol)
    if signal:
        return jsonify(signal[0])
    else:
        return "0"


@app.route("/signal", methods=["POST"])
def upsert_signal():
    details = request.get_json()
    number = details["number"]
    symbol = details["symbol"]
    type = details["type"]
    risk = details["risk"]
    open_price = details["open_price"]
    result = con.upsert_signal(number, symbol, type, risk, open_price)
    return jsonify(result)


@app.route("/price", methods=["POST"])
def update_signal():
    details = request.get_json()
    symbol = details["symbol"]
    current_price = details["current_price"]
    result = con.update_signal(symbol, current_price)
    return jsonify(result)


@app.route('/')
@cache.cached(timeout=300)
def home():
    return render_template('index.html')


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers[
        "Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    init()
    app.run(host='127.0.0.1', port=8000, debug=False)
