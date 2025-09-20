from flask import Flask, request, Response, send_from_directory
import os, random, datetime, xml.etree.ElementTree as ET

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "ac_logs")
EVENTS_GEN4 = os.path.join(BASE_DIR, "wonder_gen4")
EVENTS_GEN5 = os.path.join(BASE_DIR, "wonder_gen5")

os.makedirs(LOG_DIR, exist_ok=True)

# ===== Logging helper =====
def save_raw_request(prefix: str, data: bytes, headers: dict):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S%fZ")
    filename = f"{prefix}_{ts}.bin"
    with open(os.path.join(LOG_DIR, filename), "wb") as f:
        f.write(data)
    with open(os.path.join(LOG_DIR, filename + ".meta"), "w", encoding="utf-8") as f:
        for k, v in headers.items():
            f.write(f"{k}: {v}\n")

# ===== Gen 4: random event =====
@app.route("/gen4/event", methods=["GET"])
def gen4_event():
    files = [f for f in os.listdir(EVENTS_GEN4) if f.lower().endswith((".pgt", ".pcd"))]
    if not files:
        return Response("<error>No Gen4 events found</error>", mimetype="application/xml")

    chosen = random.choice(files)
    print(f"Serving Gen4 event: {chosen}")
    return send_from_directory(EVENTS_GEN4, chosen, mimetype="application/octet-stream")

# ===== Gen 5: random event =====
@app.route("/gen5/event", methods=["GET"])
def gen5_event():
    files = [f for f in os.listdir(EVENTS_GEN5) if f.lower().endswith(".pgf")]
    if not files:
        return Response("<error>No Gen5 events found</error>", mimetype="application/xml")

    chosen = random.choice(files)
    print(f"Serving Gen5 event: {chosen}")
    return send_from_directory(EVENTS_GEN5, chosen, mimetype="application/octet-stream")

# ===== Catch-all =====
@app.route('/', defaults={'path': ''}, methods=['GET','POST'])
@app.route('/<path:path>', methods=['GET','POST'])
def catch_all(path):
    raw = request.get_data()
    headers = dict(request.headers)
    save_raw_request(f"unknown_{path}", raw, headers)
    print(f"Unhandled request: /{path}")
    return Response("<error>Unhandled path</error>", mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
