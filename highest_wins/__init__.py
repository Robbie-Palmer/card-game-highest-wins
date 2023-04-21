import random
from typing import Final, List

from more_itertools import distribute


class Card:
    MIN_VALUE: Final[int] = 1
    MAX_VALUE: Final[int] = 52

    def __init__(self, value: int):
        assert self.MIN_VALUE <= value <= self.MAX_VALUE, \
            f'Card must be in range {self.MIN_VALUE}-{self.MAX_VALUE} inclusive. Received: {value}'
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

    def __lt__(self, other: 'Card') -> bool:
        return self.value < other.value

    def __gt__(self, other: 'Card') -> bool:
        return self.value > other.value

    def __eq__(self, other: 'Card') -> bool:
        return self.value == other.value


class Deck:
    def __init__(self, cards: List[Card]):
        assert len(cards) > 0, 'Cannot create a Deck with no cards'
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise RuntimeError('No cards left to draw')
        return self.cards.pop()

    def deal(self, n: int) -> List['Deck']:
        decks = [Deck(list(cards)) for cards in distribute(n, self.cards)]
        return decks

    def __getitem__(self, index):
        return self.cards[index]

    def __len__(self) -> int:
        return len(self.cards)


class Player:
    def __init__(self, name: str, hand: Deck):
        self.name: str = name
        self._hand = hand
        self.score: int = 0
        self.current_card: Card | None = None

    def draw(self) -> Card:
        self.current_card = self._hand.draw()
        return self.current_card

    @property
    def num_cards(self) -> int:
        return len(self._hand)

    def __repr__(self) -> str:
        return f"Player {self.name}: {self.score} points"


class Game:
    def __init__(self):
        deck_size = 52
        self.deck = Deck([Card(i + 1) for i in range(deck_size)])
        self.num_players = 2

    def play(self):
        self.deck.shuffle()
        players = [Player(str(i + 1), hand) for i, hand in enumerate(self.deck.deal(self.num_players))]
        num_rounds = min([player.num_cards for player in players])
        for round_number in range(num_rounds):
            round_winner: Player | None = None
            for player in players:
                player.draw()
                print(f"Player {player.name}'s card:", player.current_card)
                if not round_winner or player.current_card > round_winner.current_card:
                    round_winner = player
            print(f"Player {round_winner.name} wins the round!\n")
            round_winner.score += 1

        game_winners: List[Player] = []
        for player in players:
            print(f"Player {player.name}'s score:", player.score)
            if not game_winners or player.score > game_winners[0].score:
                game_winners = [player]
            elif player.score == game_winners[0].score:
                game_winners.append(player)
        if len(game_winners) == 1:
            print(f"Player {game_winners[0].name} wins the game!")
        else:
            print(f"Players {[player.name for player in game_winners]} have tied the game!")


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
