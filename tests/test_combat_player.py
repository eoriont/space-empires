import sys
sys.path.append('src')
try:
    from game import Game
    from unit.scout import Scout
    from unit.colony_ship import Colonyship
    from unit.destroyer import Destroyer
    from player.combat_player import CombatPlayer
    from otest import do_assert, assert_err, assert_success, assert_bool, color_print
except ImportError as e:
    print(e)

game = Game((5, 5), logging=False, rendering=False, die_mode="ascend")


def assert_unit_positions(turn, phase, player, pos, units):
    board_units = [type(unit)
                   for unit in game.board[pos] if unit.player == player]
    unit_counts = {unit_type: board_units.count(
        unit_type) for unit_type in board_units}
    # Is units a subset of unit_counts?
    assert_bool(
        f"unit positions turn {turn} phase {phase}", units.items() <= unit_counts.items())


def assert_cp(turn, player, cp):
    do_assert(f"{player.name} has cp {cp} at turn {turn}", player.cp, cp)


p1 = CombatPlayer(1, "CombatPlayer1", (2, 0), game, "red")
p2 = CombatPlayer(2, "CombatPlayer2", (2, 4), game, "blue")
game.add_player(p1)
game.add_player(p2)

# Turn 1 Movement Phases
print("Movement Phase Turn 1")
game.complete_movement_phase()
assert_unit_positions(1, "movement", p1, (2, 2), {Scout: 3, Colonyship: 3})
assert_unit_positions(1, "movement", p2, (2, 2), {Scout: 3, Colonyship: 3})

# Turn 1 Combat Phase
print("Combat Phase Turn 1")
game.complete_combat_phase()
assert_unit_positions(1, "combat", p1, (2, 2), {Scout: 3})
assert_unit_positions(1, "combat", p2, (2, 2), {})

# Turn 1 Economic Phase
print("Economic Phase Turn 1")
game.complete_economic_phase()
assert_unit_positions(1, "economic", p1, (2, 0), {})
assert_unit_positions(1, "economic", p2, (2, 4), {Destroyer: 1})
assert_cp(1, p1, 7)
assert_cp(1, p2, 1)

# Turn 2 Movement Phases
print("Movement Phase Turn 2")
game.complete_movement_phase()
assert_unit_positions(2, "movement", p1, (2, 2), {Scout: 3})
assert_unit_positions(2, "movement", p2, (2, 2), {Destroyer: 1})

# Turn 2 Combat Phase
print("Combat Phase Turn 2")
game.complete_combat_phase()
assert_unit_positions(2, "combat", p1, (2, 2), {Scout: 1})
assert_unit_positions(2, "combat", p2, (2, 2), {})
color_print("All tests passed! (For ascending dice rolls)", "Blue")

# =========================================================================
game = Game((5, 5), logging=False, rendering=False, die_mode="descend")
p1 = CombatPlayer(1, "CombatPlayer1", (2, 0), game, "red")
p2 = CombatPlayer(2, "CombatPlayer2", (2, 4), game, "blue")
game.add_player(p1)
game.add_player(p2)

# Turn 1 Movement Phases
print("Movement Phase Turn 1")
game.complete_movement_phase()
assert_unit_positions(1, "movement", p1, (2, 2), {Scout: 3, Colonyship: 3})
assert_unit_positions(1, "movement", p2, (2, 2), {Scout: 3, Colonyship: 3})

# Turn 1 Combat Phase
print("Combat Phase Turn 1")
game.complete_combat_phase()
assert_unit_positions(1, "combat", p1, (2, 2), {})
assert_unit_positions(1, "combat", p2, (2, 2), {Scout: 3})

# Turn 1 Economic Phase
print("Economic Phase Turn 1")
game.complete_economic_phase()
assert_unit_positions(1, "economic", p1, (2, 0), {Destroyer: 1})
assert_unit_positions(1, "economic", p2, (2, 4), {})
assert_cp(1, p1, 1)
assert_cp(1, p2, 7)

# Turn 2 Movement Phases
print("Movement Phase Turn 2")
game.complete_movement_phase()
assert_unit_positions(2, "movement", p1, (2, 2), {Destroyer: 1})
assert_unit_positions(2, "movement", p2, (2, 2), {Scout: 3})

# Turn 2 Combat Phase
print("Combat Phase Turn 2")
game.complete_combat_phase()
assert_unit_positions(2, "combat", p1, (2, 2), {})
assert_unit_positions(2, "combat", p2, (2, 2), {Scout: 3})
print("All tests passed! (For ascending dice rolls)")