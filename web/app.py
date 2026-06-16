#!/usr/bin/env python3
"""my-stock-team 웹앱 — 종목명만 입력하면 투자 리포트 PPTX를 생성·다운로드.

실행:
    python3 web/app.py
    → http://127.0.0.1:5000

데이터: DART(재무) + FinanceDataReader(시세). 키는 .env.local의 DART_API_KEY.
가드레일: 매수/매도·목표가 미제시, 출처·기준일 병기, 학습용 명시(가드는 pipeline에 내장).
"""
import os, base64, traceback
from flask import (Flask, render_template, request, send_file,
                   jsonify, abort)

import pipeline

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", dart_ok=bool(pipeline.DART_KEY))


@app.route("/generate", methods=["POST"])
def generate():
    if request.is_json:
        query = (request.json.get("query") or "").strip()
    else:
        query = (request.form.get("query") or "").strip()
    if not query:
        return jsonify({"ok": False, "error": "종목명 또는 6자리 코드를 입력해 주세요."}), 400
    try:
        meta = pipeline.build_report(query)
    except ValueError as e:                 # 종목 해석/데이터 문제 → 사용자 메시지
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:                   # 예기치 못한 오류
        traceback.print_exc()
        return jsonify({"ok": False, "error": f"리포트 생성 중 오류: {e}"}), 500
    # 서버리스 호환: 한 번의 요청으로 PPTX를 base64로 동봉(상태 비저장)
    return jsonify({
        "ok": True,
        "name": meta["name"], "ticker": meta["ticker"],
        "asof": meta["asof"], "filename": meta["filename"],
        "has_price": meta["has_price"], "has_fin": meta["has_fin"],
        "pptx_b64": base64.b64encode(meta["data"]).decode("ascii"),
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
