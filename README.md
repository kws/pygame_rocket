# PyGame Rocket Simulator

A skeleton example of how to get started with sprites in PyGame.

## Installation

```bash
poetry install
```

This will pull down all dependencies and create a virtual environment for you to work in.

You can then run the game with:

```bash
poetry run rocket
```

or

```bash
poetry shell
python -m pygame_rocket
```

## Usage

LEFT_ARROW: rotate counterclockwise
RIGHT_ARROW: rotate clockwise
SPACEBAR: thrust

The rocket thrust in the direction it's facing. To achieve this we use pygame's vector class. We have one vector for the current velocity,
and whenever the rocket thrusts we add a vector in the direction the rocket is facing to the velocity vector.
