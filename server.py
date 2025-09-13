from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
from bleak import BleakScanner
import datetime

app = Flask(__name__)
CORS(app)

# Mock student registry: RollNo → BLE device name or address
students = {
    "21CS101": {"name": "John Doe", "id": "Galaxy-M21"},
    "21CS102": {"name": "Jane Smith", "id": "Redmi-Note-10"}
}

attendance_log = {}

@app.route("/api/start-scan", methods=["POST"])
def start_scan():
    today = str(datetime.date.today())
    if today not in attendance_log:
        attendance_log[today] = {}

    detected = []

    async def run_scan():
        devices = await BleakScanner.discover(timeout=8)
        for d in devices:
            for roll, info in students.items():
                if info["id"].lower() in (d.name or "").lower():
                    attendance_log[today][roll] = True
                    detected.append({"roll": roll, "name": info["name"]})
        return detected

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    detected = loop.run_until_complete(run_scan())

    return jsonify({"date": today, "present": detected})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
