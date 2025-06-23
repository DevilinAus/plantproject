#!/bin/bash

set -e

cd "$(dirname "$0")"

source .venv/bin/activate

echo "[INFO] Starting arduino_logger..."
python -m scripts.arduino_logger &

echo "[INFO] Starting process_sensor_data..."
python -m scripts.process_sensor_data &

echo "[INFO] Both services started. Waiting for them to complete (Ctrl+C to exit)."
wait