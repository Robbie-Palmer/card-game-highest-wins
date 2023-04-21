# Highest Wins

A CLI tool which simulates a game of cards between two players
The stages of the game are:
- We start with the deck of 52 cards, each uniquely numbered from 1 to 52
- The deck is shuffled
- We deal out those cards between the 2 players Each player gets half the deck
- On each turn of the game, both players turn over their topmost card, and they compare the value of those cards
- The player with the higher-valued card “wins” the round and gets a point The two cards being compared are discarded
- Rounds are played until all the cards are discarded
- At the end of the game the player who has the most points wins

## Usage

- Install package `pip install .`
- Execute CLI command to run the game `play-highest-wins`

## Developer Setup

- Create a Python environment. Recommended installation:
  - Install [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
  - Create a new python environment `conda create -n highest_wins python=3.10`
  - Active your environment `conda activate highest_wins`
- Install the package in editable mode `pip install -e .`

## Testing

- Install testing dependencies `pip install -r ./tests/requirements.txt`
- Run tests `python -m pytest ./tests`
