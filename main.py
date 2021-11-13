from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from uwsgidecorators import postfork
from con import Controller
import sen
import chart

con = Controller()
app = Flask(__name__, static_url_path='/static')
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)


@postfork
def init():
    sen.fetch()
    chart.gen_chart()


@cache.cached(timeout=300)
@app.route('/accounts', methods=["GET"])
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


@cache.cached(timeout=300)
@app.route('/deals', methods=["GET"])
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


@cache.cached(timeout=300)
@app.route('/positions', methods=["GET"])
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


@cache.memoize(timeout=300)
@app.route("/trend", methods=["GET"])
def get_trend():
    details = request.args
    symbol = details.get("symbol")
    number = details.get("number")
    con.upsert_status(number, 1)
    trend = con.get_sentiment(symbol)
    return jsonify(trend[0])


@cache.cached(timeout=300)
@app.route("/sentiments", methods=["GET"])
def get_sentiments():
    sentiments = con.get_sentiments()
    return jsonify(sentiments)


@cache.cached(timeout=300)
@app.route('/')
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
