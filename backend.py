# backend.py
from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
from bleak import BleakScanner

app = Flask(__name__)
CORS(app)

async def scan_devices():
    devices = await BleakScanner.discover(timeout=5)
    result = []
    for d in devices:
        result.append({"id": d.address, "name": d.name or "Unknown"})
    return result

@app.route("/api/start-scan")
def start_scan():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    devices = loop.run_until_complete(scan_devices())
    return jsonify({"students": devices})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
