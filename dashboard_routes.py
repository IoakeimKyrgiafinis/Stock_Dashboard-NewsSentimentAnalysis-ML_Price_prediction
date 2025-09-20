
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from predictor import XGBPricePredictor


load_dotenv()
dashboard_routes_bp = Blueprint("dashboard_routes", __name__)

EOD_API_KEY = os.getenv("EOD_API_KEY", "demo")
EOD_BASE_URL = "https://eodhd.com/api/eod"

def fetch_eod_data(symbol):
    url = f"{EOD_BASE_URL}/{symbol}.US?api_token={EOD_API_KEY}&fmt=json"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Request failed: {resp.status_code} {resp.text}")

    data = resp.json()
    if not isinstance(data, list) or len(data) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False)
    return df


# ------------------------
# FORM PAGE
# ------------------------
@dashboard_routes_bp.route("/stocks/form")
def stocks_form():
    return render_template("stocks_form.html")


@dashboard_routes_bp.route("/stocks/form", methods=["POST"])
def submit_symbol():
    symbol = request.form.get("symbol", "").upper().strip()
    if not symbol:
        return redirect(url_for("dashboard_routes.stocks_form"))
    return redirect(url_for("dashboard_routes.stocks_dashboard", symbol=symbol))


# ------------------------
# DASHBOARD PAGE (HTML)
# ------------------------
@dashboard_routes_bp.route("/stocks/dashboard")
def stocks_dashboard():
    """
    Render dashboard.html template with symbol context
    """
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return redirect(url_for("dashboard_routes.stocks_form"))
    return render_template("stocks_dashboard.html", symbol=symbol)


# ------------------------
# API ENDPOINT (JSON)
# ------------------------
@dashboard_routes_bp.route("/api/stocks")
def get_stocks_api():
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return jsonify({"error": "Missing stock symbol"}), 400

    try:
        df = fetch_eod_data(symbol)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if df.empty:
        return jsonify({"error": "No stock data found"}), 404

    latest_row = df.iloc[0]
    latest_data = {
        "timestamp": latest_row["date"].strftime("%Y-%m-%d"),
        "close": f"${latest_row['close']:.2f}"
    }

    preview = df.head().to_dict(orient="records")
    all_data = df[["date", "close"]].to_dict(orient="records")

    return jsonify({
        "symbol": symbol,
        "latest": latest_data,
        "preview": preview,
        "data": all_data
    })


@dashboard_routes_bp.route("/api/predict")
def predict_stock_price():
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return jsonify({"error": "Missing symbol"}), 400

    # Fetch full historical data
    df = fetch_eod_data(symbol)
    if df.empty:
        return jsonify({"error": "No stock data found"}), 404

    try:
        predictor = XGBPricePredictor(lags=10)
        predictor.train(df)  # train on last ~250 rows
        date, price = predictor.predict_next_day(df)  # predict using same recent data

        return jsonify({
            "predicted_date": date,
            "predicted_next_close": price,
            "last_date_in_data": str(predictor.last_date)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
