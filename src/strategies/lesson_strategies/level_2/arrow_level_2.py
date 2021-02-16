class ArrowStrategyLevel2:
    # Buys as many scouts as possible, then
    # Use 2 to flank from both sides

    def __init__(self, player_index):
        self.player_index = player_index

        # Count of how many units are on each side
        self.formation = [0, 0]

        # How many units to flank on each side
        self.thickness = 3

    def decide_ship_movement(self, unit_index, hidden_game_state):
        enemy_home = hidden_game_state['players'][1-self.player_index]["home_coords"]
        units = hidden_game_state['players'][self.player_index]["units"]
        unit = units[unit_index]

        if self.formation[0] < self.thickness:
            self.formation[0] += 1
            return (1, 0)
        elif self.formation[1] < self.thickness:
            self.formation[1] += 1
            return (-1, 0)
        else:
            ux, uy = unit["coords"]
            ex, ey = enemy_home
            if uy == ey:
                return (ex-ux, 0)
            elif uy < ey:
                return (0, 1)
            else:
                return (0, -1)

    # attack opponent's first ship in combat order
    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        combat_order = combat_state[coords]
        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player_index'] == opponent_index:
                return combat_index

    # Buy all possible scouts
    def decide_purchases(self, game_state):
        return {'technology': [], 'units': [{'type': 'Scout', 'coords': game_state['players'][self.player_index]['home_coords']}] *4}
