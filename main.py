from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/tradingview", methods=["POST"])
def webhook():
    data = request.json
    print("收到 TradingView 訊號：", data)
    return jsonify({"status": "success", "message": "訊號已接收"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
