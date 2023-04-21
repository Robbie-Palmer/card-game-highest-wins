import random
from typing import List, Union

from pytest_cases import parametrize_with_cases, THIS_MODULE

from highest_wins import main

SeedType = Union[int, float, str, bytes, None]


def case_player_1_win():
    seed_value = 12
    expected_ordered_card_values = [21, 4, 9, 27, 12, 35, 5, 6, 20, 14, 47, 38, 16, 26, 41, 8, 33, 28, 37, 45, 13, 42,
                                    22, 17, 3, 40, 19, 2, 7, 49, 32, 11, 48, 29, 46, 44, 36, 15, 39, 30, 51, 52, 24, 1,
                                    25, 10, 23, 50, 34, 43, 18, 31]
    expected_winners = [1]
    return seed_value, expected_ordered_card_values, expected_winners


def case_player_2_win():
    seed_value = 44
    expected_ordered_card_values = [14, 5, 16, 42, 13, 22, 31, 32, 23, 18, 41, 43, 38, 51, 39, 28, 36, 29, 9, 24, 44,
                                    30, 17, 4, 6, 50, 10, 52, 40, 3, 47, 21, 26, 46, 20, 33, 11, 7, 1, 37, 48, 49, 2,
                                    19, 15, 25, 12, 8, 45, 35, 34, 27]
    expected_winners = [2]
    return seed_value, expected_ordered_card_values, expected_winners


def case_draw() -> (SeedType, List[int], List[int]):
    seed_value = 93
    # Based on random.shuffle being applied on a Deck of 52 cards with the set seed
    expected_ordered_card_values = [18, 40, 9, 30, 29, 22, 15, 4, 1, 33, 44, 52, 17, 13, 46, 27, 2, 35, 39, 28, 7, 41,
                                    31, 20, 45, 19, 50, 16, 21, 34, 25, 14, 5, 51, 43, 24, 42, 36, 3, 38, 11, 48, 26,
                                    12, 10, 49, 6, 8, 23, 47, 37, 32]
    expected_winners = [1, 2]
    return seed_value, expected_ordered_card_values, expected_winners


@parametrize_with_cases('seed_value, expected_ordered_card_values, expected_winners', cases=THIS_MODULE)
def test_game(capfd, seed_value: SeedType, expected_ordered_card_values: List[int], expected_winners: List[int]):
    random.seed(seed_value)
    main()
    actual_output = capfd.readouterr().out
    actual_lines = [line for line in actual_output.split('\n') if line]

    # Expected to be reversed based on taking from the top of the deck
    expected_ordered_card_values.reverse()
    expected_num_players = 2
    expected_num_rounds = 26
    expected_num_lines = (expected_num_players + 1) * (expected_num_rounds + 1)
    assert len(actual_lines) == expected_num_lines, \
        'Expected printed output of one line per player score per round, plus a round summary, ' \
        'followed by a game summary consisting of one line per layer score and a line declaring the winner. ' \
        f'This would total {expected_num_lines} lines of content. ' \
        f'Received {len(actual_lines)} lines of content:\n{actual_output}'

    player_idx_to_hand = {idx: expected_ordered_card_values[expected_num_players - idx::2]
                          for idx in range(1, expected_num_players + 1)}
    expected_round_winner = [1 if player_1_value > player_2_value else 2
                             for (player_1_value, player_2_value) in
                             zip(player_idx_to_hand[1], player_idx_to_hand[2])]
    for round_idx in range(expected_num_rounds):
        for player_idx in range(1, expected_num_players + 1):
            assert actual_lines.pop(0) == f"Player {player_idx}'s card: {player_idx_to_hand[player_idx][round_idx]}"
        assert actual_lines.pop(0) == f"Player {expected_round_winner[round_idx]} wins the round!"
    for player_idx in range(1, expected_num_players + 1):
        assert actual_lines.pop(0) == f"Player {player_idx}'s score: {expected_round_winner.count(player_idx)}"

    expected_winner_statement = f"Player {expected_winners[0]} wins the game!" if len(expected_winners) == 1 \
        else f"Players {[str(i) for i in expected_winners]} have tied the game!"
    assert actual_lines.pop(0) == expected_winner_statement
    assert len(actual_lines) == 0
