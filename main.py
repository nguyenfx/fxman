from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
import con
import trend
from db import create_tables


class FxFlask(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            init()
        super(FxFlask, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = FxFlask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)


def init():
    trend.fetch()
    scheduler = BackgroundScheduler(daemon=True, timezone="Asia/Singapore")
    scheduler.add_job(trend.fetch, 'interval', minutes=7)
    scheduler.start()
    create_tables()


@cache.cached(timeout=600)
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


@cache.cached(timeout=300)
@app.route("/dailyprofits", methods=["GET"])
def get_dailyprofits():
    details = request.args
    number = details.get("number")
    dailyprofits = con.get_dailyprofits(number)
    return jsonify(dailyprofits)


@cache.cached(timeout=300)
@app.route("/symbolprofits", methods=["GET"])
def get_symbolprofits():
    details = request.args
    number = details.get("number")
    symbolprofits = con.get_symbolprofits(number)
    return jsonify(symbolprofits)


@cache.memoize(timeout=300)
@app.route("/trend", methods=["GET"])
def get_trend():
    details = request.args
    symbol = details.get("symbol")
    ret = trend.get(symbol)
    return jsonify(ret)


@cache.cached(timeout=600)
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
    app.run(host='127.0.0.1', port=8000, debug=False)
