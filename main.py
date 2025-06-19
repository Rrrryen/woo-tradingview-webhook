from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/tradingview", methods=["POST"])
def webhook():
    data = request.json
    print("收到 TradingView 訊號：", data)
    return jsonify({"status": "success", "message": "訊號已接收"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
if response.status_code == 200:
    response_json = response.json()
    if response_json.get("success"):
        return jsonify({"message": "✅ 下單成功", "status": "success", "data": response_json.get("data")})
    else:
        return jsonify({"message": "⚠️ WOO X 回應成功但未下單", "status": "warning", "detail": response_json})
else:
    return jsonify({"message": "❌ WOO X 回傳錯誤", "status": "error", "detail": response.text}), 500
