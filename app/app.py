import os, json
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "students.json")
MSSV = os.environ.get("MSSV", "2412111011")
HOTEN = "Vũ Minh Hiếu"

def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>DG1 – {{h}} – {{m}}</title>
<link rel="stylesheet" href="/static/style.css"></head><body>
<h1>DG1 – {{h}} – {{m}}</h1>
<table><tr><th>ID</th><th>Tên</th><th>Lớp</th><th>Điểm</th></tr>
{% for s in ds %}<tr><td>{{s.id}}</td><td>{{s.ten}}</td><td>{{s.lop}}</td><td>{{s.diem}}</td></tr>{% endfor %}
</table></body></html>"""

@app.get("/")
def home():
    return render_template_string(PAGE, h=HOTEN, m=MSSV, ds=load())

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "student": MSSV})

@app.get("/api/students")
def students():
    ds = load()
    lop = request.args.get("lop")
    if lop:
        ds = [s for s in ds if s.get("lop") == lop]
    return jsonify(ds)

@app.get("/api/students/<int:sid>")
def one(sid):
    for s in load():
        if s["id"] == sid:
            return jsonify(s)
    return jsonify({"error": "not found"}), 404

@app.post("/api/students")
def create():
    body = request.get_json(silent=True) or {}
    ten, lop, diem = body.get("ten"), body.get("lop"), body.get("diem")
    if not ten or not lop or diem is None:
        return jsonify({"error": "missing field"}), 400
    if isinstance(diem, bool) or not isinstance(diem, (int, float)) or not 0 <= diem <= 10:
        return jsonify({"error": "diem must be 0-10"}), 400
    ds = load()
    new = {"id": max([s["id"] for s in ds], default=0) + 1, "ten": ten, "lop": lop, "diem": diem}
    ds.append(new)
    save(ds)
    return jsonify(new), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))