from pathlib import Path


SPRITE_ROOT = Path(__file__).parent

ship_1 = SPRITE_ROOT / "ship-1.png"
ship_2 = SPRITE_ROOT / "ship-2.png"
ship_3 = SPRITE_ROOT / "ship-3.png"

planet_1 = SPRITE_ROOT / "planet-1.png"
planet_2 = SPRITE_ROOT / "planet-2.png"

__all__ = ["ship_1", "ship_2", "ship_3", "planet_1"]