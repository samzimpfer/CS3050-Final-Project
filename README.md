# Settlers of Catan

To run, run main.py.

## Description
This is a Settlers of Catan game built for up to 4 players. You may select as many of players as you want to be AI bots. The game supports trading, building settlements and cities, development cards, and a robber. The only major feature that is excluded is maritime trade.

The game is built using a Python Arcade GUI. The AI bots currently use a methodology of weighting resources that the player needs based on potential building schemes and weighting areas of the board that it sho0uld build on to decide what to do on their turns. We plan to improve this process significantly in the future of the project and implement maritime trading, and any other features that the game is missing. One idea we have for improving the AI is to compute a heuristic given a certain board state and attempt to move to a higher ranking state.

## Dependencies
* Python Arcade
