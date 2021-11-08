from flask import Flask, jsonify, request
import con
from db import create_tables

app = Flask(__name__)


@app.route('/accounts', methods=["GET"])
def get_accounts():
    accounts = con.get_accounts()
    return jsonify(accounts)


@app.route("/account", methods=["POST"])
def upsert_account():
    account_details = request.get_json()
    number = account_details["number"]
    name = account_details["name"]
    broker = account_details["broker"]
    server = account_details["server"]
    deposit = account_details["deposit"]
    credit = account_details["credit"]
    withdraw = account_details["withdraw"]
    balance = account_details["balance"]
    equity = account_details["equity"]
    margin = account_details["margin"]
    deals = account_details["deals"]
    netvolume = account_details["netvolume"]
    netprofit = account_details["netprofit"]
    positions = account_details["positions"]
    floatvolume = account_details["floatvolume"]
    floatprofit = account_details["floatprofit"]
    depositload = account_details["depositload"]
    drawdown = account_details["drawdown"]
    lastupdate = account_details["lastupdate"]
    result = con.upsert_account(number, name, broker, server, deposit, credit, withdraw, balance,
                             equity, margin, deals, netvolume, netprofit, positions, floatvolume, floatprofit,
                             depositload, drawdown, lastupdate)
    return jsonify(result)


@app.route('/trades', methods=["GET"])
def get_trades():
    trades = con.get_trades()
    return jsonify(trades)


@app.route("/trade", methods=["POST"])
def insert_trade():
    trade_details = request.get_json()
    ticket = trade_details["ticket"]
    number = trade_details["number"]
    mode = trade_details["mode"]
    time = trade_details["time"]
    symbol = trade_details["symbol"]
    type = trade_details["type"]
    volume = trade_details["volume"]
    price = trade_details["price"]
    sl = trade_details["sl"]
    tp = trade_details["tp"]
    commission = trade_details["commission"]
    swap = trade_details["swap"]
    profit = trade_details["profit"]
    magic = trade_details["magic"]
    comment = trade_details["comment"]
    result = con.insert_trade(ticket, number, mode, time, symbol, type, volume, price, sl, tp, commission, swap, profit, magic, comment)
    return jsonify(result)


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers[
        "Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, " \
                                          "Authorization "
    return response


if __name__ == "__main__":
    create_tables()
    app.run(host='127.0.0.1', port=8000, debug=True)
