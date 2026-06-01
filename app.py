from flask import Flask, render_template, request, jsonify
from selenium_logic import run_bot
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    try:
        user_id = request.form.get("id")
        user_pw = request.form.get("pw")

        function_number = list(map(int, request.form.getlist("function")))

        subject_number = request.form.get("subject_number")
        subject_number = int(subject_number) if subject_number else None

        subjects = json.loads(request.form.get("subjects") or "{}")

        run_bot(user_id, user_pw, function_number, subject_number, subjects)

        return jsonify({"message": "실행 완료"})

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)