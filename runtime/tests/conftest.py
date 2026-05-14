import sys
from pathlib import Path

# Allow `from core.xxx import ...` when running pytest from repo root or runtime/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
