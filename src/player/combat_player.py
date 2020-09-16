from player.player import Player
from unit.scout import Scout
from unit.destroyer import Destroyer


class CombatPlayer(Player):

    buy_destroyer = True

    # Upgrade ship size tech to 2
    def upgrade_tech(self):
        while True:
            if self.tech['ss'] < 2 and 'ss' in self.tech.get_available(self.cp):
                self.buy_tech('ss')
            else:
                break

    # Buy a scout or destroyer
    def build_fleet(self):
        ships = {"Scout": Scout, "Destroyer": Destroyer}
        can_buy_destroyer = self.cp >= 9 and self.tech['ss'] >= Destroyer.req_size_tech
        if self.buy_destroyer:
            if not can_buy_destroyer:
                return
            ship_to_buy = Destroyer
        else:
            ship_to_buy = Scout
        if self.cp >= ship_to_buy.cp_cost:
            self.build_unit(ship_to_buy)
            self.buy_destroyer = not self.buy_destroyer

    # Move all units
    def move_units(self, phase):
        for unit in self.units:
            self.move_towards_center(unit, phase)

    # Move to the square closest to the center
    def move_towards_center(self, unit, phase):
        if unit.pos == self.game.board.center:
            return
        moves = self.tech.get_spaces()[phase]
        possible_spaces = self.game.board.get_possible_spots(unit.pos, moves)
        distances = [dist(self.game.board.center, pos)
                     for pos in possible_spaces]
        next_space = possible_spaces[distances.index(min(distances))]
        unit.move(next_space)

    # Choose the first unit to attack
    def choose_unit_to_attack(self, units):
        return units[0]

    # Don't screen any units
    def screen_units(self):
        return []


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5