from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# ============================
# Load schemes.json safely
# ============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "schemes.json")

with open(file_path, "r", encoding="utf-8") as f:
    schemes = json.load(f)

# ============================
# Home Route
# ============================

@app.route("/")
def home():
    return render_template("index.html")

# ============================
# Recommendation Route (for fetch)
# ============================

@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    income = int(data.get("income", 0))
    disability = data.get("disability", "no")
    education = data.get("education", "any")
    location = data.get("location", "any")

    matched_schemes = []

    for scheme in schemes:

        score = 0
        reason_parts = []

        if income <= scheme["income_max"]:
            score += 25
            reason_parts.append("income within limit")
        else:
            continue

        if scheme["disability_required"]:
            if disability == "yes":
                score += 25
                reason_parts.append("disability eligible")
            else:
                continue
        else:
            score += 25

        if scheme["education"] == "any" or scheme["education"] == education:
            score += 25
            reason_parts.append("education criteria matched")
        else:
            continue

        if scheme["location"] == "any" or scheme["location"] == location:
            score += 25
            reason_parts.append("location criteria matched")
        else:
            continue

        matched_schemes.append({
            "name": scheme["name"],
            "description": scheme["description"],
            "apply_link": scheme["apply_link"],
            "score": score,
            "reason": ", ".join(reason_parts)
        })

    return jsonify(matched_schemes)



# ============================
# Run Server
# ============================

if __name__ == "__main__":
    app.run(debug=True)

