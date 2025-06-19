#!/usr/bin/env python
from flask import Flask, request, jsonify
import hmac
import hashlib
import time
import requests
import json

app = Flask(__name__)

# WOO X sandbox API 設定
API_KEY = "Zzzlto8xvlm+hs+GfjFU9g=="
API_SECRET = "BF2DXYZ53TUFMBP3K2GYSJM2BUVO"
BASE_URL = "https://api-sandbox.woo.org"

# 工具函式：產生簽名
def generate_signature(api_secret, method, endpoint, body, timestamp):
    body_str = json.dumps(body, separators=(",", ":")) if body else ""
    payload = f"{timestamp}{method}{endpoint}{body_str}"
    return hmac.new(api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

# 主路由：接收 TradingView 訊號
@app.route('/tradingview', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("接收到 webhook 訊息：", data)

        # 資料預處理
        side = data.get("side", "BUY").upper()
        symbol = data.get("symbol", "XRP-USDT").replace("-", "_").upper()
        order_type = data.get("type", "MARKET").upper()
        qty = str(data.get("qty", 1))
        client_order_id = f"tv_{int(time.time())}"

        endpoint = "/v1/order"
        url = BASE_URL + endpoint

        body = {
            "client_order_id": client_order_id,
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "size": qty,
            "order_tag": "tradingview",
            "reduce_only": False
        }

        timestamp = str(int(time.time() * 1000))
        signature = generate_signature(API_SECRET, "POST", endpoint, body, timestamp)

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": API_KEY,
            "X-SIGNATURE": signature,
            "X-TIMESTAMP": timestamp
        }

        response = requests.post(url, headers=headers, json=body)
        print("WOO X 回應：", response.status_code, response.text)

        if response.ok:
            return jsonify({"message": "WOO X 下單成功", "status": "success", "data": response.json()})
        else:
            return jsonify({"message": "WOO X 回傳錯誤", "status": "error", "detail": response.text}), response.status_code

    except Exception as e:
        print("錯誤：", str(e))
        return jsonify({"message": "系統錯誤", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
