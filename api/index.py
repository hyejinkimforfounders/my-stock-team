"""Vercel Python 서버리스 진입점 — web/app.py의 Flask `app`을 그대로 노출.

vercel.json의 rewrites가 모든 경로를 이 함수로 보내고,
@vercel/python 런타임이 WSGI `app` 객체를 자동으로 구동합니다.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "web"))

from app import app   # noqa: E402,F401  (Vercel이 이 `app`을 구동)
