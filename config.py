from pathlib import Path
import sys

ARDUINO_IP = "192.168.0.99"

BASE_DIR = Path(__file__).resolve().parent


if "pytest" in sys.modules:
    # Using bad path on purpose to ensure not using real DB.
    DB_PATH = BASE_DIR / "instance/plant_info-test.db"
else:
    DB_PATH = BASE_DIR / "instance/plant_info.db"
