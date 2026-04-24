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

subject_dict = {
                14: {"subject": "현대사회와지속가능경영", "short": "현사지경", "professor": "ㅇㅈㅇ",
                     "message": "현대사회와지속가능경영(ㅇㅈㅇ 교수님)\n2025학년도 2학기 중간고사 10,000₩\n2025학년도 2학기 기말고사 10,000₩\n\n2025학년도 2학기 중간/기말고사 15,000₩\nhttps://open.kakao.com/o/snyH7kri\n구매 의향 있으신가요?"}}
