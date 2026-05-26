#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from primitive_collision_compiler.paper.accv_visuals import main


if __name__ == "__main__":
    raise SystemExit(main())
