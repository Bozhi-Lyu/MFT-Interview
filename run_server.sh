#!/usr/bin/env bash
set -e

python3 -m venv .venv
source .venv/bin/activate

pip install -r backend/requirements.txt -q
pip install -r client/requirements.txt -q

uvicorn backend.main:app --reload
