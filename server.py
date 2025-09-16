from flask import Flask, request, send_file, abort, jsonify
import os, random, time

BASE = os.path.dirname(os.path.abspath(__file__))
GEN4_DIR = os.path.join(BASE, "wonder_gen4")
GEN5_DIR = os.path.join(BASE, "wonder_gen5")
LOGFILE = os.path.join(BASE, "server.log")

app = Flask(__name__)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    print(line, end="")
    with open(LOGFILE, "a") as f:
        f.write(line)

def list_files(folder, exts):
    return [f for f in os.listdir(folder) if any(f.lower().endswith(e) for e in exts)]

@app.route("/")
def index():
    return "Pokémon Wonder Card Server running"

@app.route("/gen4")
def gen4():
    files = list_files(GEN4_DIR, [".pcd", ".pgt"])
    if not files: return abort(404, "No Gen4 files")
    chosen = request.args.get("file") or random.choice(files)
    if chosen not in files: return abort(404, "File not found")
    log(f"Gen4 send {chosen} to {request.remote_addr}")
    return send_file(os.path.join(GEN4_DIR, chosen), mimetype="application/octet-stream")

@app.route("/gen5")
def gen5():
    files = list_files(GEN5_DIR, [".pgf"])
    if not files: return abort(404, "No Gen5 files")
    chosen = request.args.get("file") or random.choice(files)
    if chosen not in files: return abort(404, "File not found")
    log(f"Gen5 send {chosen} to {request.remote_addr}")
    return send_file(os.path.join(GEN5_DIR, chosen), mimetype="application/octet-stream")

@app.route("/list")
def list_all():
    return jsonify({
        "gen4": list_files(GEN4_DIR, [".pcd", ".pgt"]),
        "gen5": list_files(GEN5_DIR, [".pgf"])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
