import pytest
from battling_knights import Knight, Item, initialize_board, process_moves, resolve_battle, final_state_to_json

def test_knight_initialization():
    knight = Knight('RED', (0, 0))
    assert knight.name == 'RED'
    assert knight.position == (0, 0)
    assert knight.attack == 1
    assert knight.defense == 1
    assert knight.status == "LIVE"
    assert knight.item is None

def test_knight_move():
    knight = Knight('RED', (0, 0))
    knight.move('S')
    assert knight.position == (1, 0)
    knight.move('E')
    assert knight.position == (1, 1)
    knight.move('N')
    assert knight.position == (0, 1)
    knight.move('W')
    assert knight.position == (0, 0)

def test_knight_drown():
    knight = Knight('RED', (0, 0))
    knight.move('N')
    assert knight.status == "DROWNED"
    assert knight.position is None

def test_knight_equip_item():
    knight = Knight('RED', (0, 0))
    item = Item('Axe', (2, 2), 2, 0, 3)
    knight.equip_item(item)
    assert knight.item == item
    assert knight.attack + knight.item.attack == 3
    assert knight.defense + knight.item.defense == 1

def test_knight_unequip_item():
    knight = Knight('RED', (0, 0))
    item = Item('Axe', (2, 2), 2, 0, 3)
    knight.equip_item(item)
    knight.un_equip_item()
    assert knight.item is None
    assert item.equiped_by is None

def test_process_moves():
    items, knights = initialize_board()
    moves = ["R:E", "R:E", "R:S", "R:S", "R:S", "R:S"]
    process_moves(moves, items, knights)
    assert knights['R'].position == (4, 2)
    assert knights['R'].item == items['A']
    assert items['A'].equiped_by == knights['R']

def test_battle_resolution():
    items, knights = initialize_board()
    attacker = knights['R']
    defender = knights['B']
    knights['B'].item = items['A']
    defender.position = attacker.position
    resolve_battle(attacker, defender)
    assert defender.status == "DEAD"
    assert attacker.item == items['A']

def test_final_state_to_json():
    items, knights = initialize_board()
    final_state = final_state_to_json(items, knights)
    expected_state = {
        "red": [[0, 0], "LIVE", None, 1, 1],
        "blue": [[7, 0], "LIVE", None, 1, 1],
        "green": [[7, 7], "LIVE", None, 1, 1],
        "yellow": [[0, 7], "LIVE", None, 1, 1],
        "Axe": [[2, 2], None],
        "Dagger": [[2, 5], None],
        "Helmet": [[5, 2], None],
        "MagicStaff": [[5, 5], None]
    }
    assert final_state == expected_state

def test_custom_moves_set_1():
    items, knights = initialize_board()
    moves = ['R:S', 'R:S', 'B:E', 'G:N', 'Y:N']
    process_moves(moves, items, knights)
    final_state = final_state_to_json(items, knights)
    expected_state = {
        "red": [[2, 0], "LIVE", None, 1, 1],
        "blue": [[7, 1], "LIVE", None, 1, 1],
        "green": [[6, 7], "LIVE", None, 1, 1],
        "yellow": [None, "DROWNED", None, 0, 0],
        "Axe": [[2, 2], None],
        "Dagger": [[2, 5], None],
        "Helmet": [[5, 2], None],
        "MagicStaff": [[5, 5], None]
    }
    assert final_state == expected_state


def test_custom_moves_set_2():
    items, knights = initialize_board()
    moves = ['R:E', 'R:E', 'R:S', 'R:S', 'R:N', 'R:N', 'R:N']
    process_moves(moves, items, knights)
    final_state = final_state_to_json(items, knights)
    expected_state = {
        "red": [None, "DROWNED", None, 0, 0],
        "blue": [[7, 0], "LIVE", None, 1, 1],
        "green": [[7, 7], "LIVE", None, 1, 1],
        "yellow": [[0, 7], "LIVE", None, 1, 1],
        "Axe": [[0, 2], None],
        "Dagger": [[2, 5], None],
        "Helmet": [[5, 2], None],
        "MagicStaff": [[5, 5], None]
    }
    assert final_state == expected_state




if __name__ == "__main__":
    pytest.main()


