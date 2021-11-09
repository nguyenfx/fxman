from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request, render_template
import con
import trend
from db import create_tables

app = Flask(__name__)


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


@app.route("/dailyprofits", methods=["GET"])
def get_dailyprofits():
    details = request.args
    number = details.get("number")
    dailyprofits = con.get_dailyprofits(number)
    return jsonify(dailyprofits)


@app.route("/symbolprofits", methods=["GET"])
def get_symbolprofits():
    details = request.args
    number = details.get("number")
    symbolprofits = con.get_symbolprofits(number)
    return jsonify(symbolprofits)


@app.route("/trend", methods=["GET"])
def get_trend():
    details = request.args
    symbol = details.get("symbol")
    ret = trend.get(symbol)
    return jsonify(ret)


@app.route('/')
def home():
    return render_template('index.html')


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    trend.fetch()
    scheduler = BackgroundScheduler(daemon=True, timezone="Europe/Berlin")
    scheduler.add_job(trend.fetch, 'interval', minutes=1)
    scheduler.start()
    create_tables()
    app.run(host='127.0.0.1', port=8000, debug=False)
