import json
import time
import websocket

class BinanceWebSocket:
    def __init__(self, symbol, on_tick_callback):
        self.symbol = symbol.lower()
        self.on_tick_callback = on_tick_callback
        self.ws = None

    def _on_message(self, ws, message):
        data = json.loads(message)

        tick = {
            "timestamp": data["E"],     # event time in ms
            "symbol": data["s"],
            "price": float(data["p"]),
            "qty": float(data["q"])
        }

        self.on_tick_callback(tick)

    def _on_error(self, ws, error):
        print("WebSocket error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed. Reconnecting in 2s...")
        time.sleep(2)
        self.start()

    def start(self):
        socket = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"

        self.ws = websocket.WebSocketApp(
            socket,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )

        self.ws.run_forever()
