# CISC/CMPE 204: Model Dungeon Generator

This project explores valid arrangements of rooms for a [dungeon crawler](https://en.wikipedia.org/wiki/Dungeon_crawl).
We specify dungeons as a set of 13 rooms (tiles), 2 of which have special properties:

- The start tile, where the player would start the level
- The end tile, where the player must arrive to finish the level

Note that this model does not explore gameplay through the dungeon.
It simply lists the valid arrangements of tiles for level generation.

## Our Model

Our model generates level maps for dungeon crawlers. We display these maps on a square grid of locations, as shown below.
[Example Map 1](example_solutions/sol1.png)
[Example Map 2](example_solutions/sol2.png)
[Example Map 3](example_solutions/sol3.png)

## Structure

* `utils.py`: Contains legacy code from project draft (remove this!)
* `start.bat`: Run this file to execute run.py via Docker. If this doesn't work, start Docker Desktop first.

* `documents`: Contains folders for both the draft and final submissions. README.md files are included in both.
* `example_solutions`: A folder with some screenshots of our working model.
* `run.py`: This file contains the bulk of our files
* `test.py`: A file provided to make sure everything is in the submission.

## Running the Model

You will need Docker installed to run the project.

1) Run the file start.bat. If this doesn't work, open Docker Desktop and try again. 
2) If that doesn't work, open Command Prompt and cd into this directory, then run each command in start.bat

# ModelDungeonGenerator
A modelling project for CISC 204 where we model a dungeon generator in propositional logic.
